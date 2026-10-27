import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "retail_real.db"

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    strftime('%Y-%m', i.invoice_date) AS month,
    SUM(it.quantity * it.unit_price) AS gross_sales
FROM invoices AS i
JOIN invoice_items AS it
    ON i.invoice_no = it.invoice_no
WHERE it.quantity > 0
  AND it.unit_price > 0
  AND it.invoice_no NOT LIKE 'C%'
GROUP BY month
ORDER BY month ASC;
"""

df = pd.read_sql_query(query, conn)
conn.close()


df["month"] = pd.to_datetime(df["month"])

df["growth_pct"] = df["gross_sales"].pct_change() * 100


df_complete = df[
    (df["month"] >= "2011-01-01") &
    (df["month"] <= "2011-11-01")
].copy()

df_complete["growth_pct"] = (
    df_complete["gross_sales"].pct_change() * 100
)

df_complete = df_complete.reset_index(drop=True)

print(df_complete)


# Visualize monthly gross sales
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    df["month"],
    df["gross_sales"] / 1_000_000,
    marker="o"
)

ax.set_title("Monthly Gross Sales")
ax.set_ylabel("Gross Sales (£ millions)")

plt.show()