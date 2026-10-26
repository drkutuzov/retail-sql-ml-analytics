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

The raw dataset is excluded from Git version control.

## Database schema

The original flat dataset is transformed into a relational SQLite database containing three tables.

### 1. `customers`

Stores unique customer identifiers.

| Column | Type | Constraint |
|---|---|---|
| customer_id | INTEGER | Primary key |

### 2. `invoices`

Stores invoice-level information.

| Column | Type | Constraint |
|---|---|---|
| invoice_no | TEXT | Primary key |
| invoice_date | TEXT | NOT NULL |
| customer_id | INTEGER | Foreign key, nullable |
| country | TEXT | NOT NULL |

Each invoice references a customer when the customer ID is available. For invoices with missing customer information, `customer_id` is stored as `NULL`.

The earliest recorded timestamp is used as the invoice-level date when multiple timestamps occur within the same invoice.

### 3. `invoice_items`

Stores individual transaction lines.

| Column | Type | Constraint |
|---|---|---|
| item_id | INTEGER | Primary key |
| invoice_no | TEXT | Foreign key, NOT NULL |
| invoice_date | TEXT | NOT NULL |
| stock_code | TEXT | NOT NULL |
| description | TEXT | Nullable |
| quantity | INTEGER | NOT NULL |
| unit_price | REAL | NOT NULL |

Each invoice can contain multiple invoice items. The original row-level timestamp is preserved.

### Relationships

```text
customers
    |
    | 1-to-many
    v
invoices
    |
    | 1-to-many
    v
invoice_items
```

The database uses foreign-key constraints to maintain referential integrity.

### Database statistics

| Table | Records |
|---|---:|
| customers | 4,372 |
| invoices | 25,900 |
| invoice_items | 541,909 |

The import pipeline has been tested successfully, including foreign-key validation and protection against importing into an already populated database.

## Project structure

```text
retail-sql-ml-analytics/
├── data/
│   └── raw/
│       └── Online Retail.xlsx
├── src/
│   ├── create_database.py
│   ├── insert_data.py
│   ├── insert_real_data.py
│   ├── explore_data.py
│   └── query_database.py
├── README.md
├── requirements.txt
├── .gitignore
└── retail_real.db
```

The raw dataset, generated databases, virtual environment, and temporary notebooks are excluded from Git version control.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/drkutuzov/retail-sql-ml-analytics.git
cd retail-sql-ml-analytics
```

### 2. Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, activate the environment using:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the dataset

Download the Online Retail dataset from the [UCI repository](https://archive.ics.uci.edu/dataset/352/online+retail).

Extract and place the Excel file at:

```text
data/raw/Online Retail.xlsx
```

## Running the data pipeline

Run the commands from the project root directory.

### Step 1 — Create the SQLite database

```bash
python src/create_database.py
```

This creates `retail_real.db` and initializes the three relational tables.

### Step 2 — Import transaction data

```bash
python src/insert_real_data.py
```

The import script:

1. Loads the original Excel dataset.
2. Extracts unique customer records.
3. Aggregates invoice-level information.
4. Preserves individual transaction lines.
5. Inserts data in foreign-key dependency order.
6. Uses a transaction with rollback on failure.
7. Rejects imports into a nonempty database.

Expected output:

```text
Import completed successfully.
Customers: 4372
Invoices: 25900
Invoice items: 541909
```

The import requires an empty database. To rebuild the database from scratch, use a new database file or deliberately remove the generated database before recreating it. Do not remove databases containing data you need to retain.

### Step 3 — Verify database integrity

```bash
sqlite3 retail_real.db "PRAGMA foreign_key_check;"
```

An empty result indicates that SQLite found no foreign-key violations.

## SQL analytics

The project uses SQL to calculate transaction-level and aggregated business metrics.

### Total transaction revenue

Including cancellations and returns:

```sql
SELECT SUM(quantity * unit_price) AS total_revenue
FROM invoice_items;
```

Result:

**£9,747,747.934**

### Gross sales excluding cancellations

```sql
SELECT SUM(quantity * unit_price) AS gross_sales
FROM invoice_items
WHERE quantity > 0
  AND unit_price > 0
  AND invoice_no NOT LIKE 'C%';
```

Expected result from the equivalent Pandas analysis:

**£10,666,684.544**

The distinction between total transaction revenue and gross sales is important because cancellations and returns contribute negative quantities to the original data.

## Current progress

**Completed**

- Initial exploratory data analysis.
- Investigation of missing values and cancelled invoices.
- Revenue analysis using Pandas.
- Monthly and daily revenue exploration.
- Relational database design.
- SQLite database creation.
- Import of customers, invoices, and invoice items.
- Transaction handling and duplicate-import protection.
- Foreign-key integrity validation.
- Comparison of SQL and Pandas total revenue calculations.

**Planned**

- Advanced SQL joins and aggregations.
- Customer-level purchasing analysis.
- Revenue analysis by country and product.
- SQL integration with Python and Pandas.
- Automated data validation and tests.
- Time-series feature engineering.
- Revenue forecasting with machine learning.
- Model evaluation and visualization.

## Reproducibility

The project is designed to separate source code from raw data and generated outputs.

Database creation and import scripts can reproduce the SQLite database from the original Excel dataset. Database constraints and transaction handling support consistent and reliable data ingestion.

Python dependencies are specified in `requirements.txt`.

## Project status

**In active development.**

The database ingestion pipeline is implemented and tested. SQL analytics and predictive modeling are being developed incrementally.

## Data attribution

The Online Retail dataset is provided by the UCI Machine Learning Repository.

[UCI Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail)