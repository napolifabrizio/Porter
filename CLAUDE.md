# CLAUDE.md — Porter

## What it is
Porter is a personal price watchlist app. The user pastes a product URL; Porter scrapes the price, stores it, and flags when it drops or rises ≥5% from the initial price.

## Stack
- **UI**: Streamlit (`source/porter/ui/app.py`)
- **Language**: Python 3.11.9, managed with Poetry
- **Scraping**: httpx + curl-cffi (fetch) → BeautifulSoup4 (parse) → GPT-4o-mini via LangChain (LLM fallback, only when BS4 fails)
- **Models**: Pydantic v2 (`models.py`)
- **DB**: SQLite (`porter.db`, created on first run)

## Architecture — Clean / Ports & Adapters
```
source/porter/
  models.py              # ScrapedData, Product — shared DTOs
  domain/price_rules.py  # Pure price-drop rule (no I/O)
  application/
    ports.py             # HtmlFetcher, ProductScraper, ProductRepository Protocols
    checker.py           # PriceChecker orchestrator (parallel via ThreadPoolExecutor)
    service.py           # AppService facade used by UI
  infrastructure/
    fetcher.py           # httpx / curl-cffi HTTP client
    scraper.py           # BS4 + LLM hybrid scraper
    database.py          # SQLite implementation
  ui/app.py              # Streamlit entry point
```

Dependency direction: `ui → application → domain`. Infrastructure implements ports; domain has no imports from other layers.

## Key invariants
- `initial_price` is set once on insert and never updated — it's the permanent baseline.
- Price drop threshold: `(initial_price − current_price) / initial_price ≥ 0.05`
- No background polling — checks are always user-triggered.
- LLM scraper is a fallback only; JsonLD and BS4 runs first to keep costs low.

## Dev workflow
```bash
poetry install                              # install deps
cp .env.example .env                        # set OPENAI_API_KEY
poetry run streamlit run source/porter/ui/app.py   # run app
```

Use `/streamlit` to launch the app from Claude Code.

## Env
- `OPENAI_API_KEY` — required for LLM fallback scraper

## Docs
The folder ./docs contains others documentations, you cant read all of them at once, you have to read just that documentation that you
will need, you will read on-demand. Below you can see descriptions of each one, so, you will know when you will need to read each one.

`architecture_rules.md` -> When you will implement something, you will read it to respect the code rules of this project.
`application` -> When you will do some implementation, plan or research inside this folder.
`infrastructure` -> When you will do some implementation, plan or research inside this folder.
`domain` -> When you will do some implementation, plan or research inside this folder.
`ui` -> When you will do some implementation, plan or research inside this folder.
