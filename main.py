import pandas as pd
import os


def load_data(file_path):
    df = pd.read_csv(file_path)
    return df


def prepare_data(df):
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["ticker", "date"])
    return df


def aggregate_monthly(stock_df):
    stock_df = stock_df.set_index("date")

    monthly = stock_df.resample("ME").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last"
    })

    return monthly


def calculate_indicators(monthly):
    monthly["SMA_10"] = monthly["close"].rolling(10).mean()
    monthly["SMA_20"] = monthly["close"].rolling(20).mean()

    monthly["EMA_10"] = monthly["close"].ewm(
        span=10,
        adjust=False
    ).mean()

    monthly["EMA_20"] = monthly["close"].ewm(
        span=20,
        adjust=False
    ).mean()

    monthly["Donchian_Upper"] = monthly["high"].rolling(20).max()
    monthly["Donchian_Lower"] = monthly["low"].rolling(20).min()

    mid = monthly["close"].rolling(20).mean()
    sd = monthly["close"].rolling(20).std()

    monthly["BB_Middle"] = mid
    monthly["BB_Upper"] = mid + 2 * sd
    monthly["BB_Lower"] = mid - 2 * sd

    monthly["Z_Score"] = (monthly["close"] - mid) / sd

    return monthly


def save_result(monthly, ticker, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir,
        f"result_{ticker}.csv"
    )

    monthly.to_csv(output_file)


def validate_outputs(output_dir, tickers):
    print("\nValidation Results:")

    for ticker in tickers:
        file_path = os.path.join(
            output_dir,
            f"result_{ticker}.csv"
        )

        result = pd.read_csv(file_path)

        if len(result) == 24:
            print(f"{ticker}: {len(result)} rows - PASS")
        else:
            print(f"{ticker}: {len(result)} rows - FAIL")


def main():
    input_file = "data/output_file.csv"
    output_dir = "output"

    df = load_data(input_file)

    df = prepare_data(df)

    tickers = df["ticker"].unique()

    print(f"Total tickers: {len(tickers)}")
    print(f"Tickers: {list(tickers)}")

    for ticker in tickers:
        stock_df = df[df["ticker"] == ticker].copy()

        monthly = aggregate_monthly(stock_df)

        monthly = calculate_indicators(monthly)

        save_result(monthly, ticker, output_dir)

        print(f"{ticker} completed: {len(monthly)} rows")

    validate_outputs(output_dir, tickers)

    print("\nProcessing completed successfully.")


if __name__ == "__main__":
    main()