## Why

The backend modules (`scraper.py`, `database.py`, `checker.py`) are implemented as flat collections of functions with module-level constants. Wrapping them in classes improves cohesion, makes dependencies explicit, and enables proper dependency injection — particularly important as `PriceChecker` depends on both `Scraper` and `Database`.

## What Changes

- `scraper.py`: New `Scraper` class encapsulating all scraping logic; `_normalize_price` and internal BS4/LLM helpers become private methods; `fetch_and_scrape` becomes the public entry point
- `database.py`: New `Database` class carrying `db_path` as instance state; all DB helpers become instance methods
- `checker.py`: New `PriceChecker` class receiving `Scraper` and `Database` via constructor (dependency injection); `check_all_prices` becomes an instance method
- `app.py`: Updated wiring — instantiates `Database`, `Scraper`, and `PriceChecker`, then calls methods on them

## Capabilities

### New Capabilities

- None

### Modified Capabilities

- `product-scraping`: Internal structure changes — functions replaced by `Scraper` class with private helpers; public interface is now `Scraper().fetch_and_scrape(url)`
- `product-storage`: Internal structure changes — functions replaced by `Database` class with instance `db_path`; public interface is now instance methods on `Database`
- `price-checking`: Internal structure changes — function replaced by `PriceChecker` class accepting `Scraper` and `Database` dependencies; public interface is now `PriceChecker(scraper, db).check_all_prices(products)`

## Impact

- `source/porter/scraper.py` — full rewrite to class
- `source/porter/database.py` — full rewrite to class
- `source/porter/checker.py` — full rewrite to class
- `source/porter/app.py` — updated to instantiate and wire classes
- No changes to `models.py`, no logic changes anywhere, no new dependencies
