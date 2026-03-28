## 1. Update Protocol

- [x] 1.1 In `porter/application/ports.py`, rename `ProductScraper.fetch_and_scrape(url: str)` to `scrape(html: str) -> ScrapedData`

## 2. Refactor Scraper

- [x] 2.1 Remove `__init__(self, fetcher: HtmlFetcher)` and `self._fetcher` from `Scraper`
- [x] 2.2 Rename `fetch_and_scrape(self, url: str)` to `scrape(self, html: str)` and remove the `self._fetcher.fetch(url)` call
- [x] 2.3 Remove the `HtmlFetcher` import from `scraper.py` (no longer needed)

## 3. Update PriceChecker

- [x] 3.1 Add `fetcher: HtmlFetcher` parameter to `PriceChecker.__init__` and store as `self._fetcher`
- [x] 3.2 In `_check_one`, call `html = self._fetcher.fetch(product.url)` before `self._scraper.scrape(html)`

## 4. Update AppService (composition root)

- [x] 4.1 Store `self._fetcher = HttpFetcher()` in `AppService.__init__`
- [x] 4.2 Pass `self._fetcher` to `PriceChecker` constructor
- [x] 4.3 In `AppService.track(url)`, fetch HTML via `self._fetcher.fetch(url)` and pass to `self._scraper.scrape(html)`
- [x] 4.4 Remove `Scraper(fetcher=HttpFetcher())` — replace with `Scraper()`
