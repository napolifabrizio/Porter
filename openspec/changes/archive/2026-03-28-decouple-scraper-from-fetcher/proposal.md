## Why

`Scraper` currently owns HTTP fetching (via `HtmlFetcher`) and HTML parsing in the same class, violating single responsibility and making it impossible to unit-test parsing logic without mocking the network. Separating the two allows passing raw HTML directly to the scraper in tests, and makes each class easier to reason about in isolation.

## What Changes

- `Scraper.__init__` no longer accepts a `fetcher: HtmlFetcher` parameter — the class becomes a pure parser
- `Scraper.fetch_and_scrape(url)` is replaced by `Scraper.scrape(html: str)` — callers are responsible for providing HTML
- `ProductScraper` protocol is updated to match: `scrape(html: str) -> ScrapedData`
- `PriceChecker.__init__` gains a `fetcher: HtmlFetcher` parameter — it fetches HTML before delegating to the scraper
- `AppService` stores the `HttpFetcher` instance and fetches HTML itself in `track()` before calling `scraper.scrape(html)`
- **BREAKING**: `ProductScraper` protocol method signature changes from `fetch_and_scrape(url)` to `scrape(html)`

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `product-scraping`: `ProductScraper` protocol method changes from `fetch_and_scrape(url: str)` to `scrape(html: str)`; `Scraper` no longer accepts `HtmlFetcher` via constructor injection
- `price-checking`: `PriceChecker` constructor gains a `fetcher: HtmlFetcher` parameter; it fetches HTML before calling `scraper.scrape(html)`

## Impact

- `source/porter/infrastructure/scraper.py` — remove `__init__`, rename/replace `fetch_and_scrape`
- `source/porter/application/ports.py` — update `ProductScraper` protocol signature
- `source/porter/application/checker.py` — add `fetcher` param, fetch before scraping
- `source/porter/application/service.py` — store fetcher, fetch in `track()`, update wiring
