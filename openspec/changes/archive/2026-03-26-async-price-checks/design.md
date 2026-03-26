## Context

`PriceChecker.check_all_prices()` currently iterates over products sequentially. Each iteration blocks on a network fetch (2-5s), so checking N products takes N × fetch time. The fix is to run all checks concurrently.

The stack is synchronous: `httpx` sync client, LangChain's `.invoke()`, SQLite via `sqlite3`. The `Database` class opens a new connection per operation (`_connect()`), so concurrent writes from multiple threads are safe without any connection sharing.

## Goals / Non-Goals

**Goals:**
- All product checks execute concurrently (wall-clock time ≈ slowest single check)
- Results returned in same order as input `products` list
- One product's failure does not affect others
- No new dependencies (stdlib `concurrent.futures` only)
- No changes outside `checker.py`

**Non-Goals:**
- Switching to `asyncio` / async I/O
- Streaming partial results to the UI as checks complete
- Configurable concurrency limits exposed to the user

## Decisions

### Use `ThreadPoolExecutor` over `asyncio`

`asyncio` would require propagating `async/await` through `HtmlFetcher`, `Scraper`, and `PriceChecker`, and bridging into Streamlit's sync event loop via `asyncio.run()` or `nest_asyncio`. `ThreadPoolExecutor` localizes the change to a single method in `checker.py` with zero protocol changes.

**Alternatives considered:** `asyncio.gather` — discarded due to cascade of async changes needed.

### Cap thread pool at `min(10, len(products))`

Creates no more threads than products, and caps at 10 to avoid hammering target sites or exhausting OS thread limits for large watchlists.

### Preserve input order via index mapping

`as_completed()` returns futures in completion order. To guarantee input order, futures are stored in a `dict[Future → int]` and results written into a pre-sized list by index.

## Risks / Trade-offs

- **SQLite write contention** → Each `_connect()` call creates a new connection; SQLite serializes concurrent writes via file locking. With small watchlists (typical usage), contention is negligible.
- **Target site rate limiting** → Simultaneous requests from the same IP may trigger rate limits on some retailers. Mitigation: the 10-thread cap limits concurrency; no further mitigation needed for a personal tool.
- **Thread overhead for 1 product** → `min(10, len(products))` avoids creating a pool when there's nothing to parallelize.
