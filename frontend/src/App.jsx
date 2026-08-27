import React, { useEffect, useState } from "react";
import { ClipboardList } from "lucide-react";
import { tokens, fontMono, fontDisplay } from "./lib/tokens.js";
import { getAnalyticsSummary, getPracticePlan, getRecentSubmissions, syncUser, ApiError } from "./lib/api.js";
import {
  mockOverall,
  mockDifficulty,
  mockTopics,
  mockRecentSubmissions,
  mockPrescription,
} from "./data/mockData.js";

import Header from "./components/Header.jsx";
import HeroStats from "./components/HeroStats.jsx";
import DifficultyDial from "./components/DifficultyDial.jsx";
import TopicHeatmap from "./components/TopicHeatmap.jsx";
import PrescriptionCard from "./components/PrescriptionCard.jsx";
import RecentActivity from "./components/RecentActivity.jsx";

const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA !== "false";
const USERNAME = import.meta.env.VITE_DEFAULT_USERNAME || "Priyadrasta_Raut";

function SectionLabel({ children }) {
  return (
    <div
      style={{
        fontFamily: fontMono,
        fontSize: 11,
        letterSpacing: "0.14em",
        textTransform: "uppercase",
        color: tokens.faint,
        marginBottom: 14,
      }}
    >
      {children}
    </div>
  );
}

function CenteredMessage({ children }) {
  return (
    <div
      style={{
        minHeight: "60vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: fontDisplay,
        fontSize: 18,
        color: tokens.muted,
        textAlign: "center",
        padding: 24,
      }}
    >
      {children}
    </div>
  );
}

export default function App() {
  const [state, setState] = useState({ status: "loading", data: null, error: null });

  useEffect(() => {
    let cancelled = false;

    async function load() {
      if (USE_MOCK_DATA) {
        setState({
          status: "ready",
          data: {
            overall: mockOverall,
            difficulty: mockDifficulty,
            topics: mockTopics,
            prescription: mockPrescription,
            recentSubmissions: mockRecentSubmissions,
          },
          error: null,
        });
        return;
      }

      try {
        // Best-effort sync before loading — if this fails or times
        // out (expired LeetCode session, Python service degraded,
        // etc.), we deliberately don't block the dashboard on it.
        // Whatever's already in the database is still shown; the user
        // just doesn't get today's newest submissions until sync
        // succeeds again. Silent-but-logged rather than surfaced as a
        // hard error, since a sync hiccup shouldn't make the whole
        // dashboard look broken.
        await syncUser(USERNAME);
      } catch (err) {
        console.warn(
          "Sync before dashboard load failed or timed out — showing last known data.",
          err
        );
      }

      try {
        const [summary, plan, recent] = await Promise.all([
          getAnalyticsSummary(USERNAME),
          getPracticePlan(USERNAME),
          getRecentSubmissions(USERNAME).catch(() => []),
        ]);

        if (cancelled) return;

        setState({
          status: "ready",
          data: {
            overall: summary.overall,
            difficulty: summary.difficulty,
            topics: summary.topics,
            // PracticePlan (Python) only returns { topic, goal, problems } —
            // no acceptanceRate field. Look it up from the analytics
            // summary's weaknesses/topics list instead, matched by topic
            // name, with a 0 fallback so a name mismatch can't crash
            // PrescriptionCard's .toFixed(1) call.
            prescription: plan.map((p) => {
              const topicStats =
                summary.weaknesses?.find((w) => w.topic === p.topic) ||
                summary.topics?.find((t) => t.topic === p.topic);

              return {
                topic: p.topic,
                acceptanceRate: topicStats?.acceptanceRate ?? 0,
                reason: p.goal,
                problems: p.problems,
              };
            }),
            recentSubmissions: recent,
          },
          error: null,
        });
      } catch (err) {
        if (cancelled) return;
        setState({ status: "error", data: null, error: err });
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  if (state.status === "loading") {
    return (
      <div style={{ background: tokens.ink, minHeight: "100vh" }}>
        <CenteredMessage>Reading your chart…</CenteredMessage>
      </div>
    );
  }

  if (state.status === "error") {
    const message =
      state.error instanceof ApiError
        ? `The API responded with ${state.error.status}.`
        : "Couldn't reach the API. Is the Spring Boot backend running?";

    return (
      <div style={{ background: tokens.ink, minHeight: "100vh" }}>
        <CenteredMessage>
          <div>
            <ClipboardList size={28} color={tokens.amber} style={{ marginBottom: 12 }} />
            <div>{message}</div>
            <div style={{ fontFamily: fontMono, fontSize: 12, color: tokens.faint, marginTop: 10 }}>
              {String(state.error.message || state.error)}
            </div>
          </div>
        </CenteredMessage>
      </div>
    );
  }

  const { overall, difficulty, topics, prescription, recentSubmissions } = state.data;

  return (
    <div
      style={{
        background: tokens.ink,
        minHeight: "100vh",
        color: tokens.text,
        fontFamily: "'Inter', system-ui, sans-serif",
        paddingBottom: 60,
      }}
    >
      <Header username={USERNAME} streakDays={overall.streakDays} />

      <div style={{ maxWidth: 1080, margin: "0 auto", padding: "36px 32px 0" }}>
        <HeroStats overall={overall} />

        <SectionLabel>Vitals — by difficulty</SectionLabel>
        <div style={{ display: "flex", gap: 16, marginBottom: 40, flexWrap: "wrap" }}>
          {difficulty.map((d) => (
            <DifficultyDial key={d.difficulty} d={d} />
          ))}
        </div>

        <SectionLabel>Diagnostic readout — topics, weakest first</SectionLabel>
        <div style={{ marginBottom: 40 }}>
          <TopicHeatmap topics={topics} />
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1.4fr 1fr", gap: 28, alignItems: "start" }}>
          <div>
            <SectionLabel>Prescription — recommended practice</SectionLabel>
            <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              {prescription.length === 0 && (
                <div style={{ fontFamily: fontMono, fontSize: 13, color: tokens.faint }}>
                  No weak topics detected yet — keep practicing to build up analytics.
                </div>
              )}
              {prescription.map((p) => (
                <PrescriptionCard key={p.topic} item={p} />
              ))}
            </div>
          </div>

          <div>
            <SectionLabel>Recent activity</SectionLabel>
            <RecentActivity submissions={recentSubmissions} lastSyncedLabel="Synced 4 minutes ago" />
          </div>
        </div>
      </div>
    </div>
  );
}
