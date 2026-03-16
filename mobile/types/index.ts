export interface OHLCVRow {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface StockDataResponse {
  ticker: string;
  rows: OHLCVRow[];
}

export interface PredictionResponse {
  ticker: string;
  current_price: number;
  direction: "UP" | "DOWN";
  predicted_next_close: number;
  confidence: number;
}

export interface SearchResult {
  ticker: string;
  name: string;
  supported: boolean;
}

export type RootStackParamList = {
  Home: undefined;
  Stock: { ticker: string; name: string };
};
