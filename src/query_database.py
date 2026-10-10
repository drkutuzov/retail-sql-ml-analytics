import sqlite3
import pandas as pd

# Connect to SQLite
conn = sqlite3.connect("retail.db")

# Define SQL query
query = """
SELECT
    c.country,
    SUM(o.amount) AS total_revenue
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
    GROUP BY c.country
    ORDER BY total_revenue DESC;
"""

# SELECT
#     customer_id,
#     SUM(amount) AS total_revenue
# FROM orders
# GROUP BY customer_id
# ORDER BY total_revenue DESC;

# Execute query and load results into Pandas
df = pd.read_sql_query(query, conn)

print(df)

# Close connection
conn.close()