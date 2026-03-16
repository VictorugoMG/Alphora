import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { PredictionResponse } from "../types";

interface Props {
  prediction: PredictionResponse;
}

export default function PredictionCard({ prediction }: Props) {
  const isUp = prediction.direction === "UP";
  const confidencePct = Math.round(prediction.confidence * 100);

  return (
    <View style={styles.card}>
      <Text style={styles.label}>AI Prediction</Text>

      <View style={[styles.directionBadge, isUp ? styles.up : styles.down]}>
        <Text style={styles.directionText}>
          {isUp ? "▲ UP" : "▼ DOWN"}
        </Text>
      </View>

      <View style={styles.row}>
        <View style={styles.col}>
          <Text style={styles.metaLabel}>Current Price</Text>
          <Text style={styles.metaValue}>${prediction.current_price}</Text>
        </View>
        <View style={styles.col}>
          <Text style={styles.metaLabel}>Predicted Close</Text>
          <Text style={styles.metaValue}>${prediction.predicted_next_close}</Text>
        </View>
        <View style={styles.col}>
          <Text style={styles.metaLabel}>Confidence</Text>
          <Text style={styles.metaValue}>{confidencePct}%</Text>
        </View>
      </View>

      <Text style={styles.disclaimer}>
        For educational purposes only. Not financial advice.
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: "#1e1e2e",
    borderRadius: 16,
    padding: 20,
    marginVertical: 12,
  },
  label: {
    color: "#a0a0b0",
    fontSize: 13,
    marginBottom: 12,
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  directionBadge: {
    borderRadius: 8,
    paddingVertical: 10,
    alignItems: "center",
    marginBottom: 16,
  },
  up: { backgroundColor: "#1a4731" },
  down: { backgroundColor: "#4a1a1a" },
  directionText: {
    fontSize: 22,
    fontWeight: "700",
    color: "#fff",
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 14,
  },
  col: { alignItems: "center" },
  metaLabel: { color: "#a0a0b0", fontSize: 11, marginBottom: 4 },
  metaValue: { color: "#fff", fontSize: 15, fontWeight: "600" },
  disclaimer: {
    color: "#606070",
    fontSize: 11,
    textAlign: "center",
  },
});
