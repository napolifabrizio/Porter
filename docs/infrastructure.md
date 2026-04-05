# Infrastructure Layer

The `infrastructure/` folder contains the **concrete implementations** of the ports defined in `application/ports.py`. This is where all real I/O happens: HTTP requests, HTML parsing, LLM calls, and SQLite persistence.

Nothing in the domain or application layers imports from here directly — except `AppService`, which is the composition root that wires everything together.

## What lives here

### `fetcher.py` — `HttpFetcher` (implements `HtmlFetcher`)
Fetches raw HTML from a product URL using `curl_cffi`, which impersonates a real Chrome browser to bypass basic bot-detection.

### `scraper.py` — `Scraper` (implements `ProductScraper`)
Extracts product name, price, and description from raw HTML using a **three-stage hybrid strategy**, tried in order:

| Stage | Method | When it runs |
|---|---|---|
| 1 | **JSON-LD** (`_scrape_with_json_ld`) | Always first — parses `<script type="application/ld+json">` structured data |
| 2 | **BeautifulSoup CSS selectors** (`_scrape_with_bs4`) | Fallback when JSON-LD yields nothing — targets common e-commerce price/name patterns |
| 3 | **LLM** (`_scrape_with_llm`) | Last resort — strips the HTML to plain text and asks GPT-4o-mini to extract the data |

The LLM path sets `scraped_by_llm=True` on the returned `ScrapedData` so the UI can surface a warning.

A shared `_normalize_price` method handles locale-aware price strings (`R$ 1.299,99`, `$12.99`, `€1,299.00`, etc.).

### `database.py` — `Database` (implements `ProductRepository`)
SQLite persistence layer. Stores all products in a single `products` table created on first run (`init_db`).

## Dependency direction

```
infrastructure/
    fetcher.py   →  fulfills HtmlFetcher port
    scraper.py   →  fulfills ProductScraper port
    database.py  →  fulfills ProductRepository port
```

The infrastructure layer depends on the application ports (inward), never the other way around.

---

## Adding a new infrastructure implementation

When you need to replace or add a concrete implementation of a port (e.g. swap the HTTP fetcher, add a second database backend, introduce a new scraper strategy), follow these four steps:

### Step 1 — Define or reuse the port in `application/ports.py`

If the capability doesn't exist yet, add a new `Protocol` there. If you're replacing an existing one, the port stays unchanged.

```python
# application/ports.py
class HtmlFetcher(Protocol):
    def fetch(self, url: str) -> str: ...
```

The protocol only describes *what* is needed — no implementation detail, no imports from infrastructure.

### Step 2 — Create the implementation in `infrastructure/`

Add a new file (or class) inside `infrastructure/`. The class must satisfy the port's interface via structural subtyping (duck typing — no `implements` keyword needed).

```python
# infrastructure/playwright_fetcher.py
class PlaywrightFetcher:
    def fetch(self, url: str) -> str:
        ...  # Playwright-based implementation
```

Naming convention: Port = `HtmlFetcher` → Implementation = `HttpFetcher` / `PlaywrightFetcher`. Keep names descriptive of the mechanism, not the port.

### Step 3 — Wire it in `AppService` (the composition root)

`AppService.__init__` is the **only** place that instantiates infrastructure classes. Swap or add the implementation there.

```python
# application/service.py  ← only file allowed to import from infrastructure
class AppService:
    def __init__(self):
        self._fetcher = PlaywrightFetcher()   # was HttpFetcher
        self._scraper = Scraper()
        self._db = Database()
        self._checker = PriceChecker(self._scraper, self._db, self._fetcher)
```

No other file should import from `infrastructure/`.

### Step 4 — Error handling conventions

Raise `RuntimeError` for I/O failures (network errors, timeouts, HTTP errors). Raise `ValueError` for domain-level violations (e.g. duplicate URL on insert). Never let library-specific exceptions (e.g. `curl_cffi.RequestException`, `sqlite3.IntegrityError`) leak out of the infrastructure layer — catch and re-raise as the appropriate standard exception.

```python
# Good — wraps library-specific error
except curl_requests.exceptions.Timeout:
    raise RuntimeError(f"Request timed out: {url}")

# Good — wraps DB constraint as domain violation
except sqlite3.IntegrityError:
    raise ValueError(f"Product with URL already tracked: {url}")
```

---