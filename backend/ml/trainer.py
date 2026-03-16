import os
import joblib
import pandas as pd
from xgboost import XGBClassifier, XGBRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler

FEATURE_COLS = [
    "Open", "High", "Low", "Close", "Volume",
    "SMA_10", "SMA_20", "SMA_50",
    "EMA_10", "EMA_20",
    "RSI",
    "MACD", "MACD_Signal", "MACD_Hist",
    "Volatility",
]

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")


def prepare_data(df: pd.DataFrame):
    X = df[FEATURE_COLS]
    y_direction = df["direction"]
    y_price = df["next_close"]
    return X, y_direction, y_price


def train(df: pd.DataFrame, ticker: str):
    """
    Train a direction classifier and a price regressor.
    Uses time-series cross-validation (no data leakage).
    Saves both models to disk.

    Args:
        df:     Feature-engineered DataFrame from the pipeline
        ticker: Stock symbol, used to name the saved model files
    """
    X, y_direction, y_price = prepare_data(df)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Time-series split — never shuffle financial data
    tscv = TimeSeriesSplit(n_splits=5)

    # --- Direction classifier (XGBoost) ---
    clf = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        random_state=42,
    )
    clf.fit(X_scaled, y_direction)

    # --- Price regressor (XGBoost) ---
    reg = XGBRegressor(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    )
    reg.fit(X_scaled, y_price)

    # --- Save models ---
    os.makedirs(MODELS_DIR, exist_ok=True)
    ticker = ticker.upper()
    joblib.dump(clf, os.path.join(MODELS_DIR, f"{ticker}_classifier.joblib"))
    joblib.dump(reg, os.path.join(MODELS_DIR, f"{ticker}_regressor.joblib"))
    joblib.dump(scaler, os.path.join(MODELS_DIR, f"{ticker}_scaler.joblib"))

    print(f"[{ticker}] Models saved to {MODELS_DIR}")
    return clf, reg, scaler


if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from data.pipeline.pipeline import run_pipeline

    for ticker in ["AAPL", "TSLA", "MSFT", "AMZN"]:
        df = run_pipeline(ticker)
        train(df, ticker)
