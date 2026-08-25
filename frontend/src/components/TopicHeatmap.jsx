import React, { useMemo } from "react";
import { tokens, fontBody, fontMono, strengthColor } from "../lib/tokens.js";

function TopicRow({ item }) {
  const color = strengthColor(item.acceptanceRate);
  const widthPct = Math.max(6, Math.min(100, item.acceptanceRate));

  return (
    <div style={{ display: "flex", alignItems: "center", gap: 14, padding: "9px 0" }}>
      <div
        style={{
          width: 168,
          fontFamily: fontBody,
          fontSize: 13.5,
          color: tokens.text,
          fontWeight: 500,
          flexShrink: 0,
        }}
      >
        {item.topic}
      </div>
      <div
        style={{
          flex: 1,
          position: "relative",
          height: 20,
          background: tokens.ink,
          borderRadius: 3,
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${widthPct}%`,
            height: "100%",
            background: color,
            borderRadius: 3,
            transition: "width 0.4s ease",
          }}
        />
      </div>
      <div
        style={{
          width: 52,
          textAlign: "right",
          fontFamily: fontMono,
          fontSize: 13,
          color,
          fontWeight: 600,
          flexShrink: 0,
        }}
      >
        {item.acceptanceRate.toFixed(1)}%
      </div>
      <div
        style={{
          width: 70,
          textAlign: "right",
          fontFamily: fontMono,
          fontSize: 11.5,
          color: tokens.faint,
          flexShrink: 0,
        }}
      >
        {item.totalAttempts} att.
      </div>
    </div>
  );
}

// Topics are always displayed weakest-first, mirroring the backend's
// WeaknessDetector ordering, regardless of the order the API returns them in.
export default function TopicHeatmap({ topics }) {
  const sorted = useMemo(
    () => [...topics].sort((a, b) => a.acceptanceRate - b.acceptanceRate),
    [topics]
  );

  return (
    <div
      style={{
        background: tokens.panel,
        border: `1px solid ${tokens.hairline}`,
        borderRadius: 10,
        padding: "8px 22px",
      }}
    >
      {sorted.map((t, i) => (
        <div key={t.topic} style={{ borderBottom: i < sorted.length - 1 ? `1px solid ${tokens.hairline}` : "none" }}>
          <TopicRow item={t} />
        </div>
      ))}
    </div>
  );
}
