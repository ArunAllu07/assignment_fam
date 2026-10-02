import os
import pandas as pd


def load_data(file_path):
    return pd.read_csv(file_path)


def prepare_data(df):
    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values(
        ["ticker", "date"]
    )

    return df


def save_result(monthly, ticker, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir,
        f"result_{ticker}.csv"
    )

    monthly.to_csv(output_file)


def validate_outputs(output_dir, tickers):
    expected_columns = [
        "date",
        "ticker",
        "open",
        "high",
        "low",
        "close",
        "adjclose",
        "volume",
        "SMA_10",
        "SMA_20",
        "EMA_10",
        "EMA_20",
        "Donchian_Upper",
        "Donchian_Lower",
        "Donchian_Middle", 
        "BB_Middle",
        "BB_Upper",
        "BB_Lower",
        "Z_Score"
    ]

    results = {}

    for ticker in tickers:
        file_path = os.path.join(
            output_dir,
            f"result_{ticker}.csv"
        )

        if not os.path.exists(file_path):
            results[ticker] = False
            continue

        result = pd.read_csv(file_path)

        valid = True

        if len(result) != 24:
            valid = False

        if list(result.columns) != expected_columns:
            valid = False

        if not all(result["ticker"] == ticker):
            valid = False

        dates = pd.to_datetime(result["date"])

        if dates.duplicated().any():
            valid = False

        if not dates.is_monotonic_increasing:
            valid = False

        results[ticker] = valid

    return results