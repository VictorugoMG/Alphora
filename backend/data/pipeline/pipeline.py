from .fetcher import fetch_ohlcv
from .features import engineer_features
import pandas as pd

SUPPORTED_TICKERS = ["AAPL", "TSLA", "MSFT", "AMZN"]


def run_pipeline(ticker: str, period: str = "2y") -> pd.DataFrame:
    """
    Full data pipeline: fetch raw OHLCV data and engineer features.

    Args:
        ticker: Stock symbol
        period: How far back to fetch data

    Returns:
        DataFrame ready for model training or inference
    """
    if ticker.upper() not in SUPPORTED_TICKERS:
        raise ValueError(f"Ticker '{ticker}' not supported. Choose from {SUPPORTED_TICKERS}")

    df = fetch_ohlcv(ticker.upper(), period=period)
    df = engineer_features(df)
    return df


if __name__ == "__main__":
    for ticker in SUPPORTED_TICKERS:
        df = run_pipeline(ticker)
        print(f"{ticker}: {df.shape[0]} rows, {df.shape[1]} columns")
