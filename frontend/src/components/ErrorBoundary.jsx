import React from "react";
import { tokens, fontDisplay, fontMono } from "../lib/tokens.js";

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, info) {
    // Surfaces in the browser console with a full stack + component
    // stack, in addition to the on-page message below.
    console.error("Dashboard crashed:", error, info);
  }

  render() {
    if (this.state.error) {
      return (
        <div
          style={{
            background: tokens.ink,
            minHeight: "100vh",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: 24,
          }}
        >
          <div style={{ maxWidth: 560, textAlign: "center" }}>
            <div style={{ fontFamily: fontDisplay, fontSize: 20, color: tokens.text, marginBottom: 10 }}>
              Something broke while rendering the chart.
            </div>
            <div
              style={{
                fontFamily: fontMono,
                fontSize: 12,
                color: tokens.faint,
                whiteSpace: "pre-wrap",
                textAlign: "left",
                background: tokens.panel,
                border: `1px solid ${tokens.hairline}`,
                borderRadius: 8,
                padding: 14,
                marginTop: 12,
              }}
            >
              {String(this.state.error?.message || this.state.error)}
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
