import os
import joblib
import pandas as pd
import numpy as np
from .trainer import FEATURE_COLS, MODELS_DIR


def load_models(ticker: str):
    ticker = ticker.upper()
    clf_path = os.path.join(MODELS_DIR, f"{ticker}_classifier.joblib")
    reg_path = os.path.join(MODELS_DIR, f"{ticker}_regressor.joblib")
    scaler_path = os.path.join(MODELS_DIR, f"{ticker}_scaler.joblib")

    for path in [clf_path, reg_path, scaler_path]:
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Model file not found: {path}. Run the trainer first."
            )

    clf = joblib.load(clf_path)
    reg = joblib.load(reg_path)
    scaler = joblib.load(scaler_path)
    return clf, reg, scaler


def predict(ticker: str, df: pd.DataFrame) -> dict:
    """
    Run inference on the latest row of a feature-engineered DataFrame.

    Returns:
        {
            "ticker": "AAPL",
            "current_price": 182.45,
            "direction": "UP" | "DOWN",
            "predicted_next_close": 185.10,
            "confidence": 0.64
        }
    """
    clf, reg, scaler = load_models(ticker)

    latest = df[FEATURE_COLS].iloc[[-1]]
    latest_scaled = scaler.transform(latest)

    direction_prob = clf.predict_proba(latest_scaled)[0]
    direction_label = int(np.argmax(direction_prob))
    confidence = float(direction_prob[direction_label])

    predicted_price = float(reg.predict(latest_scaled)[0])
    current_price = float(df["Close"].iloc[-1])

    return {
        "ticker": ticker.upper(),
        "current_price": round(current_price, 2),
        "direction": "UP" if direction_label == 1 else "DOWN",
        "predicted_next_close": round(predicted_price, 2),
        "confidence": round(confidence, 4),
    }
