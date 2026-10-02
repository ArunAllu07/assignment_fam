from src.aggregation import aggregate_monthly
from src.indicators import calculate_all_indicators
from src.utils import load_data, prepare_data, save_result, validate_outputs
from src.config import TICKERS
from src.utils import (
    load_data,
    prepare_data,
    save_result,
    validate_outputs
)


def process_ticker(df, ticker, output_dir):
    stock_df = df[
        df["ticker"] == ticker
    ].copy()

    stock_df = stock_df.set_index("date")

    monthly = aggregate_monthly(stock_df)

    monthly = calculate_all_indicators(
        monthly
    )

    monthly.insert(
        0,
        "ticker",
        ticker
    )

    save_result(
        monthly,
        ticker,
        output_dir
    )

    return monthly


def run_pipeline(input_file, output_dir):
    df = load_data(input_file)

    df = prepare_data(df)

    tickers = df["ticker"].unique()

    print(f"Total tickers: {len(tickers)}")
    print(f"Tickers: {list(tickers)}")

    for ticker in tickers:
        monthly = process_ticker(
            df,
            ticker,
            output_dir
        )

        print(
            f"{ticker} completed: "
            f"{len(monthly)} rows"
        )

    validation = validate_outputs(
        output_dir,
        tickers
    )

    print("\nValidation Results:")

    for ticker, passed in validation.items():
        status = "PASS" if passed else "FAIL"

        print(
            f"{ticker}: "
            f"{'24 rows' if passed else 'Invalid row count'} "
            f"- {status}"
        )

    return validation