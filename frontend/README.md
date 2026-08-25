# The Prescriber — frontend

React + Vite dashboard for the LeetCode practice recommendation engine.
Renders standalone with bundled mock data out of the box — no backend
required to see the UI.

## Project structure

```
frontend/
├── src/
│   ├── components/       # Header, HeroStats, DifficultyDial, TopicHeatmap,
│   │                      PrescriptionCard, RecentActivity
│   ├── data/mockData.js  # Fallback data used when VITE_USE_MOCK_DATA=true
│   ├── lib/
│   │   ├── api.js        # fetch wrappers for the Spring Boot endpoints
│   │   └── tokens.js     # design tokens (colors, fonts, strengthColor())
│   ├── App.jsx           # assembles everything, loading/error states
│   ├── main.jsx           # React entry point
│   └── index.css
├── index.html
├── vite.config.js         # dev server + /api proxy to localhost:8080
├── Dockerfile              # multi-stage build -> nginx static serve
├── nginx.conf               # SPA fallback + /api reverse proxy
├── docker-compose.yml
└── .env.example
```

## Local development

```bash
npm install
cp .env.example .env.local   # adjust if needed; defaults work out of the box
npm run dev
```

Open http://localhost:5173 — you'll see the dashboard immediately, running
on bundled mock data (`VITE_USE_MOCK_DATA=true` by default).

## Wiring to the real backend

1. Set `VITE_USE_MOCK_DATA=false` in `.env.local`.
2. Run your Spring Boot API on `localhost:8080` (the Vite dev server already
   proxies `/api/*` there — see `vite.config.js`).
3. Confirm the endpoints in `src/lib/api.js` match your actual controllers:
   - `GET /api/analytics/{username}/summary` → `AnalyticsSummaryResponse`
   - `GET /api/practice-plan/{username}` → `List<PracticeTopicPlan>`
   - `GET /api/submissions/{username}/recent` → recent submissions (add this
     endpoint if it doesn't exist yet; it's optional — the page still loads
     without it)

   **CORS note:** in dev the Vite proxy avoids CORS entirely. In production
   (see hosting below), the nginx config also proxies `/api/*` server-side
   for the same reason — the browser only ever talks to one origin. If you
   ever call the Spring Boot API directly from the browser instead, you'll
   need `@CrossOrigin` (or a `CorsConfig` bean) on the Spring side.

4. If your DTO field names differ from what's assumed in `App.jsx` (the
   `prescription` mapping in particular), adjust that mapping — it's
   flagged with a comment at the spot most likely to need a tweak.

## Building for production

```bash
npm run build
```
Outputs static files to `dist/` — deployable to any static host (Vercel,
Netlify, S3+CloudFront, GitHub Pages, or your own server).

## Hosting options

**Option A — Docker (recommended, matches your existing Postgres/Redis setup)**

```bash
docker build -t prescriber-frontend .
docker run -p 8081:80 prescriber-frontend
```
Open http://localhost:8081. The container serves the built app via nginx
and reverse-proxies `/api/*` to a service named `leettracker-api` — update
`nginx.conf`'s `proxy_pass` if your backend container/host is named
differently.

To run it alongside your existing stack, copy the `frontend` service block
from `docker-compose.yml` here into your project's main compose file (the
one already defining `postgres` and `redis`), so all services share a
network and the frontend can reach the backend by container name.

**Option B — Static host (Vercel / Netlify / GitHub Pages)**

Point the host at this folder, build command `npm run build`, output
directory `dist`. Set `VITE_API_BASE_URL` as a build-time environment
variable to your deployed backend's public URL (since there's no nginx
proxy on these platforms, the browser will call the API directly — make
sure CORS is enabled on the Spring Boot side in this case).

**Option C — Serve directly from Spring Boot**

Copy the contents of `dist/` into Spring Boot's `src/main/resources/static/`
after building. The whole app then serves from one origin/port — simplest
option if you don't want a separate frontend deployment, at the cost of
rebuilding/redeploying the backend whenever the frontend changes.

## Design notes

Colors, fonts, and the acceptance-rate → color interpolation used across
the heatmap and stat accents all live in `src/lib/tokens.js` — change them
in one place. The "prescription pad" perforated-edge styling on the
recommendation cards is deliberate (it's meant to echo the app's own
diagnose → prescribe framing) — most other surfaces are kept quieter by
design so that one element carries the visual personality.
