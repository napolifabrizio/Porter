## 1. Project Setup

- [x] 1.1 Add dependencies to `pyproject.toml`: `streamlit`, `langchain>=1.0`, `langchain-openai`, `beautifulsoup4`, `httpx`, `pydantic`
- [x] 1.2 Create `source/porter/__init__.py`

## 2. Data Models

- [x] 2.1 Create `source/porter/models.py` with a `Product` Pydantic model (id, url, name, description, initial_price, current_price, last_checked) and a `ScrapedData` model (name, price, description)

## 3. Database Layer

- [x] 3.1 Create `source/porter/database.py` with `init_db()` that creates `porter.db` and the `products` table if not exists
- [x] 3.2 Implement `add_product(scraped: ScrapedData, url: str) -> Product` — inserts and returns the new record; raises on duplicate URL
- [x] 3.3 Implement `list_products() -> list[Product]` — returns all products ordered by id ascending
- [x] 3.4 Implement `update_price(product_id: int, new_price: float)` — updates `current_price` and `last_checked`

## 4. Scraper

- [x] 4.1 Create `source/porter/scraper.py` with `normalize_price(raw: str) -> float` that handles R$, $, € formats and European/US decimal notation
- [x] 4.2 Implement `scrape_with_bs4(html: str) -> ScrapedData | None` — tries `[itemprop="price"]`, `[class*="price"]`, `meta[property="og:price:amount"]` for price; `h1`, `[itemprop="name"]`, `meta[property="og:title"]` for name; `meta[name="description"]`, `[itemprop="description"]` for description
- [x] 4.3 Implement `scrape_with_llm(html: str) -> ScrapedData` — strips `<script>`/`<style>`, truncates to ~8000 chars, uses LangChain `ChatPromptTemplate` + structured output (Pydantic) to extract name, price string, description; normalizes price
- [x] 4.4 Implement `fetch_and_scrape(url: str) -> ScrapedData` — fetches URL with `httpx` (browser User-Agent), tries BS4 first, falls back to LLM if any field is missing, raises descriptive errors on network or parse failures

## 5. Price Checking

- [x] 5.1 Create `source/porter/checker.py` with a `CheckResult` dataclass (product, dropped, change_pct, error)
- [x] 5.2 Implement `check_all_prices(products: list[Product]) -> list[CheckResult]` — re-scrapes each product, updates DB, computes drop using `(initial - current) / initial >= 0.05`, catches per-product errors without aborting the loop

## 6. Streamlit UI

- [x] 6.1 Create `source/porter/app.py` — call `init_db()` at startup
- [x] 6.2 Add URL input + "Add Product" button; on click: call `fetch_and_scrape`, then `add_product`; show success/warning/error messages
- [x] 6.3 Add "Check All Prices" button; on click: load all products, call `check_all_prices`, display results
- [x] 6.4 Render product list with name, current price, and indicator: green "↓ -X%" if dropped, neutral "=" otherwise, red error message if check failed
- [x] 6.5 Show empty-state message when no products are tracked
