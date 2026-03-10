import pandas as pd
import numpy as np


def add_sma(df: pd.DataFrame, windows: list[int] = [10, 20, 50]) -> pd.DataFrame:
    for w in windows:
        df[f"SMA_{w}"] = df["Close"].rolling(window=w).mean()
    return df


def add_ema(df: pd.DataFrame, windows: list[int] = [10, 20]) -> pd.DataFrame:
    for w in windows:
        df[f"EMA_{w}"] = df["Close"].ewm(span=w, adjust=False).mean()
    return df


def add_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=window - 1, min_periods=window).mean()
    avg_loss = loss.ewm(com=window - 1, min_periods=window).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))
    return df


def add_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    ema_fast = df["Close"].ewm(span=fast, adjust=False).mean()
    ema_slow = df["Close"].ewm(span=slow, adjust=False).mean()
    df["MACD"] = ema_fast - ema_slow
    df["MACD_Signal"] = df["MACD"].ewm(span=signal, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]
    return df


def add_volatility(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    df["Volatility"] = df["Close"].pct_change().rolling(window=window).std()
    return df


def add_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the prediction target:
      - direction: 1 if next day close > today close, else 0
      - next_close: next day closing price
    """
    df["next_close"] = df["Close"].shift(-1)
    df["direction"] = (df["next_close"] > df["Close"]).astype(int)
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all feature engineering steps and return a clean DataFrame."""
    df = df.copy()
    df = add_sma(df)
    df = add_ema(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_volatility(df)
    df = add_target(df)

    # Drop rows with NaN (from rolling windows and the last row which has no next_close)
    df.dropna(inplace=True)

    return df


if __name__ == "__main__":
    from fetcher import fetch_ohlcv
    df = fetch_ohlcv("AAPL")
    df = engineer_features(df)
    print(df.tail())
    print(f"\nColumns: {list(df.columns)}")
    print(f"Shape: {df.shape}")
