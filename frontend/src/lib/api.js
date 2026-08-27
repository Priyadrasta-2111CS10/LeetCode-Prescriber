// Base URL for the Spring Boot API.
//
// - In dev (`npm run dev`), requests to "/api/..." are proxied to
//   http://localhost:8080 by vite.config.js, so leave this as "".
// - In production, set VITE_API_BASE_URL at build time if the frontend
//   is hosted on a different origin than the API, e.g.:
//     VITE_API_BASE_URL=https://api.example.com npm run build
//   If the frontend is served BY Spring Boot itself (see README), leave
//   this unset — same-origin requests need no base URL.
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

// `options` is forwarded straight to fetch() — method, signal, body,
// etc. Previously this only ever accepted `path`, so any caller trying
// to pass { method: "POST" } (like syncUser below) was silently
// ignored and every request went out as GET regardless of what was
// asked for.
async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { Accept: "application/json" },
    ...options,
  });

  if (!response.ok) {
    throw new ApiError(`${path} responded with ${response.status}`, response.status);
  }

  // POST /sync returns 200 with no body in some setups — guard against
  // response.json() throwing on an empty body.
  const text = await response.text();
  return text ? JSON.parse(text) : null;
}

// Matches AnalyticsController -> AnalyticsService.getSummary(username) ->
// AnalyticsSummaryResponse { overall, difficulty, topics, weaknesses }
export function getAnalyticsSummary(username) {
  return request(`/api/v1/users/${encodeURIComponent(username)}/analytics/summary`);
}

// Matches PracticePlanController -> PracticePlanService.generatePlan(username)
// -> List<PracticeTopicPlan>
export function getPracticePlan(username) {
  return request(`/api/v1/users/${encodeURIComponent(username)}/practice-plan`);
}

// Matches UserController -> UserService.getUser(username) -> User
export function getUser(username) {
  return request(`/api/v1/users/${encodeURIComponent(username)}`);
}

// Matches SubmissionController -> SubmissionService.getRecentSubmissions
export function getRecentSubmissions(username) {
  return request(`/api/v1/users/${encodeURIComponent(username)}/submissions/recent`);
}

// Triggers a fresh sync against LeetCode before the dashboard loads.
// Client-side timeout via AbortController so a slow/hanging sync can't
// block the dashboard indefinitely — it aborts and falls back to
// whatever's already in the database.
export function syncUser(username, timeoutMs = 8000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  return request(`/api/v1/users/${encodeURIComponent(username)}/sync`, {
    method: "POST",
    signal: controller.signal,
  }).finally(() => clearTimeout(timeoutId));
}

export { ApiError };