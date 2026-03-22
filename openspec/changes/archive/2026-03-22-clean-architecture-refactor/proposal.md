## Why

The codebase currently mixes business logic with infrastructure concerns — `PriceChecker` directly depends on `Scraper` (HTTP/LLM) and `Database` (SQLite), making the domain rules impossible to test or reason about in isolation. As the project grows and new scraping strategies or storage backends may be introduced, the lack of clear layer boundaries will make changes risky and difficult.

## What Changes

- Restructure `source/porter/` into four explicit layers: `domain/`, `application/`, `infrastructure/`, and `ui/`
- Extract the pure price-drop business rule into a `domain/` module with no external dependencies
- Introduce `Protocol` interfaces (ports) for the scraper and repository so the application layer depends on abstractions, not concretions
- Move `Scraper` and `Database` into `infrastructure/` as concrete adapters
- Move orchestration logic (`PriceChecker`, `AppService`) into `application/`
- Move `app.py` into `ui/`
- **BREAKING**: Internal module import paths change throughout the codebase

## Capabilities

### New Capabilities

- `layered-architecture`: Defines the four-layer structure (domain, application, infrastructure, ui) and the dependency rule: outer layers depend on inner layers, never the reverse

### Modified Capabilities

- `price-checking`: The price-drop rule moves into `domain/`; `PriceChecker` becomes an application-layer orchestrator that depends on protocols, not concretions
- `product-scraping`: `Scraper` moves to `infrastructure/` and implements a `ProductScraper` protocol defined in `application/`
- `product-storage`: `Database` moves to `infrastructure/` and implements a `ProductRepository` protocol defined in `application/`
- `app-service`: `AppService` moves to `application/` and is wired up via dependency injection in `ui/app.py`

## Impact

- All internal imports across `source/porter/` change
- `pyproject.toml` package path unchanged (`source/porter/` root stays)
- No changes to external behavior, API, or the SQLite schema
- `models.py` stays flat at the `porter/` root (shared across all layers)
