## Why

Product names are scraped once at tracking time and are never editable, leaving users stuck with whatever title the scraper extracted — which is often truncated, ugly, or ambiguous. Users need a quick way to give products meaningful names without re-adding them.

## What Changes

- A product name can be edited inline from the product card in the UI.
- The backend exposes a new `PATCH /products/{id}` endpoint that accepts a new name.
- The database layer gains an `update_name` operation.

## Capabilities

### New Capabilities

- `product-rename`: Inline editing of a product's name from the product card, persisted via API.

### Modified Capabilities

- `tracker-ui`: Product card gains an editable name field (inline edit interaction).
- `product-storage`: Repository must support updating a product's name.

## Impact

- `App/src/components/ProductCard.tsx` — add inline edit UI
- `source/porter/app.py` — new `PATCH /products/{id}` route
- `source/porter/infrastructure/database.py` — new `update_name` method
- `source/porter/application/ports.py` — extend `ProductRepository` protocol
