import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBClassifier
from .trainer import FEATURE_COLS, prepare_data


def evaluate(df: pd.DataFrame, ticker: str, n_splits: int = 5) -> dict:
    """
    Evaluate direction classifier using walk-forward time-series cross-validation.
    Prints a summary and returns metrics as a dict.
    """
    X, y_direction, _ = prepare_data(df)
    X = X.values

    tscv = TimeSeriesSplit(n_splits=n_splits)
    all_preds = []
    all_true = []

    for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y_direction.iloc[train_idx], y_direction.iloc[test_idx]

        clf = XGBClassifier(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss",
            random_state=42,
        )
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)

        all_preds.extend(preds)
        all_true.extend(y_test)

    accuracy = accuracy_score(all_true, all_preds)
    precision = precision_score(all_true, all_preds, zero_division=0)
    recall = recall_score(all_true, all_preds, zero_division=0)
    f1 = f1_score(all_true, all_preds, zero_division=0)
    cm = confusion_matrix(all_true, all_preds)

    print(f"\n=== Evaluation: {ticker.upper()} ===")
    print(f"  Accuracy : {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall   : {recall:.4f}")
    print(f"  F1 Score : {f1:.4f}")
    print(f"  Confusion Matrix:\n{cm}")

    return {
        "ticker": ticker.upper(),
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }


if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from data.pipeline.pipeline import run_pipeline

    for ticker in ["AAPL", "TSLA", "MSFT", "AMZN"]:
        df = run_pipeline(ticker)
        evaluate(df, ticker)
