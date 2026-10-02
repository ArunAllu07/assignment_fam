import pandas as pd

from src.indicators import calculate_all_indicators


def test_indicator_columns():
    dates = pd.date_range(
        "2018-01-31",
        periods=24,
        freq="ME"
    )

    monthly = pd.DataFrame({
        "open": range(24),
        "high": range(1, 25),
        "low": range(24),
        "close": range(1, 25),
        "adjclose": range(1, 25),
        "volume": [1000] * 24
    }, index=dates)

    result = calculate_all_indicators(monthly)

    expected_columns = [
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

    for column in expected_columns:
        assert column in result.columns