import sqlite3
import pandas as pd

DB_PATH = "retail_real.db"

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    i.country,
    SUM(it.quantity * it.unit_price) AS gross_sales
FROM invoices AS i
JOIN invoice_items AS it
    ON i.invoice_no = it.invoice_no
WHERE it.quantity > 0
  AND it.unit_price > 0
  AND it.invoice_no NOT LIKE 'C%'
GROUP BY i.country
ORDER BY gross_sales DESC;
"""

df = pd.read_sql_query(query, conn)

conn.close()

print(df.head(10))

# Visualize the top 10 countries by gross sales
import matplotlib.pyplot as plt

top10 = df.head(10)

fig, ax = plt.subplots(figsize=(10, 6))

ax.barh(
    top10["country"],
    top10["gross_sales"] / 1_000_000
)

ax.invert_yaxis()
ax.set_xscale("log")

ax.set_xlabel("Gross sales (£ millions)")
ax.set_ylabel("Country")
ax.set_title("Top 10 countries by gross sales")

fig.tight_layout()

fig.savefig(
    "results/figures/gross_sales_by_country.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()