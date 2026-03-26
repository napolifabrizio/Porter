## Why

Price checks run sequentially today — each product waits for the previous one to finish fetching and scraping. With N products, check time grows linearly (~3-5s per product), making the UI feel slow as the watchlist grows.

## What Changes

- `PriceChecker.check_all_prices()` runs all product checks concurrently using a thread pool instead of sequentially
- Results are returned in the same order as the input product list
- A failed check for one product does not affect others (errors are isolated per product)

## Capabilities

### New Capabilities

- None

### Modified Capabilities

- `price-checking`: The `check_all_prices` operation now executes concurrently (all products at the same time) rather than sequentially. Error isolation and result ordering guarantees are added to the spec.

## Impact

- `source/porter/application/checker.py` — only file changed
- No changes to ports, database, scraper, UI, or models
- Adds `concurrent.futures` from Python stdlib (no new dependencies)
