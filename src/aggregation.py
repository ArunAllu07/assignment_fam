def aggregate_monthly(stock_df):
    stock_df = stock_df.sort_index()

    monthly = stock_df.resample("ME").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "adjclose": "last",
        "volume": "sum"
    })

    return monthly