
"""Analyze and forecast daily gross retail sales."""

from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import TimeSeriesSplit


DB_PATH = Path("retail_real.db")
FIGURE_PATH = Path("results/figures/daily_sales_forecast.png")

FEATURES = ["lag_1", "weekday", "month"]


def load_daily_sales():
    """Load daily gross sales from SQLite."""

    query = """
    SELECT
        date(i.invoice_date) AS day,
        SUM(it.quantity * it.unit_price) AS gross_sales
    FROM invoices AS i
    JOIN invoice_items AS it
        ON i.invoice_no = it.invoice_no
    WHERE it.quantity > 0
      AND it.unit_price > 0
      AND it.invoice_no NOT LIKE 'C%'
    GROUP BY day
    ORDER BY day ASC;
    """

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn)

    df["day"] = pd.to_datetime(df["day"])
    return df.set_index("day").sort_index()


def prepare_features(df):
    """Prepare sales-day observations and calendar features."""

    df = df.loc["2011-01-01":"2011-11-30"].copy()

    df["weekday"] = df.index.dayofweek
    df["month"] = df.index.month

    # Previous recorded-sales day, not previous calendar day.
    df["lag_1"] = df["gross_sales"].shift(1)

    return df.dropna(subset=["lag_1"])


def calculate_metrics(actual, predicted):
    """Return MAE and RMSE."""

    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))

    return mae, rmse


def compare_models_cv(train):
    """Compare weekday encodings using time-series CV."""

    encoded = pd.get_dummies(
        train,
        columns=["weekday"],
        drop_first=True,
        dtype=int,
    )

    weekday_features = [
        col for col in encoded.columns
        if col.startswith("weekday_")
    ]

    onehot_features = ["lag_1", "month"] + weekday_features

    models = {
        "linear": train[FEATURES],
        "onehot": encoded[onehot_features],
    }

    y = train["gross_sales"]
    tscv = TimeSeriesSplit(n_splits=5)

    results = []

    for fold, (train_idx, val_idx) in enumerate(
        tscv.split(train), start=1
    ):
        row = {"fold": fold}

        for name, X in models.items():
            model = LinearRegression()

            model.fit(
                X.iloc[train_idx],
                y.iloc[train_idx],
            )

            predictions = model.predict(
                X.iloc[val_idx]
            )

            row[name] = mean_absolute_error(
                y.iloc[val_idx],
                predictions,
            )

        results.append(row)

    results_df = pd.DataFrame(results)

    print("\nCross-validation results:")
    print(results_df.round(2))

    print("\nMean cross-validation MAE:")
    print(results_df[["linear", "onehot"]].mean().round(2))

    return results_df


def plot_predictions(test, predictions):
    """Save actual versus predicted daily sales."""

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        test.index,
        test["gross_sales"],
        label="Actual sales",
        color="black",
        linewidth=1.5,
    )

    ax.plot(
        test.index,
        predictions,
        label="Linear Regression prediction",
        color="red",
        linewidth=1.5,
    )

    ax.set_title("Daily Retail Sales: Actual vs Predicted")
    ax.set_xlabel("Date")
    ax.set_ylabel("Gross sales (£)")

    ax.legend()
    ax.grid(alpha=0.3)

    fig.autofmt_xdate()
    fig.tight_layout()

    FIGURE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig.savefig(FIGURE_PATH, dpi=300)
    plt.close(fig)

    print(f"\nFigure saved to: {FIGURE_PATH}")


def main():
    df = load_daily_sales()
    df_model = prepare_features(df)

    # Chronological train/test split.
    split_idx = int(len(df_model) * 0.8)

    train = df_model.iloc[:split_idx].copy()
    test = df_model.iloc[split_idx:].copy()

    print(f"Training observations: {len(train)}")
    print(f"Test observations: {len(test)}")

    print(
        f"Training period: {train.index.min().date()} "
        f"to {train.index.max().date()}"
    )

    print(
        f"Test period: {test.index.min().date()} "
        f"to {test.index.max().date()}"
    )

    # Baseline: previous recorded-sales day's revenue.
    baseline_predictions = test["lag_1"]

    baseline_mae, baseline_rmse = calculate_metrics(
        test["gross_sales"],
        baseline_predictions,
    )

    print(f"\nBaseline MAE: £{baseline_mae:,.2f}")
    print(f"Baseline RMSE: £{baseline_rmse:,.2f}")

    # Compare feature representations on training data.
    compare_models_cv(train)

    # Selected model: numerical weekday encoding.
    model = LinearRegression()

    model.fit(
        train[FEATURES],
        train["gross_sales"],
    )

    predictions = model.predict(test[FEATURES])

    mae, rmse = calculate_metrics(
        test["gross_sales"],
        predictions,
    )

    print(f"\nLinear Regression MAE: £{mae:,.2f}")
    print(f"Linear Regression RMSE: £{rmse:,.2f}")

    improvement = 100 * (baseline_mae - mae) / baseline_mae

    print(f"MAE improvement over baseline: {improvement:.1f}%")

    print(f"\nIntercept: {model.intercept_:,.2f}")

    for feature, coefficient in zip(
        FEATURES, model.coef_
    ):
        print(f"{feature}: {coefficient:,.4f}")

    plot_predictions(test, predictions)


if __name__ == "__main__":
    main()
