## 1. Create folder structure

- [x] 1.1 Create `source/porter/domain/__init__.py`
- [x] 1.2 Create `source/porter/application/__init__.py`
- [x] 1.3 Create `source/porter/infrastructure/__init__.py`
- [x] 1.4 Create `source/porter/ui/__init__.py`

## 2. Domain layer

- [x] 2.1 Create `source/porter/domain/price_rules.py` with `DROP_THRESHOLD = 0.05` and `evaluate_price_drop(initial: float, current: float) -> tuple[bool, float]`

## 3. Application layer — ports

- [x] 3.1 Create `source/porter/application/ports.py` with `ProductScraper` Protocol (`fetch_and_scrape(url: str) -> ScrapedData`)
- [x] 3.2 Add `ProductRepository` Protocol to `ports.py` with `init_db`, `add_product`, `list_products`, `update_price`

## 4. Application layer — checker

- [x] 4.1 Create `source/porter/application/checker.py` — move `CheckResult` and `PriceChecker` from flat `checker.py`
- [x] 4.2 Update `PriceChecker.__init__` to accept `ProductScraper` and `ProductRepository` instead of concrete classes
- [x] 4.3 Update `PriceChecker.check_all_prices` to delegate drop evaluation to `domain.price_rules.evaluate_price_drop`

## 5. Application layer — service

- [x] 5.1 Create `source/porter/application/service.py` — move `AppService` from flat `service.py`
- [x] 5.2 Update `AppService` imports to use `infrastructure.database.Database`, `infrastructure.scraper.Scraper`, and `application.checker.PriceChecker`

## 6. Infrastructure layer

- [x] 6.1 Create `source/porter/infrastructure/database.py` — move `Database` class from flat `database.py` (no logic changes)
- [x] 6.2 Create `source/porter/infrastructure/scraper.py` — move `Scraper` class from flat `scraper.py` (no logic changes)

## 7. UI layer

- [x] 7.1 Create `source/porter/ui/app.py` — move `app.py` content, update import to `from porter.application.service import AppService`

## 8. Cleanup and wiring

- [x] 8.1 Delete old flat files: `checker.py`, `service.py`, `database.py`, `scraper.py`, `app.py`
- [x] 8.2 Update `CLAUDE.md` project layout section to reflect new folder structure and entry point
- [x] 8.3 Update README / pyproject.toml entry point from `source/porter/app.py` to `source/porter/ui/app.py`
- [x] 8.4 Smoke-test the app end-to-end (`poetry run streamlit run source/porter/ui/app.py`)
