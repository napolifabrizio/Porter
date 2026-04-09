## Context

Porter currently stores all products in a single flat SQLite table (`products`). There is no concept of grouping; `list_products()` always returns everything. The UI renders them all in one undifferentiated list.

We are introducing named watchlists so users can segment their tracking (e.g. "Foods", "Cars"). A built-in **Standard** list acts as the default and catch-all; it can never be deleted. Every product belongs to exactly one list at all times.

The change touches all four layers: infrastructure (new `lists` table + FK), models (new `WatchList`, updated `Product`), application (new service methods + updated ports), and UI (sidebar nav, track form, product card).

---

## Goals / Non-Goals

**Goals:**
- Users can create and delete named lists.
- Products are assigned to a list at add-time; they can be moved later.
- Sidebar shows available lists; selecting one filters the product view.
- Existing `porter.db` databases are migrated automatically — no data loss.
- Standard list always exists and cannot be deleted; products from a deleted list fall back to it.

**Non-Goals:**
- Many-to-many (a product in multiple lists) — one list per product is sufficient for a personal tracker.
- A global "All Products" view — only per-list views.
- List ordering or nesting.
- Sharing or exporting lists.

---

## Decisions

### 1. One-to-many (FK on products) vs many-to-many (junction table)

**Decision**: One-to-many — `products.list_id` FK pointing to `lists.id`.

**Rationale**: A product belongs to one category ("Groceries" or "Electronics", not both). Many-to-many adds a join table, complicates queries, and introduces deletion semantics (remove from list vs delete product) that are unnecessary here. Can be revisited if multi-list membership is needed.

---

### 2. Standard list as a protected row (id = 1)

**Decision**: Insert Standard list with a fixed `id = 1` via `INSERT OR IGNORE INTO lists (id, name) VALUES (1, 'Standard')` inside `init_db()`.

**Rationale**: A well-known ID makes the FK default (`list_id INTEGER DEFAULT 1`) straightforward and lets the migration back-fill existing rows with a single `UPDATE`. Protecting deletion at the service layer (raise `ValueError` if `list_id == 1`) is simpler than a DB constraint.

**Alternative considered**: A separate boolean column `is_standard`. Rejected because it adds a column and doesn't simplify the protection logic.

---

### 3. Nullable vs NOT NULL FK during migration

**Decision**: Add the column as `INTEGER DEFAULT 1` (effectively NOT NULL after back-fill). Migration sequence:
1. `ALTER TABLE products ADD COLUMN list_id INTEGER DEFAULT 1`
2. `UPDATE products SET list_id = 1 WHERE list_id IS NULL`

**Rationale**: SQLite does not allow adding a NOT NULL column without a default to a populated table. Using `DEFAULT 1` plus an immediate back-fill achieves the same result without a table rebuild. The application model treats `list_id` as non-nullable (`int`) after migration.

---

### 4. Separate `WatchListRepository` Protocol vs extending `ProductRepository`

**Decision**: Add a new `WatchListRepository` Protocol in `ports.py`. The concrete `Database` class implements both structurally.

**Rationale**: `ProductRepository` is already stable and tested. Extending it with list methods changes its contract. A separate protocol respects the Interface Segregation Principle — components that only care about products (e.g. `PriceChecker`) don't need to know about lists.

---

### 5. Service method signatures: list_id (int) vs list_name (str)

**Decision**: Service layer uses `list_id: int`; the UI is responsible for resolving a name to an ID from the list of `WatchList` objects it fetches at render time.

**Rationale**: IDs are stable; names can change. Keeping the internal contract ID-based avoids look-ups inside the service layer and makes the API explicit.

---

## Risks / Trade-offs

- **Migration irreversibility** → The `ALTER TABLE` cannot be rolled back on SQLite. Mitigation: the column has a safe default; existing data is never deleted.
- **Standard list assumption** → Code assumes `id = 1` is Standard. If someone manually deletes that row the app will error. Mitigation: `init_db()` uses `INSERT OR IGNORE` so it's always re-created on startup.
- **UI cache staleness** → `AppService._products` caches products; list operations must invalidate it. Mitigation: call `_populate_or_update_products(update=True)` after any mutation.
- **PRAGMA foreign_keys** → SQLite disables FK enforcement by default. Mitigation: emit `PRAGMA foreign_keys = ON` at the start of every `_connect()` call.

---

## Migration Plan

Handled entirely inside `init_db()` — no manual steps required:

1. Create `lists` table (`CREATE TABLE IF NOT EXISTS lists …`).
2. Insert Standard list (`INSERT OR IGNORE INTO lists (id, name) VALUES (1, 'Standard')`).
3. Check if `list_id` column exists on `products` via `PRAGMA table_info(products)`.
4. If absent: `ALTER TABLE products ADD COLUMN list_id INTEGER DEFAULT 1`, then back-fill NULLs.

`init_db()` is idempotent — safe to run on an already-migrated database.

**Rollback**: Not supported (SQLite ALTER TABLE is permanent). The column carries a safe default, so partial migration leaves the app functional.

---

## Open Questions

None — all decisions resolved during exploration.
