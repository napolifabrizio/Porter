# Porter — Price Tracker

A personal price watchlist app. Paste a product URL, Porter scrapes the price, stores it, and tells you when it drops 5% or more from the original.

> Built with the assistance of **[Claude Code](https://claude.ai/claude-code)** — Anthropic's agentic CLI for software engineering.

---

## What it does

- Paste any product URL from any e-commerce site
- Porter fetches the page and extracts the product name and price automatically
- Tracks price history against the initial price (your baseline never changes)
- Check all prices or select specific products to re-check
- Highlights price drops of 5% or more in green

---

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11.9 |
| Package manager | Poetry |
| UI | Streamlit |
| Primary scraper | httpx + BeautifulSoup4 |
| LLM fallback scraper | LangChain + GPT-4o-mini (OpenAI) |
| Data models | Pydantic v2 |
| Database | SQLite (local file `porter.db`) |

### Hybrid scraping strategy

Porter uses a two-step approach to keep costs low:

1. **BeautifulSoup4** — tries standard CSS selectors (`itemprop`, `og:*` meta tags, `[class*='price']`, `h1`). Fast and free.
2. **LLM fallback** — if BS4 can't find name or price, the page text is sent to `gpt-4o-mini` via LangChain with structured output. Only fires when needed.

Price strings like `R$ 1.299,99`, `$12.99`, and `€1,299.00` are all normalized to float correctly.

---

## Project layout

```
source/porter/
  app.py        # Streamlit UI entry point
  scraper.py    # fetch_and_scrape: BS4 first, LLM fallback
  checker.py    # check_all_prices: re-scrapes, updates DB, returns CheckResult list
  database.py   # SQLite helpers: init_db, add_product, list_products, update_price
  models.py     # ScrapedData, Product (Pydantic v2)

openspec/
  specs/        # Capability specs per feature area
  changes/      # Active feature changes (OpenSpec workflow)
  changes/archive/  # Completed and archived changes
```

---

## Running locally

```bash
# 1. Install dependencies
poetry install

# 2. Set your OpenAI key (required for LLM fallback)
export OPENAI_API_KEY=sk-...

# 3. Run
poetry run streamlit run source/porter/app.py
```

The SQLite database (`porter.db`) is created automatically on first run.

---

## Key design decisions

- **`initial_price` is immutable.** Once a product is added, `initial_price` never changes — it's the permanent baseline. Only `current_price` and `last_checked` are updated on each check.
- **5% drop threshold.** Defined as `(initial_price − current_price) / initial_price ≥ 0.05` in `checker.py`.
- **No background polling.** Price checks are intentionally manual — the user triggers them. No scheduler, no daemon.
- **Selective checking.** Each product has a checkbox so you can check only the ones you care about right now.

---

## Roadmap

### Frontend
- [ ] Replace Streamlit with a production-grade frontend (React or Next.js) with a proper component library
- [ ] Price history chart per product (line graph over time)
- [ ] Notification system — email or push alerts when a price drop is detected
- [ ] Multi-user support with authentication

### Infrastructure (AWS)
- [ ] Containerize the backend with Docker and deploy to **AWS ECS (Fargate)**
- [ ] Serve the frontend via **AWS CloudFront** with an S3 origin
- [ ] Migrate from SQLite to **AWS RDS (PostgreSQL)** for a managed, durable database
- [ ] Store secrets in **AWS Secrets Manager**
- [ ] Set up a CI/CD pipeline with **GitHub Actions** deploying to ECS on push
- [ ] Add scheduled price checks using **AWS EventBridge** (replace manual trigger with automatic background polling)
- [ ] Centralized logging and monitoring with **AWS CloudWatch**

---

## License

MIT
