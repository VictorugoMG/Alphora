import yfinance as yf
import pandas as pd


def fetch_ohlcv(ticker: str, period: str = "2y", interval: str = "1d") -> pd.DataFrame:
    """
    Download historical OHLCV data for a given ticker.

    Args:
        ticker:   Stock symbol (e.g. 'AAPL')
        period:   How far back to fetch ('1y', '2y', '5y', etc.)
        interval: Bar size ('1d' for daily end-of-day)

    Returns:
        DataFrame with columns: Open, High, Low, Close, Volume
    """
    raw = yf.download(ticker, period=period, interval=interval, auto_adjust=True, progress=False)

    if raw.empty:
        raise ValueError(f"No data returned for ticker '{ticker}'. Check the symbol and try again.")

    # Flatten MultiIndex columns if present (yfinance sometimes returns them)
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    df = raw[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.index.name = "Date"
    df.dropna(inplace=True)

    return df


if __name__ == "__main__":
    df = fetch_ohlcv("AAPL")
    print(df.tail())
    print(f"\nShape: {df.shape}")
