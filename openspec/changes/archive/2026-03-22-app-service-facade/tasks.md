## 1. Create AppService

- [x] 1.1 Create `source/porter/service.py` with `AppService` class
- [x] 1.2 Implement `__init__` — instantiate `Database`, `Scraper`, and `PriceChecker` internally
- [x] 1.3 Implement `track(url: str) -> Product` — calls `_scraper.fetch_and_scrape` then `_db.add_product`
- [x] 1.4 Implement `list_products() -> list[Product]` — delegates to `_db.list_products()`
- [x] 1.5 Implement `check_all_prices() -> list[CheckResult]` — loads products internally, delegates to `_checker.check_all_prices(products)`

## 2. Update app.py

- [x] 2.1 Replace `Database`, `Scraper`, `PriceChecker` imports with `from porter.service import AppService`
- [x] 2.2 Replace the three instantiation lines with `svc = AppService()` and remove `db.init_db()` call (move `init_db` into `AppService.__init__`)
- [x] 2.3 Replace `scraper.fetch_and_scrape(url)` + `db.add_product(scraped, url)` with `svc.track(url)`
- [x] 2.4 Replace all `db.list_products()` calls with `svc.list_products()`
- [x] 2.5 Replace `checker.check_all_prices(products)` / `checker.check_all_prices(selected_products)` with `svc.check_all_prices()` / `svc.check_selected(ids)` — added `check_selected` method to handle UI checkbox filtering
