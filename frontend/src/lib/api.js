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

async function request(path) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new ApiError(`${path} responded with ${response.status}`, response.status);
  }

  return response.json();
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

// No recent-submissions endpoint exists on the backend yet (only
// UserController, AnalyticsController, PracticePlanController are wired
// up). App.jsx already catches this call's failure and falls back to an
// empty list, so the dashboard still renders without it. Add a real
// endpoint (e.g. backed by SubmissionRepository.findAll()) and point
// this at it once it exists.
export function getRecentSubmissions(username) {
  return request(`/api/v1/users/${encodeURIComponent(username)}/submissions/recent`);
}

export { ApiError };
