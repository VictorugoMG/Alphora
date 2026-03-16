import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  StyleSheet,
  SafeAreaView,
} from "react-native";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { RouteProp } from "@react-navigation/native";
import { RootStackParamList, OHLCVRow, PredictionResponse } from "../types";
import { getStockData, getPrediction } from "../services/api";
import StockChart from "../components/StockChart";
import PredictionCard from "../components/PredictionCard";

type Props = {
  navigation: NativeStackNavigationProp<RootStackParamList, "Stock">;
  route: RouteProp<RootStackParamList, "Stock">;
};

export default function StockScreen({ navigation, route }: Props) {
  const { ticker, name } = route.params;

  const [ohlcv, setOhlcv] = useState<OHLCVRow[]>([]);
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [loadingData, setLoadingData] = useState(true);
  const [loadingPrediction, setLoadingPrediction] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const stock = await getStockData(ticker);
        setOhlcv(stock.rows);
      } catch {
        setError("Failed to load stock data.");
      } finally {
        setLoadingData(false);
      }
    }
    load();
  }, [ticker]);

  async function handlePredict() {
    setLoadingPrediction(true);
    setError("");
    try {
      const result = await getPrediction(ticker);
      setPrediction(result);
    } catch {
      setError("Prediction unavailable for this ticker.");
    } finally {
      setLoadingPrediction(false);
    }
  }

  const latest = ohlcv[ohlcv.length - 1];

  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView style={styles.container} contentContainerStyle={styles.content}>

        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.back}>
          <Text style={styles.backText}>← Back</Text>
        </TouchableOpacity>

        <Text style={styles.ticker}>{ticker}</Text>
        <Text style={styles.name}>{name}</Text>

        {latest && (
          <View style={styles.priceRow}>
            <Text style={styles.price}>${latest.close.toFixed(2)}</Text>
            <Text style={styles.priceLabel}>Last Close</Text>
          </View>
        )}

        {loadingData ? (
          <ActivityIndicator color="#63b3ed" style={{ marginVertical: 40 }} />
        ) : (
          <StockChart data={ohlcv} ticker={ticker} />
        )}

        {!!error && <Text style={styles.error}>{error}</Text>}

        {!prediction && (
          <TouchableOpacity
            style={styles.predictBtn}
            onPress={handlePredict}
            disabled={loadingPrediction}
          >
            {loadingPrediction ? (
              <ActivityIndicator color="#12121f" />
            ) : (
              <Text style={styles.predictBtnText}>Get AI Prediction</Text>
            )}
          </TouchableOpacity>
        )}

        {prediction && <PredictionCard prediction={prediction} />}

      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#12121f" },
  container: { flex: 1 },
  content: { padding: 16, paddingBottom: 40 },
  back: { marginBottom: 16 },
  backText: { color: "#63b3ed", fontSize: 16 },
  ticker: { color: "#fff", fontSize: 36, fontWeight: "800" },
  name: { color: "#a0a0b0", fontSize: 14, marginBottom: 12 },
  priceRow: { flexDirection: "row", alignItems: "baseline", gap: 8, marginBottom: 4 },
  price: { color: "#fff", fontSize: 28, fontWeight: "700" },
  priceLabel: { color: "#a0a0b0", fontSize: 13 },
  error: { color: "#fc8181", textAlign: "center", marginVertical: 12 },
  predictBtn: {
    backgroundColor: "#63b3ed",
    borderRadius: 12,
    padding: 16,
    alignItems: "center",
    marginTop: 16,
  },
  predictBtnText: { color: "#12121f", fontSize: 16, fontWeight: "700" },
});
