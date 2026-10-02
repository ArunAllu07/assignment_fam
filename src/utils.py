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
    results = {}

    for ticker in tickers:
        file_path = os.path.join(
            output_dir,
            f"result_{ticker}.csv"
        )

        result = pd.read_csv(file_path)

        results[ticker] = (
            len(result) == 24
        )

    return results