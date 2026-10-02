from src.config import (
    SMA_WINDOWS,
    EMA_WINDOWS,
    DONCHIAN_WINDOW,
    BOLLINGER_WINDOW,
    BOLLINGER_MULTIPLIER,
    ZSCORE_WINDOW
)


def calculate_sma(monthly):
    for window in SMA_WINDOWS:
        monthly[f"SMA_{window}"] = (
            monthly["close"].rolling(window).mean()
        )

    return monthly


def calculate_ema(monthly):
    for window in EMA_WINDOWS:
        monthly[f"EMA_{window}"] = (
            monthly["close"]
            .ewm(span=window, adjust=False)
            .mean()
        )

    return monthly


def calculate_donchian(monthly):
    monthly["Donchian_Upper"] = (
        monthly["high"]
        .rolling(DONCHIAN_WINDOW)
        .max()
    )

    monthly["Donchian_Lower"] = (
        monthly["low"]
        .rolling(DONCHIAN_WINDOW)
        .min()
    )

    monthly["Donchian_Middle"] = (
        monthly["Donchian_Upper"]
        + monthly["Donchian_Lower"]
    ) / 2

    return monthly


def calculate_bollinger(monthly):
    middle = (
        monthly["close"]
        .rolling(BOLLINGER_WINDOW)
        .mean()
    )

    std = (
        monthly["close"]
        .rolling(BOLLINGER_WINDOW)
        .std()
    )

    monthly["BB_Middle"] = middle

    monthly["BB_Upper"] = (
        middle + BOLLINGER_MULTIPLIER * std
    )

    monthly["BB_Lower"] = (
        middle - BOLLINGER_MULTIPLIER * std
    )

    return monthly


def calculate_zscore(monthly):
    mean = (
        monthly["close"]
        .rolling(ZSCORE_WINDOW)
        .mean()
    )

    std = (
        monthly["close"]
        .rolling(ZSCORE_WINDOW)
        .std()
    )

    monthly["Z_Score"] = (
        monthly["close"] - mean
    ) / std

    return monthly


def calculate_all_indicators(monthly):
    monthly = calculate_sma(monthly)
    monthly = calculate_ema(monthly)
    monthly = calculate_donchian(monthly)
    monthly = calculate_bollinger(monthly)
    monthly = calculate_zscore(monthly)

    return monthly