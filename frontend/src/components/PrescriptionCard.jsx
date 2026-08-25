import React from "react";
import { Stethoscope, ChevronRight } from "lucide-react";
import { tokens, fontDisplay, fontBody, fontMono, strengthColor } from "../lib/tokens.js";

function PerforatedTop() {
  const dots = new Array(28).fill(0);
  return (
    <div style={{ display: "flex", justifyContent: "space-between", padding: "0 10px", marginBottom: -1 }}>
      {dots.map((_, i) => (
        <div
          key={i}
          style={{
            width: 5,
            height: 5,
            borderRadius: "50%",
            background: tokens.ink,
            border: `1px solid ${tokens.hairline}`,
          }}
        />
      ))}
    </div>
  );
}

export default function PrescriptionCard({ item }) {
  // Defensive fallback: if acceptanceRate is ever missing/undefined for
  // any reason (topic name mismatch upstream, different API shape,
  // etc.), degrade to "—" instead of crashing the whole page on
  // undefined.toFixed().
  const hasRate = typeof item.acceptanceRate === "number" && !Number.isNaN(item.acceptanceRate);

  return (
    <div
      style={{
        background: tokens.panel,
        border: `1px solid ${tokens.hairline}`,
        borderRadius: 10,
        overflow: "hidden",
      }}
    >
      <PerforatedTop />
      <div style={{ padding: "18px 20px 20px" }}>
        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", marginBottom: 6 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <Stethoscope size={15} color={tokens.amber} />
            <span style={{ fontFamily: fontDisplay, fontSize: 18, fontWeight: 600, color: tokens.text }}>
              {item.topic}
            </span>
          </div>
          <span
            style={{
              fontFamily: fontMono,
              fontSize: 12.5,
              color: hasRate ? strengthColor(item.acceptanceRate) : tokens.faint,
            }}
          >
            {hasRate ? `${item.acceptanceRate.toFixed(1)}% AC` : "—"}
          </span>
        </div>

        {item.reason && (
          <div style={{ fontFamily: fontBody, fontSize: 12.5, color: tokens.muted, lineHeight: 1.5, marginBottom: 14 }}>
            {item.reason}
          </div>
        )}

        <div
          style={{
            fontFamily: fontMono,
            fontSize: 10.5,
            letterSpacing: "0.1em",
            color: tokens.faint,
            marginBottom: 8,
          }}
        >
          RX — {item.problems.length} PROBLEM{item.problems.length === 1 ? "" : "S"}
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          {item.problems.map((p) => {
            // Handle either JSON key casing defensively — not fully
            // confirmed whether the Spring DTO's Jackson mapping
            // converts Python's snake_case title_slug to camelCase or
            // passes it through as-is.
            const slug = p.titleSlug || p.title_slug;
            const href = slug ? `https://leetcode.com/problems/${slug}/` : null;

            const rowStyle = {
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              padding: "8px 10px",
              background: tokens.ink,
              borderRadius: 6,
              border: `1px solid ${tokens.hairline}`,
              textDecoration: "none",
            };

            const rowContent = (
              <>
                <span style={{ fontFamily: fontBody, fontSize: 13, color: tokens.text }}>{p.title}</span>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  {p.difficulty && (
                    <span
                      style={{
                        fontFamily: fontMono,
                        fontSize: 10.5,
                        color:
                          p.difficulty === "Hard"
                            ? tokens.weak
                            : p.difficulty === "Medium"
                            ? tokens.amber
                            : tokens.strong,
                      }}
                    >
                      {p.difficulty.toUpperCase()}
                    </span>
                  )}
                  <ChevronRight size={13} color={tokens.faint} />
                </div>
              </>
            );

            // No real slug available — render as a non-link instead of
            // a broken/misleading URL that dumps the user on the
            // generic problemset page.
            if (!href) {
              return (
                <div key={p.title} style={{ ...rowStyle, opacity: 0.6, cursor: "default" }}>
                  {rowContent}
                </div>
              );
            }

            return (
              <a key={p.title} href={href} target="_blank" rel="noreferrer" style={rowStyle}>
                {rowContent}
              </a>
            );
          })}
        </div>
      </div>
    </div>
  );
}