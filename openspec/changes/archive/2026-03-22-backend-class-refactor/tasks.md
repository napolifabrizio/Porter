## 1. Refactor Database

- [x] 1.1 Wrap `database.py` in a `Database` class with `__init__(self, db_path: Path = Path("porter.db"))`
- [x] 1.2 Move `_connect` to a private instance method `_connect(self)`
- [x] 1.3 Convert `init_db`, `add_product`, `list_products`, `update_price` to instance methods
- [x] 1.4 Remove module-level `DB_PATH` constant (now an instance attribute)

## 2. Refactor Scraper

- [x] 2.1 Wrap `scraper.py` in a `Scraper` class with `__init__(self)`
- [x] 2.2 Move `BROWSER_HEADERS` to a private class attribute `_BROWSER_HEADERS`
- [x] 2.3 Convert `normalize_price` to a private static method `_normalize_price`
- [x] 2.4 Convert `scrape_with_bs4` and `scrape_with_llm` to private instance methods
- [x] 2.5 Convert `fetch_and_scrape` to a public instance method

## 3. Refactor PriceChecker

- [x] 3.1 Wrap `checker.py` in a `PriceChecker` class with `__init__(self, scraper: Scraper, db: Database)`
- [x] 3.2 Store `scraper` and `db` as instance attributes
- [x] 3.3 Convert `check_all_prices` to an instance method using `self._scraper` and `self._db`
- [x] 3.4 Keep `DROP_THRESHOLD = 0.05` as a public class attribute

## 4. Update App Wiring

- [x] 4.1 In `app.py`, instantiate `Database`, `Scraper`, and `PriceChecker` at module level
- [x] 4.2 Replace all bare function calls with method calls on the instances
