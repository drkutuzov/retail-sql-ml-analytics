
import sqlite3
from pathlib import Path

# Define the database location
DB_PATH = Path("retail_real.db")

# Connect to the database
conn = sqlite3.connect(DB_PATH)

# Enable foreign key constraints
conn.execute("PRAGMA foreign_keys = ON")

# Create a cursor to execute SQL
cursor = conn.cursor()

# Create the customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY
)
""")

# Create the invoices table
cursor.execute("""
CREATE TABLE IF NOT EXISTS invoices (
    invoice_no TEXT PRIMARY KEY,
    invoice_date TEXT NOT NULL,
    customer_id INTEGER,
    country TEXT NOT NULL,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
)
""")

# Create the invoices_items table
cursor.execute("""
CREATE TABLE IF NOT EXISTS invoice_items (
    item_id INTEGER PRIMARY KEY,
    invoice_no TEXT NOT NULL,
    invoice_date TEXT NOT NULL,
    stock_code TEXT NOT NULL,
    description TEXT,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (invoice_no)
        REFERENCES invoices(invoice_no)
)
""")

# Save changes
conn.commit()

# Close the connection
conn.close()

print("Database created successfully!")
