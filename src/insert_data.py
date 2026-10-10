import sqlite3
from pathlib import Path

# Database location
DB_PATH = Path("retail.db")

# Connect to the database
conn = sqlite3.connect(DB_PATH)

# Enable foreign key constraints
conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()

# Customer records
customers = [
    (1, "Alice", "Denmark"),
    (2, "Bob", "Germany"),
    (3, "Charlie", "Denmark")
]

# Insert customers
cursor.executemany(
    """
    INSERT INTO customers (customer_id, name, country)
    VALUES (?, ?, ?)
    """,
    customers
)

# Order records
orders = [
    (101, 1, 150.0),
    (102, 2, 200.0),
    (103, 1, 75.0),
    (104, 3, 300.0)
]

# Insert orders
cursor.executemany(
    """
    INSERT INTO orders (order_id, customer_id, amount)
    VALUES (?, ?, ?)
    """,
    orders
)

# Save changes
conn.commit()

# Close database connection
conn.close()

print("Data inserted successfully!")