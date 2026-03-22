## Context

Porter currently has a flat module structure under `source/porter/`. `PriceChecker` directly imports and depends on the concrete `Scraper` and `Database` classes, coupling business logic to infrastructure. As the project grows (new scraping strategies, notification backends, alternative storage), this makes changes risky and the domain rules untestable in isolation.

The refactor introduces a four-layer architecture without changing any external behavior, API surface, or database schema.

## Goals / Non-Goals

**Goals:**
- Separate domain rules, application orchestration, infrastructure, and UI into explicit folders
- Make `PriceChecker` depend on `Protocol` abstractions instead of concrete classes
- Extract pure price-drop logic into a dependency-free `domain/` module
- Keep `models.py` flat at the `porter/` root (shared across all layers)
- Zero behavior changes — all existing tests and UI interactions remain identical

**Non-Goals:**
- Swapping out the actual SQLite or HTTP implementations (that's a future change)
- Introducing a dependency injection framework
- Adding new features or changing the public API of `AppService`
- Moving `models.py` into `domain/` (out of scope per proposal)

## Decisions

### 1. Use `typing.Protocol` for ports, not ABCs

**Decision**: Define `ProductRepository` and `ProductScraper` as `Protocol` classes in `application/ports.py`.

**Rationale**: Protocols use structural subtyping — the infrastructure classes don't need to explicitly inherit from the protocol. This avoids import cycles (infrastructure importing from application just to declare `class Database(ProductRepository)`) and is more idiomatic modern Python.

**Alternative considered**: `abc.ABC` with explicit inheritance. Rejected because it requires infrastructure to import from application, which reverses the intended dependency direction or creates coupling.

---

### 2. Four-layer folder structure

**Decision**:
```
source/porter/
  models.py                  # shared value objects, stays flat
  domain/
    __init__.py
    price_rules.py           # DROP_THRESHOLD, evaluate_price_drop()
  application/
    __init__.py
    ports.py                 # ProductRepository + ProductScraper Protocols
    checker.py               # PriceChecker — orchestrates via ports
    service.py               # AppService facade
  infrastructure/
    __init__.py
    database.py              # Database — concrete SQLite impl
    scraper.py               # Scraper — concrete HTTP+LLM impl
  ui/
    __init__.py
    app.py                   # Streamlit entry point
```

**Dependency rule**: `domain` ← `application` ← `infrastructure` ← `ui`. Inner layers never import from outer layers.

**Rationale**: Makes layer boundaries visible in the filesystem. Any import violation is immediately obvious from the path.

---

### 3. AppService self-wires concrete infrastructure classes

**Decision**: `AppService.__init__` continues to instantiate `Database` and `Scraper` directly and pass them into `PriceChecker`. The UI still just does `AppService()`.

**Rationale**: Keeps the UI completely unchanged. The value of this refactor is that `PriceChecker` is now testable with mock implementations of the protocols — not that `AppService` is injectable. Full DI framework is overkill for this project size.

**Alternative considered**: Passing infrastructure instances into `AppService.__init__` from `app.py`. Deferred — easy to do later if needed.

---

### 4. `CheckResult` stays in `application/checker.py`

**Decision**: The `CheckResult` dataclass lives alongside `PriceChecker` in `application/checker.py`.

**Rationale**: It's an output DTO of the application layer, not a domain concept. The domain only knows about prices and thresholds, not check results.

## Risks / Trade-offs

- [Import path breakage] All internal `from porter.X import Y` paths change → Mitigation: update all imports as part of the migration, run app end-to-end after
- [Streamlit entry point] `poetry run streamlit run source/porter/app.py` must become `source/porter/ui/app.py` → Mitigation: update `pyproject.toml` scripts or README accordingly
- [Flat `__init__.py`s] Re-exporting from `porter/__init__.py` could hide layer violations → Mitigation: keep `__init__.py` files empty

## Migration Plan

1. Create folder structure (`domain/`, `application/`, `infrastructure/`, `ui/`)
2. Create `domain/price_rules.py` — pure function, no deps
3. Create `application/ports.py` — Protocol definitions
4. Move and update `checker.py` → `application/checker.py` (use protocols + domain)
5. Move and update `service.py` → `application/service.py`
6. Move `database.py` → `infrastructure/database.py` (no logic changes)
7. Move `scraper.py` → `infrastructure/scraper.py` (no logic changes)
8. Move `app.py` → `ui/app.py` (update import path only)
9. Update all cross-module imports
10. Update entry point reference in README / pyproject.toml
11. Delete old flat files
