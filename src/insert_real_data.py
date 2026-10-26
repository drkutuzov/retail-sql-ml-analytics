import sqlite3
import pandas as pd
from pathlib import Path

# Raw data excel file location
DATA_PATH = Path("data/raw/Online Retail.xlsx")
df = pd.read_excel(DATA_PATH)

# Database location
DB_PATH = Path("retail_real.db")

# Connect to the database
conn = sqlite3.connect(DB_PATH)

# Enable foreign key constraints
conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()


try:

    # Ensure all tables are empty before importing
    tables = ["customers", "invoices", "invoice_items"]

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]

        if count > 0:
            raise RuntimeError(
                f"Table '{table}' already contains {count} records. "
                "Import requires an empty database."
            )
    
    #---------------------------------------
    # Customer records
    customers = (
        df[["CustomerID"]]
        .dropna()
        .drop_duplicates()
        .astype(int)
    )

    customers = customers.rename(
        columns={"CustomerID": "customer_id"}
    )

    # Insert customers into the database
    cursor.executemany(
        """
        INSERT INTO customers (customer_id)
        VALUES (?)
        """,
        customers.itertuples(index=False, name=None)
    )

    #---------------------------------------
    # Invoices records
    invoices = (
        df.groupby("InvoiceNo")
        .agg({
            "InvoiceDate": "min",
            "CustomerID": "first",
            "Country": "first"
        })
        .reset_index()
    )

    invoices = invoices.rename(columns={
        "InvoiceNo": "invoice_no",
        "InvoiceDate": "invoice_date",
        "CustomerID": "customer_id",
        "Country": "country"
    })

    invoices["invoice_no"] = invoices["invoice_no"].astype(str)

    invoices["invoice_date"] = (
        pd.to_datetime(invoices["invoice_date"])
        .dt.strftime("%Y-%m-%d %H:%M:%S")
    )

    invoices["customer_id"] = (
        invoices["customer_id"].astype("Int64")
    )

    invoice_records = [
        (
            row.invoice_no,
            row.invoice_date,
            int(row.customer_id) if pd.notna(row.customer_id) else None,
            row.country
        )
        for row in invoices.itertuples(index=False)
    ]

    # Insert invoices into the database
    cursor.executemany(
        """
        INSERT INTO invoices (
            invoice_no,
            invoice_date,
            customer_id,
            country
        )
        VALUES (?, ?, ?, ?)
        """,
        invoice_records
    )

    #---------------------------------------
    # Invoice items records
    items = df[[
        "InvoiceNo",
        "InvoiceDate",
        "StockCode",
        "Description",
        "Quantity",
        "UnitPrice"
    ]].copy()

    items = items.rename(columns={
        "InvoiceNo": "invoice_no",
        "InvoiceDate": "invoice_date",
        "StockCode": "stock_code",
        "Description": "description",
        "Quantity": "quantity",
        "UnitPrice": "unit_price"
    })

    items["invoice_no"] = items["invoice_no"].astype(str)
    items["stock_code"] = items["stock_code"].astype(str)

    items["invoice_date"] = (
        pd.to_datetime(items["invoice_date"])
        .dt.strftime("%Y-%m-%d %H:%M:%S")
    )

    item_records = [
        (
            row.invoice_no,
            row.invoice_date,
            row.stock_code,
            row.description if pd.notna(row.description) else None,
            int(row.quantity),
            float(row.unit_price)
        )
        for row in items.itertuples(index=False)
    ]

    cursor.executemany(
        """
        INSERT INTO invoice_items (
            invoice_no,
            invoice_date,
            stock_code,
            description,
            quantity,
            unit_price
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        item_records
    )

    conn.commit()

    print("Import completed successfully.")
    print("Customers:", len(customers))
    print("Invoices:", len(invoices))
    print("Invoice items:", len(items))

except Exception:
    conn.rollback()
    raise

finally:
    conn.close()


