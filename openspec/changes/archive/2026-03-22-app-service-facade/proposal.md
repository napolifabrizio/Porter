## Why

`app.py` currently imports and wires three backend classes directly (`Database`, `Scraper`, `PriceChecker`), coupling the UI layer to the internal backend structure. Introducing a single facade class (`AppService`) decouples the frontend from backend internals — `app.py` imports one class and calls high-level operations, while all wiring and orchestration live in the service layer.

## What Changes

- New file `source/porter/service.py` with class `AppService`
- `AppService.__init__` instantiates and wires `Database`, `Scraper`, and `PriceChecker` internally
- `AppService.track(url)` — scrapes and saves a product in one call (replaces separate `fetch_and_scrape` + `add_product` calls in `app.py`)
- `AppService.list_products()` — delegates to `Database.list_products()`
- `AppService.check_all_prices()` — loads products internally, delegates to `PriceChecker.check_all_prices()` (no argument from caller)
- `app.py` updated: replaces all backend imports and wiring with `from porter.service import AppService` and a single `svc = AppService()` instance

## Capabilities

### New Capabilities

- `app-service`: Facade class that exposes high-level tracker operations to the UI layer, encapsulating backend wiring and orchestration

### Modified Capabilities

- None — existing backend behavior is unchanged; `tracker-ui` implementation changes but its requirements do not

## Impact

- New file: `source/porter/service.py`
- Modified: `source/porter/app.py` — imports and call sites updated
- No changes to `database.py`, `scraper.py`, `checker.py`, or `models.py`
- No new dependencies
