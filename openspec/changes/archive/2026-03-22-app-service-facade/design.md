## Context

After the backend class refactor, `app.py` instantiates `Database`, `Scraper`, and `PriceChecker` at module level and calls methods on them directly. The UI layer is still coupled to three separate backend classes — it knows about the internal structure and is responsible for wiring them together. The goal is to move that responsibility into a dedicated facade so `app.py` only knows about one entry point.

## Goals / Non-Goals

**Goals:**
- Create `AppService` in `source/porter/service.py` as the single import for `app.py`
- `AppService` owns all backend wiring internally
- `AppService.track(url)` absorbs the scrape + save orchestration currently split across `app.py`
- `AppService.check_all_prices()` absorbs the `list_products` + `check_all_prices` call sequence
- `app.py` reduced to UI logic only — no backend imports beyond `AppService`

**Non-Goals:**
- No changes to any backend class (`Database`, `Scraper`, `PriceChecker`)
- No new public API, HTTP layer, or external interface
- No changes to `models.py` or return types

## Decisions

### D1: `AppService` owns instantiation of all backend classes

`AppService.__init__` creates `Database()`, `Scraper()`, and `PriceChecker(scraper, db)` internally. It does not accept them as constructor arguments.

**Alternatives considered:**
- Accept backend instances via DI — makes `AppService` testable in isolation, but the only consumer is `app.py` which has no need to swap implementations. Adds complexity with no current benefit.

**Rationale:** The point of `AppService` is to be the wiring hub. Pushing DI up to the caller (`app.py`) defeats the purpose.

### D2: `track(url)` merges scrape + save into one call

`app.py` currently calls `scraper.fetch_and_scrape(url)` then passes the result to `db.add_product(scraped, url)`. `AppService.track(url)` absorbs both steps and returns the saved `Product`.

**Rationale:** From the UI's perspective these are one operation — "add a product by URL". The split was an artifact of the UI knowing too much.

### D3: `check_all_prices()` takes no arguments

`app.py` currently loads `products` from the DB and passes them to `checker.check_all_prices(products)`. The facade loads products internally, so the caller just triggers the check and receives results.

**Rationale:** The UI has no reason to manage the product list before a check. Loading from DB is the only sensible source.

### D4: `check_selected(ids)` as a separate method for UI checkbox filtering

The "Check Selected" button in the UI passes a subset of product IDs from checkbox state. Rather than making `check_all_prices` accept an optional filter, a dedicated `check_selected(ids: list[int])` method was added. The facade loads all products, filters by ID, then delegates to `PriceChecker`.

**Rationale:** Keeps `check_all_prices()` clean and no-arg. The "selected" case is a distinct UI operation that deserves its own named method.

## Risks / Trade-offs

- [Thin public API] `AppService` exposes only three methods — if new UI features need finer-grained backend access, either `AppService` grows new methods or the abstraction leaks. → Mitigation: add methods to `AppService` as needed rather than bypassing it.
- [Streamlit reruns] Streamlit reruns the entire script on each interaction. `svc = AppService()` at module level means backend instances are recreated per rerun, same as before. No regression.
