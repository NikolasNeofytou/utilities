import sqlite3

DATABASE = 'utilities.db'

schema = '''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER REFERENCES customers(id),
    month TEXT NOT NULL,
    amount REAL NOT NULL
);
'''

def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.executescript(schema)
    # example data
    conn.execute("INSERT INTO customers (name, email) VALUES (?, ?)",
                 ("Alice", "alice@example.com"))
    conn.execute("INSERT INTO customers (name, email) VALUES (?, ?)",
                 ("Bob", "bob@example.com"))
    conn.execute(
        "INSERT INTO usage (customer_id, month, amount) VALUES (?,?,?)",
        (1, '2023-07', 50.75)
    )
    conn.execute(
        "INSERT INTO usage (customer_id, month, amount) VALUES (?,?,?)",
        (2, '2023-07', 65.20)
    )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print('Database initialized with sample data.')
