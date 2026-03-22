## Context

The three backend modules (`scraper.py`, `database.py`, `checker.py`) consist of flat module-level functions and constants. The `checker` module already depends on both `scraper` and `database` by importing their functions directly — this coupling is implicit and cannot be swapped or tested in isolation. The refactor wraps each module in a single class, makes the `PriceChecker` dependency on `Scraper` and `Database` explicit via constructor injection, and carries `db_path` as instance state on `Database`.

## Goals / Non-Goals

**Goals:**
- Wrap `scraper.py`, `database.py`, and `checker.py` in service classes
- Make `PriceChecker` receive `Scraper` and `Database` via constructor (DI)
- Carry `db_path` as `Database` instance state
- Make all internal helpers private (prefix `_`)
- Update `app.py` wiring to instantiate and connect the classes

**Non-Goals:**
- No logic changes of any kind
- No changes to `models.py`
- No new tests, no new dependencies
- No changes to the Streamlit UI beyond the wiring update

## Decisions

### D1: Dependency Injection over internal instantiation

`PriceChecker` receives `Scraper` and `Database` as constructor arguments rather than creating them internally.

**Alternatives considered:**
- Internal instantiation (`self._scraper = Scraper()` inside `__init__`) — simpler but hides dependencies and makes future testing harder.

**Rationale:** Explicit dependencies are easier to trace and swap. The wiring cost in `app.py` is trivial.

### D2: `db_path` as constructor parameter with default

`Database.__init__(self, db_path: Path = Path("porter.db"))` — keeps existing behavior by default, but allows overriding (e.g., for a test database).

**Rationale:** No behavior change for the app; the default matches the current hardcoded path. Passing a different path in the future requires no structural change.

### D3: `_normalize_price` as a private static method on `Scraper`

`normalize_price` is currently a public module-level function. It is only used internally within `scraper.py`. Moving it to `Scraper._normalize_price` (static method) signals it is an implementation detail.

**Rationale:** Nothing outside `scraper.py` calls it. Keeping it public would expose unnecessary surface area.

### D4: `BROWSER_HEADERS` as a class-level constant on `Scraper`

The dict becomes `Scraper._BROWSER_HEADERS` — a private class attribute.

**Rationale:** It is implementation detail of the scraper, not a public API.

### D5: `DROP_THRESHOLD` as a class-level constant on `PriceChecker`

`DROP_THRESHOLD = 0.05` becomes `PriceChecker.DROP_THRESHOLD` — kept public so callers (e.g., UI) can display the threshold without hardcoding it.

## Risks / Trade-offs

- `app.py` instantiation order matters: `Database` and `Scraper` must be created before `PriceChecker`. This is a one-time setup at module level in `app.py` — low risk.
- Any external code importing `fetch_and_scrape`, `add_product`, etc. as bare functions will break. Scope is limited to `app.py` in this project.
