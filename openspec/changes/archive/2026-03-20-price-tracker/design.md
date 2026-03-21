## Context

Porter is a fresh Python project (empty `source/porter/` package, Poetry build system). There are no existing modules, no database, and no UI. This design establishes the full architecture from scratch.

The app is a local, single-user desktop tool. There is no server, no auth, and no multi-tenancy to worry about.

## Goals / Non-Goals

**Goals:**
- Add any product by URL from any e-commerce site
- Extract name, price, and description reliably via a hybrid scraper
- Store products in a local SQLite database
- Allow the user to trigger a full price re-check with one button
- Surface products whose price dropped ≥ 5% from the initial price
- Keep the app runnable with `streamlit run source/porter/app.py`

**Non-Goals:**
- Scheduled/automatic price checks (no cron, no background workers)
- Price history over time (only initial vs. current)
- Multi-user support or cloud sync
- Browser automation (no Playwright/Selenium in first iteration)
- Notifications (email, SMS, push)

## Decisions

### 1. Package structure: flat modules inside `source/porter/`

```
source/porter/
├── __init__.py
├── app.py          ← Streamlit entry point
├── scraper.py      ← hybrid extraction logic
├── database.py     ← SQLite CRUD via sqlite3 stdlib
└── models.py       ← Pydantic v2 models
```

**Why**: Keeps the package small and navigable. No sub-packages needed at this scale. Each module has a single clear responsibility.

**Alternative considered**: A `services/` layer. Rejected — over-engineered for a single-user local tool.

---

### 2. Hybrid scraper: BeautifulSoup first, LangChain LLM fallback

**Flow:**
```
URL → httpx.get(url, headers=browser_headers)
          │
          ▼
   BeautifulSoup parse
   try common selectors:
   - price: [class*="price"], [itemprop="price"], meta[property="og:price:amount"]
   - name:  h1, [itemprop="name"], meta[property="og:title"]
   - desc:  [itemprop="description"], meta[name="description"]
          │
          ├── all three found? → return ProductData
          │
          └── missing any? → LangChain fallback
                    │
                    ▼
             strip <script>/<style> from HTML
             truncate to ~8000 chars
             ChatPromptTemplate → LLM
             structured output (Pydantic)
                    │
                    └── return ProductData
```

**Why LangChain**: Product pages have wildly varying structures. An LLM reliably extracts semantic fields (name, price, description) from messy HTML without site-specific rules.

**Why truncate**: Raw HTML can be 300–600KB. LLMs have token limits and cost per token. Stripping scripts/styles and truncating to ~8000 chars preserves the visible content that carries price/name.

**Why `httpx` over `requests`**: HTTP/2 support, better timeout ergonomics. Both are viable; `httpx` is slightly more modern.

**LLM provider**: OpenAI (`gpt-4o-mini`) via `langchain-openai`. Cheap, fast, sufficient for structured extraction. Key loaded from `OPENAI_API_KEY` env var.

**Alternative considered**: Always using LLM. Rejected — unnecessary cost and latency when BS4 works. Per-domain caching of "needs LLM" is a future optimization.

---

### 3. SQLite via stdlib `sqlite3`

Single `porter.db` file at the project root. No ORM.

**Schema:**
```sql
CREATE TABLE products (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    url           TEXT NOT NULL UNIQUE,
    name          TEXT NOT NULL,
    description   TEXT,
    initial_price REAL NOT NULL,
    current_price REAL NOT NULL,
    last_checked  TEXT NOT NULL   -- ISO 8601 datetime
);
```

**Why no ORM**: SQLAlchemy is overkill for one table and simple CRUD. Direct `sqlite3` keeps dependencies minimal and code transparent.

**Why `UNIQUE` on url**: Prevents duplicate products. Attempting to add an already-tracked URL should be rejected gracefully.

---

### 4. Price normalization

Prices arrive as strings like `"R$ 1.299,99"`, `"$12.99"`, `"€1,299.00"`. The scraper normalizes them:

1. Strip currency symbols and whitespace
2. Detect format: if `.` appears before `,` → European format (`1.299,99` → `1299.99`)
3. Replace `,` with `.` and cast to `float`

---

### 5. Drop threshold: ≥ 5%

```python
def is_price_dropped(initial: float, current: float) -> bool:
    return (initial - current) / initial >= 0.05
```

Displayed in UI as `↓ -X%` (green) or `= same` (neutral).

---

### 6. Streamlit UI — session state for reactivity

Streamlit reruns the script on every interaction. Products are loaded from SQLite on each rerun. The "Check All Prices" button triggers a re-scrape loop and updates the DB before the next rerender.

## Risks / Trade-offs

- **Anti-bot blocking** → `httpx` with realistic `User-Agent` and `Accept` headers reduces detection. Some sites (Amazon, ML) may still block. Mitigation: show a clear error message per product; don't crash the whole check.
- **LLM extraction failures** → LLM may hallucinate or fail to find price. Mitigation: validate extracted price is a parseable number; surface error in UI if not.
- **Price format edge cases** → Unusual formats (free products, "from $X", price ranges) may fail normalization. Mitigation: treat normalization failure as a scrape error; notify user.
- **Large HTML truncation** → Truncating at 8000 chars may cut off the price in some pages. Mitigation: prefer extracting the `<main>` or `<body>` visible text before truncating.
- **OPENAI_API_KEY not set** → Fallback path crashes. Mitigation: check at startup and show a Streamlit warning if missing; BS4-only mode still works for simple sites.
