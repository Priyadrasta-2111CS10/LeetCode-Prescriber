import React from "react";
import { tokens, fontDisplay, fontMono } from "../lib/tokens.js";

// d matches DifficultyStatsResponse: { difficulty, totalAttempts,
// acceptedAttempts, uniqueProblemsSolved, acceptanceRate }. There's no
// "total problems available at this difficulty" in the data, so the ring
// reflects acceptanceRate (accepted / attempted) rather than a
// solved-vs-catalog-size fraction.
export default function DifficultyDial({ d }) {
  const pct = d.acceptanceRate || 0;
  const color =
    d.difficulty === "Easy" ? tokens.strong : d.difficulty === "Medium" ? tokens.amber : tokens.weak;
  const r = 34;
  const c = 2 * Math.PI * r;

  return (
    <div
      style={{
        background: tokens.panelRaised,
        border: `1px solid ${tokens.hairline}`,
        borderRadius: 8,
        padding: "18px 16px",
        display: "flex",
        alignItems: "center",
        gap: 16,
        flex: 1,
        minWidth: 220,
      }}
    >
      <svg width="80" height="80" style={{ transform: "rotate(-90deg)", flexShrink: 0 }}>
        <circle cx="40" cy="40" r={r} fill="none" stroke={tokens.ink} strokeWidth="7" />
        <circle
          cx="40"
          cy="40"
          r={r}
          fill="none"
          stroke={color}
          strokeWidth="7"
          strokeDasharray={c}
          strokeDashoffset={c - (pct / 100) * c}
          strokeLinecap="round"
          style={{ transition: "stroke-dashoffset 0.5s ease" }}
        />
      </svg>
      <div>
        <div
          style={{ fontFamily: fontMono, fontSize: 11, color: tokens.muted, letterSpacing: "0.06em", marginBottom: 3 }}
        >
          {d.difficulty.toUpperCase()}
        </div>
        <div style={{ fontFamily: fontDisplay, fontSize: 22, fontWeight: 600, color: tokens.text, lineHeight: 1.1 }}>
          {d.uniqueProblemsSolved}
          <span style={{ fontSize: 14, color: tokens.faint, fontFamily: fontMono }}> solved</span>
        </div>
        <div style={{ fontFamily: fontMono, fontSize: 11.5, color, marginTop: 2 }}>
          {(d.acceptanceRate ?? 0).toFixed(1)}% AC · {d.totalAttempts} att.
        </div>
      </div>
    </div>
  );
}
