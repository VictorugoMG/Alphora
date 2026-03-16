from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import yfinance as yf

from data.pipeline.pipeline import run_pipeline, SUPPORTED_TICKERS
from data.pipeline.fetcher import fetch_ohlcv
from ml.predictor import predict

router = APIRouter(prefix="/stocks", tags=["stocks"])


# --- Response Models ---

class OHLCVRow(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float


class StockDataResponse(BaseModel):
    ticker: str
    rows: list[OHLCVRow]


class PredictionResponse(BaseModel):
    ticker: str
    current_price: float
    direction: str
    predicted_next_close: float
    confidence: float


class SearchResult(BaseModel):
    ticker: str
    name: str
    supported: bool


# --- Routes ---

@router.get("/search", response_model=list[SearchResult])
def search_stocks(q: str = Query(..., min_length=1, max_length=10)):
    """
    Validate a ticker symbol and return basic info.
    """
    ticker = q.upper().strip()
    try:
        info = yf.Ticker(ticker).info
        name = info.get("longName") or info.get("shortName") or ticker
        if not info.get("regularMarketPrice") and not info.get("currentPrice"):
            raise ValueError("No market data")
    except Exception:
        raise HTTPException(status_code=404, detail=f"Ticker '{ticker}' not found.")

    return [SearchResult(
        ticker=ticker,
        name=name,
        supported=ticker in SUPPORTED_TICKERS,
    )]


@router.get("/{ticker}/data", response_model=StockDataResponse)
def get_stock_data(ticker: str, days: int = Query(default=90, ge=10, le=500)):
    """
    Return the last N days of OHLCV data for a ticker.
    """
    ticker = ticker.upper()
    try:
        df = fetch_ohlcv(ticker)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    df = df.tail(days).reset_index()
    rows = [
        OHLCVRow(
            date=str(row["Date"])[:10],
            open=round(row["Open"], 2),
            high=round(row["High"], 2),
            low=round(row["Low"], 2),
            close=round(row["Close"], 2),
            volume=round(row["Volume"], 2),
        )
        for _, row in df.iterrows()
    ]
    return StockDataResponse(ticker=ticker, rows=rows)


@router.get("/{ticker}/predict", response_model=PredictionResponse)
def get_prediction(ticker: str):
    """
    Return next-day direction and price prediction for a supported ticker.
    """
    ticker = ticker.upper()
    if ticker not in SUPPORTED_TICKERS:
        raise HTTPException(
            status_code=400,
            detail=f"'{ticker}' is not supported. Supported tickers: {SUPPORTED_TICKERS}",
        )
    try:
        df = run_pipeline(ticker)
        result = predict(ticker, df)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return PredictionResponse(**result)
