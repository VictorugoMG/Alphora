import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  ActivityIndicator,
  StyleSheet,
  SafeAreaView,
} from "react-native";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { RootStackParamList, SearchResult } from "../types";
import { searchStock } from "../services/api";

type Props = {
  navigation: NativeStackNavigationProp<RootStackParamList, "Home">;
};

const QUICK_PICKS = ["AAPL", "TSLA", "MSFT", "AMZN"];

export default function HomeScreen({ navigation }: Props) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSearch(ticker?: string) {
    const q = (ticker ?? query).trim().toUpperCase();
    if (!q) return;
    setLoading(true);
    setError("");
    try {
      const data = await searchStock(q);
      setResults(data);
    } catch {
      setError("Ticker not found. Try AAPL, TSLA, MSFT, or AMZN.");
      setResults([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <SafeAreaView style={styles.safe}>
      <View style={styles.container}>
        <Text style={styles.title}>Alphora</Text>
        <Text style={styles.subtitle}>Stock Market Predictions</Text>

        <View style={styles.searchRow}>
          <TextInput
            style={styles.input}
            placeholder="Search ticker (e.g. AAPL)"
            placeholderTextColor="#606070"
            value={query}
            onChangeText={setQuery}
            autoCapitalize="characters"
            onSubmitEditing={() => handleSearch()}
          />
          <TouchableOpacity style={styles.searchBtn} onPress={() => handleSearch()}>
            <Text style={styles.searchBtnText}>Go</Text>
          </TouchableOpacity>
        </View>

        <Text style={styles.sectionLabel}>Quick Picks</Text>
        <View style={styles.quickPicks}>
          {QUICK_PICKS.map((t) => (
            <TouchableOpacity
              key={t}
              style={styles.chip}
              onPress={() => handleSearch(t)}
            >
              <Text style={styles.chipText}>{t}</Text>
            </TouchableOpacity>
          ))}
        </View>

        {loading && <ActivityIndicator color="#63b3ed" style={{ marginTop: 24 }} />}
        {!!error && <Text style={styles.error}>{error}</Text>}

        <FlatList
          data={results}
          keyExtractor={(item) => item.ticker}
          renderItem={({ item }) => (
            <TouchableOpacity
              style={styles.resultRow}
              onPress={() =>
                navigation.navigate("Stock", {
                  ticker: item.ticker,
                  name: item.name,
                })
              }
            >
              <View>
                <Text style={styles.resultTicker}>{item.ticker}</Text>
                <Text style={styles.resultName}>{item.name}</Text>
              </View>
              {item.supported && (
                <View style={styles.supportedBadge}>
                  <Text style={styles.supportedText}>AI Ready</Text>
                </View>
              )}
            </TouchableOpacity>
          )}
        />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#12121f" },
  container: { flex: 1, padding: 16 },
  title: { color: "#fff", fontSize: 32, fontWeight: "800", marginTop: 16 },
  subtitle: { color: "#a0a0b0", fontSize: 14, marginBottom: 24 },
  searchRow: { flexDirection: "row", gap: 8, marginBottom: 20 },
  input: {
    flex: 1,
    backgroundColor: "#1e1e2e",
    color: "#fff",
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 16,
  },
  searchBtn: {
    backgroundColor: "#63b3ed",
    borderRadius: 10,
    paddingHorizontal: 20,
    justifyContent: "center",
  },
  searchBtnText: { color: "#12121f", fontWeight: "700", fontSize: 16 },
  sectionLabel: { color: "#a0a0b0", fontSize: 12, letterSpacing: 1, marginBottom: 10 },
  quickPicks: { flexDirection: "row", gap: 8, marginBottom: 24 },
  chip: {
    backgroundColor: "#1e1e2e",
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  chipText: { color: "#63b3ed", fontWeight: "600" },
  error: { color: "#fc8181", textAlign: "center", marginTop: 16 },
  resultRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#1e1e2e",
    borderRadius: 12,
    padding: 16,
    marginBottom: 10,
  },
  resultTicker: { color: "#fff", fontSize: 17, fontWeight: "700" },
  resultName: { color: "#a0a0b0", fontSize: 13, marginTop: 2 },
  supportedBadge: {
    backgroundColor: "#1a3a4a",
    borderRadius: 6,
    paddingHorizontal: 10,
    paddingVertical: 4,
  },
  supportedText: { color: "#63b3ed", fontSize: 12, fontWeight: "600" },
});
