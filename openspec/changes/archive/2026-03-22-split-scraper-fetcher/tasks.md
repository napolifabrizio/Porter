## 1. Add HtmlFetcher protocol to ports

- [x] 1.1 Add `HtmlFetcher` Protocol to `porter.application.ports` with method `fetch(url: str) -> str`

## 2. Create HttpFetcher in infrastructure

- [x] 2.1 Create `source/porter/infrastructure/fetcher.py` with `HttpFetcher` class
- [x] 2.2 Move `_BROWSER_HEADERS`, `_TRACKING_PARAMS`, and `_clean_url()` from `scraper.py` into `HttpFetcher`
- [x] 2.3 Implement `HttpFetcher.fetch(url: str) -> str` with curl_cffi request, error handling, and URL cleaning

## 3. Refactor Scraper to parsing-only

- [x] 3.1 Remove HTTP-related attributes and methods from `Scraper` (`_BROWSER_HEADERS`, `_TRACKING_PARAMS`, `_clean_url`, curl_cffi imports)
- [x] 3.2 Add `__init__(self, fetcher: HtmlFetcher)` to `Scraper` storing `self._fetcher`
- [x] 3.3 Update `fetch_and_scrape` to call `self._fetcher.fetch(url)` instead of performing the HTTP request directly

## 4. Update wiring in AppService

- [x] 4.1 Update `AppService` in `service.py` to instantiate `Scraper(fetcher=HttpFetcher())` and import both classes
