import os

import pandas as pd


def test_output_files():
    tickers = [
        "AAPL",
        "AMD",
        "AMZN",
        "AVGO",
        "CSCO",
        "MSFT",
        "NFLX",
        "PEP",
        "TMUS",
        "TSLA"
    ]

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

    for ticker in tickers:
        file_path = os.path.join(
            "output",
            f"result_{ticker}.csv"
        )

        assert os.path.exists(file_path)

        df = pd.read_csv(file_path)

        assert len(df) == 24
        assert list(df.columns) == expected_columns