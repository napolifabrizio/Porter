## Why

All tracked products live in a single flat list, making it hard to organise a watchlist that spans multiple categories (e.g. groceries, electronics, vehicles). Users need a way to group products into named lists so they can focus on one category at a time.

## What Changes

- Users can create and delete named lists (e.g. "Foods", "Cars").
- Every product belongs to exactly one list; a built-in **Standard** list always exists and cannot be deleted.
- When adding a product, users pick which list it goes into (defaults to Standard).
- Products can be moved between lists at any time.
- When a list is deleted its products are moved back to Standard.
- The sidebar shows the available lists; clicking one filters the product view to that list only.
- "Check All Prices" always checks every product regardless of which list is active.
- The `products` table gains a `list_id` FK column; a new `lists` table is introduced. **BREAKING**: existing databases are migrated automatically on first run.

## Capabilities

### New Capabilities

- `watchlist-management`: Create, delete, and list named watchlists; enforce the Standard list invariant; move products between lists.

### Modified Capabilities

- `product-storage`: `products` table gains `list_id` FK; new `lists` table; `add_product` and `list_products` accept list context.
- `tracker-ui`: Sidebar gains list navigation; track form gains list selector; product cards gain move-to-list control.
- `app-service`: New orchestration methods for list management; `track()` and `list_products()` accept an optional `list_id`.

## Impact

- **infrastructure/database.py** — schema migration, new list CRUD methods, FK enforcement via `PRAGMA foreign_keys = ON`.
- **models.py** — new `WatchList` model; `Product` gains `list_id: int` field.
- **application/ports.py** — new `WatchListRepository` Protocol; `ProductRepository` extended with list-aware signatures.
- **application/service.py** — new list management methods; `track()` and `list_products()` updated.
- **ui/app.py** — sidebar, track form, and product loop all updated.
- **porter.db** — one-time non-destructive migration (adds column, inserts Standard list, back-fills existing products).
