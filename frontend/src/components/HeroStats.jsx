import React from "react";
import { tokens, fontDisplay, fontBody, fontMono, strengthColor } from "../lib/tokens.js";

function StatBlock({ label, value, sub, accent }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
      <div style={{ fontFamily: fontMono, fontSize: 11, color: tokens.muted, letterSpacing: "0.06em" }}>
        {label}
      </div>
      <div
        style={{
          fontFamily: fontDisplay,
          fontSize: 34,
          fontWeight: 600,
          color: accent || tokens.text,
          lineHeight: 1,
        }}
      >
        {value}
      </div>
      {sub && <div style={{ fontFamily: fontBody, fontSize: 12.5, color: tokens.faint }}>{sub}</div>}
    </div>
  );
}

export default function HeroStats({ overall }) {
  return (
    <div
      style={{
        display: "flex",
        gap: 44,
        padding: "28px 32px",
        background: tokens.panel,
        border: `1px solid ${tokens.hairline}`,
        borderRadius: 12,
        marginBottom: 28,
        flexWrap: "wrap",
      }}
    >
      <StatBlock
        label="ACCEPTANCE RATE"
        value={`${overall.acceptanceRate}%`}
        sub={`${overall.acceptedAttempts} of ${overall.totalAttempts} attempts`}
        accent={strengthColor(overall.acceptanceRate)}
      />
      <div style={{ width: 1, background: tokens.hairline }} />
      <StatBlock label="SOLVED" value={overall.uniqueProblemsSolved} sub="unique problems" />
      <div style={{ width: 1, background: tokens.hairline }} />
      <StatBlock label="TOTAL ATTEMPTS" value={overall.totalAttempts} sub="all-time submissions" />
    </div>
  );
}
