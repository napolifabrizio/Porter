# Porter — Price Tracker

Personal watchlist app: paste a product URL, track its price, get notified when it drops ≥ 5%.

## Stack

- **Python 3.11.9** managed with **Poetry**
- **Streamlit** — UI (`source/porter/app.py`)
- **LangChain + gpt-4o-mini** — LLM fallback scraper
- **httpx + BeautifulSoup4** — primary scraper
- **SQLite** — local database (`porter.db`, created at runtime)
- **Pydantic v2** — data models

## Project Layout

```
source/porter/
  app.py        # Streamlit entry point
  scraper.py    # fetch_and_scrape: BS4 first, LLM fallback
  checker.py    # check_all_prices: re-scrapes, updates DB, returns CheckResult list
  database.py   # SQLite helpers: init_db, add_product, list_products, update_price
  models.py     # ScrapedData, Product (Pydantic)

openspec/
  specs/        # Capability specs: price-checking, product-scraping, product-storage, tracker-ui
  changes/      # Active feature changes (OpenSpec workflow)
  changes/archive/  # Completed changes
```

## Running the App

```bash
# Install dependencies
poetry install

# Set your OpenAI key (required for LLM fallback scraper)
export OPENAI_API_KEY=sk-...

# Run
poetry run streamlit run source/porter/app.py
```

The SQLite database (`porter.db`) is created automatically in the working directory on first run.

## Key Design Decisions

- **Hybrid scraping**: BS4 with common CSS selectors runs first; LLM extraction is only used when BS4 fails. This keeps costs low and avoids unnecessary API calls.
- **Price drop threshold**: `(initial_price − current_price) / initial_price ≥ 0.05` (5%). Defined in `checker.py:DROP_THRESHOLD`.
- **`initial_price` is immutable**: Once a product is added, `initial_price` never changes — it's the baseline for all comparisons. Only `current_price` and `last_checked` are updated.
- **Price normalization**: `scraper.normalize_price` handles R$, $, € and European/Brazilian comma-dot conventions.
- **No background polling**: Price checks are manual — the user clicks "Check All Prices".

## OpenSpec Workflow

New features are developed using the OpenSpec workflow:
- Use `/openspec-propose` to propose a change (creates `openspec/changes/<slug>/`)
- Use `/openspec-apply-change` to implement tasks from the change
- Use `/openspec-archive-change` to finalize and archive a completed change

Capability specs live in `openspec/specs/` and define the contract for each feature area.
