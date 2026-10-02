import pandas as pd
import pytest
from src.indicators import calculate_all_indicators

def test_indicator_columns():
    dates = pd.date_range("2018-01-31", periods=24, freq="ME")

    monthly = pd.DataFrame({
        "open": range(1, 25),
        "high": range(2, 26),
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
        "BB_Middle",
        "BB_Upper",
        "BB_Lower",
        "Z_Score"
    ]

    for column in expected_columns:
        assert column in result.columns


def test_sma_10_value():
    dates = pd.date_range("2018-01-31", periods=10, freq="ME")

    monthly = pd.DataFrame({
        "open": range(1, 11),
        "high": range(2, 12),
        "low": range(10),
        "close": range(1, 11),
        "adjclose": range(1, 11),
        "volume": [1000] * 10
    }, index=dates)

    result = calculate_all_indicators(monthly)

    assert result.iloc[9]["SMA_10"] == pytest.approx(5.5)


def test_sma_20_value():
    dates = pd.date_range("2018-01-31", periods=20, freq="ME")

    monthly = pd.DataFrame({
        "open": range(1, 21),
        "high": range(2, 22),
        "low": range(20),
        "close": range(1, 21),
        "adjclose": range(1, 21),
        "volume": [1000] * 20
    }, index=dates)

    result = calculate_all_indicators(monthly)

    assert result.iloc[19]["SMA_20"] == pytest.approx(10.5)


def test_donchian_values():
    dates = pd.date_range("2018-01-31", periods=20, freq="ME")

    monthly = pd.DataFrame({
        "open": range(1, 21),
        "high": range(2, 22),
        "low": range(20),
        "close": range(1, 21),
        "adjclose": range(1, 21),
        "volume": [1000] * 20
    }, index=dates)

    result = calculate_all_indicators(monthly)

    assert result.iloc[19]["Donchian_Upper"] == 21
    assert result.iloc[19]["Donchian_Lower"] == 0


def test_bollinger_and_zscore():
    dates = pd.date_range("2018-01-31", periods=20, freq="ME")

    monthly = pd.DataFrame({
        "open": range(1, 21),
        "high": range(2, 22),
        "low": range(20),
        "close": range(1, 21),
        "adjclose": range(1, 21),
        "volume": [1000] * 20
    }, index=dates)

    result = calculate_all_indicators(monthly)

    expected_mean = 10.5
    expected_std = pd.Series(range(1, 21)).std()
    expected_upper = expected_mean + 2 * expected_std
    expected_lower = expected_mean - 2 * expected_std
    expected_zscore = (20 - expected_mean) / expected_std

    assert result.iloc[19]["BB_Middle"] == pytest.approx(expected_mean)
    assert result.iloc[19]["BB_Upper"] == pytest.approx(expected_upper)
    assert result.iloc[19]["BB_Lower"] == pytest.approx(expected_lower)
    assert result.iloc[19]["Z_Score"] == pytest.approx(expected_zscore)