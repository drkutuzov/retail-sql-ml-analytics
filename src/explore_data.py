import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/raw/Online Retail.xlsx")

df = pd.read_excel(DATA_PATH)

invoice_customers = df.groupby("InvoiceNo")["CustomerID"].nunique(
    dropna=False
)

print("Invoices with multiple customer IDs:",
      (invoice_customers > 1).sum())

# print("Dataset shape:", df.shape)

# print("\nFirst five rows:")
# print(df.head())

# print("\nColumn information:")
# df.info()

#Exercise 9: Challenge A
# print(df.isna().sum())

#Exercise 9: Challenge B
# missing_pct = 100 * df["CustomerID"].isna().sum() / df["CustomerID"].size
# print(f"Missing CustomerID: {missing_pct:.2f}%")

#Exercise 9: Challenge C
# print(f"Negative quantity values count = {(df["Quantity"] < 0).sum()}")
# print(f"Negative or zero unit price count = {(df["UnitPrice"] <= 0).sum()}") 
