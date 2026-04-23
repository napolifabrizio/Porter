## Why

The current Streamlit UI is tightly coupled to the Python runtime and cannot be deployed independently or evolved into a polished product-quality interface. Replacing it with a React SPA that consumes the existing FastAPI backend decouples the frontend from the Python stack, enables proper routing and richer UX patterns, and prepares the app for production deployment.

## What Changes

- New `App/` directory containing a Vite + React TypeScript project
- React app implements all current Streamlit UI features (product tracking, price checking, list management, move-to-list, LLM badge, expand/collapse cards, check-selected)
- Client-side routing: `/login` and `/list/:id`
- JWT-based auth stored in `sessionStorage`; 30-day token matches current backend config
- API client layer using `VITE_API_URL` env var (supports local + production)
- **BREAKING** (backend): `CORSMiddleware` added to FastAPI so browsers can reach the API
- Streamlit UI (`source/porter/ui/app.py`) remains in place but is no longer the primary UI

## Capabilities

### New Capabilities

- `react-frontend`: React/Vite SPA scaffold — routing, auth guard, Zustand global state, TanStack Query data layer, Tailwind + shadcn/ui component library, VITE_API_URL env var, CORS middleware on FastAPI

### Modified Capabilities

- `tracker-ui`: Launch mechanism changes from `streamlit run` to `npm run dev`; authentication changes from Python session state + password to JWT stored in sessionStorage; the UI surface and behavioral requirements remain identical

## Impact

- `App/` — new Vite/React project (scaffolded from scratch)
- `source/porter/app.py` — add `CORSMiddleware` (single-line change, backend-breaking for browsers without it)
- `pyproject.toml` / `poetry.lock` — no changes; React dependencies managed by npm inside `App/`
- `.env.example` — document `VITE_API_URL` and `SECRET_KEY` for full-stack local setup
