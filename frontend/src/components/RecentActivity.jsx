import React from "react";
import { CircleCheck, CircleX, Circle, Activity } from "lucide-react";
import { tokens, fontBody, fontMono } from "../lib/tokens.js";

function statusIcon(status) {
  if (status === "Accepted") return <CircleCheck size={14} color={tokens.strong} />;
  if (status === "Wrong Answer") return <CircleX size={14} color={tokens.weak} />;
  return <Circle size={14} color={tokens.amber} />;
}

export default function RecentActivity({ submissions, lastSyncedLabel }) {
  return (
    <div>
      <div
        style={{
          background: tokens.panel,
          border: `1px solid ${tokens.hairline}`,
          borderRadius: 10,
          padding: "6px 18px",
        }}
      >
        {submissions.length === 0 && (
          <div style={{ padding: "18px 0", fontFamily: fontBody, fontSize: 13, color: tokens.faint }}>
            No recent submissions yet.
          </div>
        )}
        {submissions.map((s, i) => (
          <div
            key={`${s.title}-${i}`}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 10,
              padding: "12px 0",
              borderBottom: i < submissions.length - 1 ? `1px solid ${tokens.hairline}` : "none",
            }}
          >
            {statusIcon(s.status)}
            <div style={{ flex: 1, minWidth: 0 }}>
              <div
                style={{
                  fontFamily: fontBody,
                  fontSize: 13,
                  color: tokens.text,
                  whiteSpace: "nowrap",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                }}
              >
                {s.title}
              </div>
              <div style={{ fontFamily: fontMono, fontSize: 10.5, color: tokens.faint, marginTop: 2 }}>
                {s.topic}
              </div>
            </div>
            <div style={{ fontFamily: fontMono, fontSize: 10.5, color: tokens.faint, flexShrink: 0 }}>{s.when}</div>
          </div>
        ))}
      </div>

      {lastSyncedLabel && (
        <div
          style={{
            marginTop: 16,
            display: "flex",
            alignItems: "center",
            gap: 8,
            padding: "12px 16px",
            background: tokens.panelRaised,
            border: `1px dashed ${tokens.hairline}`,
            borderRadius: 8,
            fontFamily: fontBody,
            fontSize: 12,
            color: tokens.muted,
          }}
        >
          <Activity size={14} color={tokens.amber} />
          {lastSyncedLabel}
        </div>
      )}
    </div>
  );
}
