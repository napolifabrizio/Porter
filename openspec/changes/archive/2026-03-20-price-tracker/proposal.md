## Why

Users want a personal watchlist of products from any e-commerce site where they can manually trigger a price check and be instantly notified if the price dropped by 5% or more compared to when the product was first added.

## What Changes

- New Streamlit web UI for adding products by URL and triggering price checks
- Hybrid scraper that extracts product name, price, and description from any URL (BeautifulSoup first, LangChain LLM fallback)
- SQLite-backed product storage with initial and current price tracking
- Price comparison logic that flags a drop when `(initial − current) / initial ≥ 5%`

## Capabilities

### New Capabilities

- `product-storage`: Persist products (url, name, description, initial_price, current_price, last_checked) in SQLite
- `product-scraping`: Hybrid scraper — structured CSS selectors first, LangChain LLM extraction as fallback; normalizes price formats (R$, $, €)
- `price-checking`: On user request, re-scrape all tracked products, update current_price, and surface which products dropped ≥ 5%
- `tracker-ui`: Streamlit interface — URL input to add products, "Check All Prices" button, product list with ↓ / = indicators

### Modified Capabilities

## Impact

- New dependencies: `streamlit`, `langchain>=1.0`, `beautifulsoup4`, `requests`, `pydantic`, `httpx`
- New module: `source/porter/` package (`app.py`, `scraper.py`, `database.py`, `models.py`)
- Requires an LLM API key (e.g., OpenAI) for the scraper fallback path
- Local SQLite file created at runtime (e.g., `porter.db`)
