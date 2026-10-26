# Retail SQL & ML Analytics

An end-to-end data analytics project using Python, SQL, and Pandas to explore retail transactions, build a relational database, and analyze business performance.

The project demonstrates a reproducible workflow from raw Excel data to a normalized SQLite database and SQL-based analytics. Future development will include machine learning models for revenue forecasting and customer behavior analysis.

## Project objectives

- Design and implement a relational SQLite database.
- Explore, clean, and transform real-world retail transaction data.
- Analyze revenue, sales trends, and customer behavior using SQL.
- Integrate SQL queries with Python and Pandas.
- Visualize business performance using Matplotlib.
- Develop machine learning models for predictive analytics.
- Build reproducible data processing and analysis workflows.

## Technologies

- Python 3.13
- SQLite
- Pandas and NumPy
- Matplotlib
- JupyterLab
- OpenPyXL
- Scikit-learn (planned)

## Dataset

**Source:** [UCI Machine Learning Repository — Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)

The dataset contains **541,909 transaction records** from a UK-based online retailer, covering December 2010 to December 2011.

The original dataset includes:

| Column | Description |
|---|---|
| InvoiceNo | Unique invoice identifier |
| StockCode | Product identifier |
| Description | Product description |
| Quantity | Number of items purchased or returned |
| InvoiceDate | Transaction date and time |
| UnitPrice | Product unit price in GBP |
| CustomerID | Customer identifier |
| Country | Customer country |

### Data quality considerations

The dataset contains missing values, cancelled transactions, negative quantities, and zero-price records.

Initial exploration identified:

- 135,080 records with missing customer IDs (24.93%).
- 1,454 records with missing product descriptions.
- 10,624 records with negative quantities.
- 9,288 records associated with invoice numbers beginning with `C`.

The database preserves the original transaction records, including cancellations and missing values, allowing different filtering strategies for subsequent analyses.

The raw dataset is excluded