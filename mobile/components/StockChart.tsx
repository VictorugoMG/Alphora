import React from "react";
import { View, Text, StyleSheet, Dimensions } from "react-native";
import { LineChart } from "react-native-chart-kit";
import { OHLCVRow } from "../types";

interface Props {
  data: OHLCVRow[];
  ticker: string;
}

const SCREEN_WIDTH = Dimensions.get("window").width;

export default function StockChart({ data, ticker }: Props) {
  if (!data || data.length === 0) {
    return <Text style={styles.empty}>No chart data available.</Text>;
  }

  // Show last 30 data points to keep the chart readable
  const recent = data.slice(-30);
  const prices = recent.map((r) => parseFloat(r.close.toFixed(2)));

  // Label every 10th date
  const labels = recent.map((r, i) =>
    i % 10 === 0 ? r.date.slice(5) : ""
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{ticker} — Last 30 Days</Text>
      <LineChart
        data={{ labels, datasets: [{ data: prices }] }}
        width={SCREEN_WIDTH - 32}
        height={220}
        chartConfig={{
          backgroundColor: "#1e1e2e",
          backgroundGradientFrom: "#1e1e2e",
          backgroundGradientTo: "#1e1e2e",
          decimalPlaces: 2,
          color: (opacity = 1) => `rgba(99, 179, 237, ${opacity})`,
          labelColor: (opacity = 1) => `rgba(160, 160, 176, ${opacity})`,
          propsForDots: { r: "2" },
        }}
        bezier
        style={styles.chart}
        withInnerLines={false}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { marginVertical: 12 },
  title: {
    color: "#a0a0b0",
    fontSize: 13,
    textTransform: "uppercase",
    letterSpacing: 1,
    marginBottom: 8,
  },
  chart: { borderRadius: 12 },
  empty: { color: "#606070", textAlign: "center", marginVertical: 20 },
});
