# Application Layer

The `application/` folder is the **use-case layer** of Porter's Clean Architecture. It sits between the UI and the domain/infrastructure, orchestrating how the system responds to user actions without owning any I/O or business rules itself.

## What lives here

### `ports.py` — Abstractions (interfaces)
Defines three `Protocol` classes that describe *what the application needs* from the outside world, without caring about the concrete implementation.

### `checker.py` — Price-check orchestrator
`PriceChecker` receives the three ports via constructor injection and executes the price-check workflow:

1. Fetches the current HTML for each product.
2. Scrapes the price from that HTML.
3. Persists the new price via the repository.
4. Delegates to `domain/price_rules.py` to evaluate drop/rise.
5. Returns a `CheckResult` per product.

All products are checked **in parallel** using a `ThreadPoolExecutor` (up to 10 workers).

### `service.py` — Application facade
`AppService` is the single entry point used by the UI. It wires together the concrete infrastructure implementations and exposes high-level methods:

| Method | What it does |
|---|---|
| `track(url)` | Scrapes a new URL and adds it to the watchlist |
| `list_products()` | Returns all tracked products |
| `check_all_prices()` | Runs a price check for every tracked product |
| `check_selected(ids)` | Runs a price check for a specific subset |
| `remove_product(id)` | Deletes a product from the watchlist |

It also caches the product list in memory (`_products`) to avoid redundant DB reads within the same session.

## Dependency direction

```
ui/app.py
    └── AppService (service.py)
            ├── PriceChecker (checker.py)
            │       └── ports.py  ←  fulfilled by infrastructure/
            └── domain/price_rules.py
```

The application layer imports from `domain` and `ports`, but **never from infrastructure directly** (except `AppService`, which is the composition root).

---

## Adding a new use case

When you need to add a new capability to the application layer (e.g. a new workflow, a new port, a new facade method), follow these four steps:

### Step 1 — Define the port in `application/ports.py` (if new I/O is needed)

If the use case requires a new external capability (network, storage, third-party API), add a `Protocol` in `ports.py`. If the use case only composes existing ports, skip this step.

```python
# application/ports.py
class NotificationSender(Protocol):
    def send(self, message: str, recipient: str) -> None: ...
```

Ports describe *what the application needs* — no implementation detail, no infrastructure imports. Keep them minimal: one method per responsibility.

### Step 2 — Implement the orchestrator in `application/`

Add a new file for the use case. The class receives its dependencies via constructor injection (the ports it needs) and contains only orchestration logic — no I/O of its own.

```python
# application/notifier.py
class PriceAlertNotifier:
    def __init__(self, sender: NotificationSender, repo: ProductRepository):
        self._sender = sender
        self._repo = repo

    def notify_drops(self, results: list[CheckResult]) -> None:
        for result in results:
            if result.dropped:
                self._sender.send(...)
```

Rules for orchestrators:
- Depend only on ports (`ports.py`) and domain (`domain/`), never on concrete infrastructure.
- No business rules here — delegate decisions to `domain/`.
- Parallelism via `ThreadPoolExecutor` is acceptable when operations are independent (see `checker.py`).

### Step 3 — Expose it via `AppService`

`AppService` is the **only** place that wires concrete implementations to orchestrators. Add the new orchestrator and expose a public method for the UI.

```python
# application/service.py
class AppService:
    def __init__(self):
        self._fetcher = HttpFetcher()
        self._scraper = Scraper()
        self._db = Database()
        self._checker = PriceChecker(self._scraper, self._db, self._fetcher)
        self._notifier = PriceAlertNotifier(EmailSender(), self._db)  # new

    def notify_price_drops(self) -> None:   # new public method
        results = self._checker.check_all()
        self._notifier.notify_drops(results)
```

`AppService` methods should be thin — one call to the relevant orchestrator, nothing more.

### Step 4 — Conventions

**What belongs in the application layer:**
- Orchestration: sequencing calls across ports and domain objects.
- Parallelism decisions (e.g. `ThreadPoolExecutor`).
- Input validation that spans multiple domain concepts.

**What does NOT belong here:**
- Business rules — those live in `domain/`.
- I/O — that lives in `infrastructure/` behind a port.
- UI concerns — those live in `ui/`.

**Error handling:** let domain exceptions (`ValueError`) and infrastructure exceptions (`RuntimeError`) propagate to the UI unchanged. The application layer does not catch and re-wrap — it only raises its own errors for orchestration-level failures (e.g. a required port returns an unexpected `None`).
