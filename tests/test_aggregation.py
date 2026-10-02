import pandas as pd
from src.aggregation import aggregate_monthly

def test_monthly_aggregation():
    dates = pd.date_range("2020-01-01", periods=3, freq="D")

    data = pd.DataFrame({
        "open": [10, 11, 13],
        "high": [15, 20, 17],
        "low": [8, 7, 6],
        "close": [12, 18, 14],
        "adjclose": [12, 18, 14],
        "volume": [100, 200, 300]
    }, index=dates)

    result = aggregate_monthly(data)

    assert len(result) == 1
    assert result.iloc[0]["open"] == 10
    assert result.iloc[0]["high"] == 20
    assert result.iloc[0]["low"] == 6
    assert result.iloc[0]["close"] == 14