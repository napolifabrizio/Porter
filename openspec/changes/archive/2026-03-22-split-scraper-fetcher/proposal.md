## Why

`scraper.py` currently handles two distinct concerns — HTTP fetching and HTML parsing — making each harder to read and reason about in isolation. Separating them improves clarity and makes each file single-purpose.

## What Changes

- New file `infrastructure/fetcher.py` with `HttpFetcher` class: browser headers, URL cleaning, and HTTP request logic via `curl_cffi`
- `infrastructure/scraper.py` becomes parsing-only: BS4 extraction, LLM fallback, price normalization, and the `fetch_and_scrape` facade
- `Scraper.__init__` accepts an injected `HtmlFetcher` dependency
- New `HtmlFetcher` protocol added to `application/ports.py`
- `AppService` updated to wire `Scraper(fetcher=HttpFetcher())`

## Capabilities

### New Capabilities

- `html-fetching`: HTTP fetching concern extracted into its own class — browser headers, URL cleaning, error handling, and `curl_cffi` request logic

### Modified Capabilities

- `product-scraping`: `Scraper` now receives an `HtmlFetcher` via constructor injection instead of performing HTTP requests internally

## Impact

- `source/porter/infrastructure/scraper.py` — reduced to parsing concerns only
- `source/porter/infrastructure/fetcher.py` — new file
- `source/porter/application/ports.py` — new `HtmlFetcher` protocol
- `source/porter/application/service.py` — wiring updated to inject `HttpFetcher` into `Scraper`
- No changes to public behavior or the `ProductScraper` protocol
