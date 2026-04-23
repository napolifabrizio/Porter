## Context

Porter is a personal price watchlist app. The backend is a FastAPI service with JWT Bearer auth (HS256, 30-day tokens). The current UI is Streamlit (`source/porter/ui/app.py`) — a Python SSR tool that runs in the same process as the app. The new React frontend lives in `App/` and communicates with FastAPI exclusively over HTTP. The FastAPI app currently has no CORS configuration, so browsers would reject all cross-origin requests. Local dev will run the React dev server on a different port than FastAPI.

## Goals / Non-Goals

**Goals:**
- Replicate every feature of the Streamlit UI in React (feature parity)
- Desktop-first layout (no mobile breakpoints required)
- Blocking spinner for long operations (Check All / Check Selected can take 10–30 s)
- JWT stored in `sessionStorage` (closes on browser tab close, no extra refresh logic)
- Configurable API base URL via `VITE_API_URL` env var (supports local + production targets)
- CORS middleware on FastAPI to allow browser requests

**Non-Goals:**
- Mobile responsiveness
- Push notifications or background polling
- Modifying the FastAPI business logic or auth scheme
- Removing or deprecating the Streamlit UI

## Decisions

### D1 — Vite + React + TypeScript
**Decision**: Scaffold `App/` with `npm create vite@latest` using the React + TypeScript template.  
**Rationale**: Fastest cold-start for a greenfield SPA. TypeScript catches API contract mismatches at compile time. Alternatives considered: Next.js (overkill — no SSR needed, adds deployment complexity), CRA (deprecated).

### D2 — TanStack Router for routing
**Decision**: Use TanStack Router (v1) with two routes: `/login` and `/list/$listId`.  
**Rationale**: Type-safe route params without boilerplate. The app has exactly two views; a single-file route tree is sufficient. Alternatives considered: React Router v7 (more familiar but less type-safe), no router / single-page state (ruled out — deep-linking to a list is valuable).

### D3 — TanStack Query for server state
**Decision**: Wrap all API calls in `useQuery` / `useMutation` hooks.  
**Rationale**: Automatic cache invalidation, loading/error states, and background refetch fit the "check and refresh" interaction model. Alternatives considered: SWR (fewer features for mutations), raw `fetch` + `useState` (too much manual wiring for a list app).

### D4 — Zustand for global client state
**Decision**: A single Zustand store holds `{ token, setToken, clearToken }`.  
**Rationale**: Auth token must be accessible by the API client module, which is not a React component. Zustand is framework-agnostic and avoids prop-drilling. Alternatives considered: React Context (requires provider nesting and re-renders on token change), Redux (overkill for one slice of state).

### D5 — sessionStorage for JWT persistence
**Decision**: Persist the JWT in `sessionStorage`, not `localStorage`.  
**Rationale**: Closing the browser tab forces re-login, which is acceptable for a personal-use app and avoids XSS exposure via `localStorage`. The 30-day token TTL means re-login is rare in normal usage. Alternatives considered: `localStorage` (longer persistence but XSS risk), cookie (requires backend changes).

### D6 — Tailwind CSS + shadcn/ui
**Decision**: Tailwind for utility-first styling; shadcn/ui for pre-built accessible primitives (Button, Input, Dialog for delete confirmation).  
**Rationale**: shadcn/ui components are copied into `App/components/ui/` — no runtime dependency, full control. Tailwind avoids CSS modules overhead. Alternatives considered: Chakra UI (runtime overhead), MUI (opinionated design that conflicts with custom layout).

### D7 — CORS via FastAPI middleware
**Decision**: Add `CORSMiddleware` to `source/porter/app.py` allowing `http://localhost:5173` in development and a configurable `CORS_ORIGINS` env var for production.  
**Rationale**: Minimal change to the backend — a single `app.add_middleware(...)` call before any route definitions. Alternatives considered: proxy in Vite dev server (hides CORS config needed for production, would need to be re-done).

### D8 — Typed API client module
**Decision**: A single `App/src/api/client.ts` module exports typed async functions for every FastAPI endpoint. It reads `import.meta.env.VITE_API_URL` and attaches `Authorization: Bearer <token>` from Zustand.  
**Rationale**: Central place to update the base URL and token logic. TypeScript interfaces mirror Pydantic models, giving compile-time safety for API responses. Alternatives considered: OpenAPI codegen (adds build step complexity that's premature for ~10 endpoints).

### D9 — Blocking spinner for price checks
**Decision**: While `POST /products/check` or `POST /products/check-selected` is in-flight, render a full-page overlay spinner. No partial updates.  
**Rationale**: Matches the Streamlit behavior the user already understands. The check can take 10–30 s; a skeleton or partial update would require streaming from the backend, which is out of scope.

### D10 — Active list via URL param, not global state
**Decision**: The active list is encoded in the route (`/list/$listId`). Navigating to a list sets the URL.  
**Rationale**: The URL is the canonical source of truth for "which list am I on". Deep links work, browser back/forward works. Zustand only stores auth state; list state lives in the router.

## Risks / Trade-offs

- **sessionStorage re-login on tab close** → Acceptable for a personal app; the 30-day JWT means re-login is a one-time cost per session. If this becomes painful, swap to `localStorage` in the Zustand persist middleware.
- **Long check duration with blocking spinner** → UX could feel frozen. Mitigation: show a descriptive spinner label ("Checking prices, this may take ~30 s"). If backend later supports streaming, the spinner can be replaced incrementally.
- **CORS `allowed_origins` misconfiguration in production** → Could lock out the frontend or open the API to any origin. Mitigation: document the `CORS_ORIGINS` env var clearly in `.env.example`; default to `http://localhost:5173` only.
- **Stale check_results display** → After navigating between lists, old stripe state from a previous check might linger. Mitigation: `check_results` is stored in TanStack Query mutation state scoped to the current query; navigating clears it naturally via component unmount.
- **shadcn/ui component upgrades** → Components are copied into the repo, so upstream changes require manual re-copy. Mitigation: acceptable for a personal tool; lock the shadcn CLI version in `package.json`.

## Migration Plan

1. Add `CORSMiddleware` to `source/porter/app.py` (backend change, deploy first or simultaneously).
2. Scaffold `App/` with Vite and install dependencies.
3. Implement API client, auth layer, and routing shell.
4. Implement all UI features (product list, list sidebar, check actions).
5. Update `.env.example` to document `VITE_API_URL`.
6. Run `npm run dev` locally alongside `uvicorn` to verify end-to-end.
7. Streamlit UI stays as-is; no removal planned.

**Rollback**: CORS middleware can be removed from `app.py` independently. The React app is fully additive — nothing in the backend or Streamlit UI changes behavior.

## Open Questions

- Production hosting target for the React app (static file host like Vercel/Netlify, or served from within FastAPI via `StaticFiles`)? This affects how `VITE_API_URL` is set and whether CORS is needed in production at all.
- Should `GET /products/check` results persist between list navigations, or reset on route change? (Current decision: reset on unmount — simple, predictable.)
