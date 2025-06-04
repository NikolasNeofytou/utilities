import os
import sqlite3
from datetime import date
from fpdf import FPDF
import smtplib
from email.message import EmailMessage

DATABASE = 'utilities.db'
INVOICE_DIR = 'invoices'
PAY_URL_TEMPLATE = 'https://payment.example.com/pay?customer_id={id}&amount={amount}'

os.makedirs(INVOICE_DIR, exist_ok=True)


def connect_db():
    return sqlite3.connect(DATABASE)


def calculate_monthly_total(conn, customer_id, billing_month):
    cur = conn.cursor()
    cur.execute(
        'SELECT SUM(amount) FROM usage WHERE customer_id=? AND month=?',
        (customer_id, billing_month)
    )
    result = cur.fetchone()[0]
    return result or 0.0


def generate_invoice(customer, amount, billing_month):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, f"Invoice for {customer['name']}")
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(40, 10, f'Month: {billing_month}')
    pdf.ln(10)
    pdf.cell(40, 10, f'Total amount due: ${amount:.2f}')
    pdf.ln(10)
    pay_url = PAY_URL_TEMPLATE.format(id=customer['id'], amount=amount)
    pdf.cell(40, 10, f'Pay now: {pay_url}')
    pdf_path = os.path.join(INVOICE_DIR, f"invoice_{customer['id']}_{billing_month}.pdf")
    pdf.output(pdf_path)
    return pdf_path


def send_email_with_invoice(customer, pdf_path, amount):
    msg = EmailMessage()
    msg['Subject'] = 'Your utility invoice'
    msg['From'] = 'no-reply@utility.local'
    msg['To'] = customer['email']
    msg.set_content(
        f"Hello {customer['name']},\n"
        f"Your total due is ${amount:.2f}.\n"
        f"Please see attached invoice."
    )
    with open(pdf_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=os.path.basename(pdf_path))

    # Configure your SMTP server details here
    with smtplib.SMTP('localhost') as s:
        s.send_message(msg)


def send_monthly_invoices(billing_month):
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM customers')
    customers = cur.fetchall()
    for customer in customers:
        total = calculate_monthly_total(conn, customer['id'], billing_month)
        if total <= 0:
            continue
        pdf_path = generate_invoice(customer, total, billing_month)
        send_email_with_invoice(customer, pdf_path, total)
        print(f"Sent invoice to {customer['email']} for ${total:.2f}")
    conn.close()


if __name__ == '__main__':
    today = date.today().strftime('%Y-%m')  # e.g., 2023-07
    send_monthly_invoices(today)
