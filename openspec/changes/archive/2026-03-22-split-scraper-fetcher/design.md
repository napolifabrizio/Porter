## Context

`scraper.py` currently conflates two responsibilities: making HTTP requests (headers, URL cleaning, curl_cffi) and parsing HTML into product data (BS4 selectors, LLM fallback, price normalization). This makes each concern harder to navigate in isolation.

## Goals / Non-Goals

**Goals:**
- Single-responsibility files: `fetcher.py` owns HTTP, `scraper.py` owns parsing
- `Scraper` receives `HttpFetcher` via constructor injection
- New `HtmlFetcher` protocol in `ports.py` to name the dependency explicitly
- No change to public behavior or the `ProductScraper` protocol

**Non-Goals:**
- Changing scraping strategy or adding new extraction methods
- Making `HttpFetcher` swappable at runtime (only at construction time)
- Adding tests (out of scope for this change)

## Decisions

### Inject `HttpFetcher` into `Scraper` rather than instantiating internally

`Scraper.__init__(self, fetcher: HtmlFetcher)` receives the fetcher as a dependency. `AppService` creates and wires `Scraper(fetcher=HttpFetcher())`.

**Alternatives considered:**
- Internal instantiation (`self._fetcher = HttpFetcher()` inside `__init__`): simpler wiring, but makes the dependency invisible and harder to replace in tests.
- Chosen approach makes the dependency explicit at the boundary without requiring changes to any caller beyond `AppService`.

### `HtmlFetcher` protocol lives in `ports.py`

The fetcher is a dependency of `Scraper`, which lives in the infrastructure layer. Defining it as a Protocol in `ports.py` follows the existing pattern (`ProductScraper`, `ProductRepository`) and avoids coupling `scraper.py` directly to `fetcher.py`.

### `_LLMProduct` stays in `scraper.py`

It is a private implementation detail of the LLM parsing path. Moving it to a separate file would add indirection without benefit.

## Risks / Trade-offs

- `AppService` wiring change is minimal but must be updated — forgetting it is the only realistic mistake → caught immediately at runtime (TypeError on construction)
- Slightly more files to navigate → offset by each file being shorter and focused
