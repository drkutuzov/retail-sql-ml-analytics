
import sqlite3
from pathlib import Path

# Define the database location
DB_PATH = Path("retail.db")

# Connect to the database
conn = sqlite3.connect(DB_PATH)

# Enable foreign key constraints
conn.execute("PRAGMA foreign_keys = ON")

# Create a cursor to execute SQL
cursor = conn.cursor()

# Create the customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT
)
""")

# Create the orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
)
""")

# Save changes
conn.commit()

# Close the connection
conn.close()

print("Database created successfully!")
