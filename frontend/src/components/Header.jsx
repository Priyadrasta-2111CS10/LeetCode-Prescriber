import React from "react";
import { ClipboardList, Flame } from "lucide-react";
import { tokens, fontDisplay, fontMono } from "../lib/tokens.js";

export default function Header({ username, streakDays }) {
  return (
    <div
      style={{
        borderBottom: `1px solid ${tokens.hairline}`,
        padding: "22px 32px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <ClipboardList size={18} color={tokens.amber} />
        <span style={{ fontFamily: fontDisplay, fontSize: 19, fontWeight: 600, color: tokens.text }}>
          The Prescriber
        </span>
      </div>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 8,
          fontFamily: fontMono,
          fontSize: 12.5,
          color: tokens.muted,
        }}
      >
        <span>@{username}</span>
        {streakDays != null && (
          <>
            <span style={{ color: tokens.hairline }}>•</span>
            <Flame size={13} color={tokens.amber} />
            <span>{streakDays}d streak</span>
          </>
        )}
      </div>
    </div>
  );
}
