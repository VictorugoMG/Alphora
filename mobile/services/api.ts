import axios from "axios";
import { PredictionResponse, SearchResult, StockDataResponse } from "../types";

// Use your machine's local IP so physical devices can reach the API.
// For emulators: Android uses 10.0.2.2, iOS simulator uses localhost.
// Android emulator uses 10.0.2.2 to reach host machine localhost
const BASE_URL = "http://10.0.2.2:8000";

const client = axios.create({ baseURL: BASE_URL, timeout: 15000 });

export async function searchStock(query: string): Promise<SearchResult[]> {
  const { data } = await client.get<SearchResult[]>("/stocks/search", {
    params: { q: query },
  });
  return data;
}

export async function getStockData(
  ticker: string,
  days: number = 90
): Promise<StockDataResponse> {
  const { data } = await client.get<StockDataResponse>(
    `/stocks/${ticker}/data`,
    { params: { days } }
  );
  return data;
}

export async function getPrediction(
  ticker: string
): Promise<PredictionResponse> {
  const { data } = await client.get<PredictionResponse>(
    `/stocks/${ticker}/predict`
  );
  return data;
}
