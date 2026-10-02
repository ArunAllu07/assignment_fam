import pandas as pd

from src.aggregation import aggregate_monthly


def test_monthly_aggregation():
    dates = pd.date_range(
        "2020-01-01",
        periods=40,
        freq="D"
    )

    data = pd.DataFrame({
        "open": range(40),
        "high": range(1, 41),
        "low": range(40),
        "close": range(1, 41),
        "adjclose": range(1, 41),
        "volume": [100] * 40
    }, index=dates)

    result = aggregate_monthly(data)

    assert len(result) >= 1
    assert "open" in result.columns
    assert "high" in result.columns
    assert "low" in result.columns
    assert "close" in result.columns
    assert "adjclose" in result.columns
    assert "volume" in result.columns