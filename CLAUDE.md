# CLAUDE.md — Porter

## What it is
Porter is a personal price watchlist app. The user pastes a product URL; Porter scrapes the price, stores it, and flags when it drops or rises ≥5% from the initial price.

## Stack
- **Frontend**: React 19 + TypeScript + Vite + Tailwind CSS v4 + shadcn/ui + TanStack Router + React Query + Zustand (`App/`)
- **Backend**: FastAPI (`source/porter/app.py`) — REST API with JWT auth
- **Language**: Python 3.11.9, managed with Poetry
- **Scraping**: httpx + curl-cffi (fetch) → BeautifulSoup4 (parse) → GPT-4o-mini via LangChain (LLM fallback, only when BS4 fails)
- **Models**: Pydantic v2 (`models.py`)
- **DB**: PostgreSQL (via `infrastructure/database.py`)

## Architecture — Clean / Ports & Adapters
```
App/                          # React frontend (served from S3 in prod)
  src/
    api/client.ts             # HTTP client (calls FastAPI)
    components/               # UI components (shadcn/ui based)
    hooks/                    # useLists, useProducts (React Query)
    pages/                    # ListPage, LoginPage
    store/auth.ts             # Zustand auth store

source/porter/
  app.py                      # FastAPI entry point (REST API + JWT)
  models.py                   # ScrapedData, Product, request/response DTOs
  domain/price_rules.py       # Pure price-drop rule (no I/O)
  application/
    ports.py                  # HtmlFetcher, ProductScraper, ProductRepository Protocols
    checker.py                # PriceChecker orchestrator (parallel via ThreadPoolExecutor)
    service.py                # AppService facade used by API
  infrastructure/
    fetcher.py                # httpx / curl-cffi HTTP client
    scraper.py                # BS4 + LLM hybrid scraper
    database.py               # PostgreSQL implementation
    auth.py                   # Password verification
```

Dependency direction: `api → application → domain`. Infrastructure implements ports; domain has no imports from other layers.

## Key invariants
- `initial_price` is set once on insert and never updated — it's the permanent baseline.
- Price drop threshold: `(initial_price − current_price) / initial_price ≥ 0.05`
- No background polling — checks are always user-triggered.
- LLM scraper is a fallback only; JsonLD and BS4 runs first to keep costs low.

## Dev workflow
```bash
# Backend
poetry install
cp .env.example .env
poetry run uvicorn porter.app:app --reload  # API on http://localhost:8000

# Frontend
cd App
npm install
npm run dev                                 # React on http://localhost:5173
```

## Env
- `OPENAI_API_KEY` — required for LLM fallback scraper
- `SECRET_KEY` — JWT signing key (required)
- `CORS_ORIGINS` — comma-separated allowed origins (default: `http://localhost:5173`)

## Docs
The folder ./docs contains others documentations, you cant read all of them at once, you have to read just that documentation that you
will need, you will read on-demand. Below you can see descriptions of each one, so, you will know when you will need to read each one.

`architecture_rules.md` -> When you will implement something, you will read it to respect the code rules of this project.
`application` -> When you will do some implementation, plan or research inside this folder.
`infrastructure` -> When you will do some implementation, plan or research inside this folder.
`domain` -> When you will do some implementation, plan or research inside this folder.
`ui` -> When you will do some implementation, plan or research inside this folder.
