# Utility Billing Service

This repository contains a minimal Python implementation for generating and emailing monthly utility invoices.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Initialize the sample database:
   ```bash
   python init_db.py
   ```

## Usage
Run the billing service to send invoices for the current month:
```bash
python billing_service.py
```

The service connects to a SQLite database, calculates the monthly charges for each customer, generates a PDF invoice, and emails it to the customer. Each invoice includes a **Pay Now** link for online payment.

Adjust SMTP settings in `billing_service.py` to point to your email server.
