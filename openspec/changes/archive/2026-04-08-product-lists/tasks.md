## 1. Models

- [x] 1.1 Add `WatchList` Pydantic model to `models.py` (fields: `id: int`, `name: str`)
- [x] 1.2 Add `list_id: int` field to the `Product` Pydantic model in `models.py`

## 2. Ports

- [x] 2.1 Add `WatchListRepository` Protocol to `application/ports.py` with methods: `create_list`, `list_all_lists`, `delete_list`, `move_product_to_list`
- [x] 2.2 Update `ProductRepository` Protocol in `application/ports.py`: add optional `list_id` param to `add_product` and `list_products`

## 3. Database — Schema & Migration

- [x] 3.1 Enable `PRAGMA foreign_keys = ON` inside `Database._connect()`
- [x] 3.2 Add `CREATE TABLE IF NOT EXISTS lists (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE)` to `init_db()`
- [x] 3.3 Insert Standard list via `INSERT OR IGNORE INTO lists (id, name) VALUES (1, 'Standard')` inside `init_db()`
- [x] 3.4 Add migration in `init_db()`: check `PRAGMA table_info(products)` for `list_id`; if absent run `ALTER TABLE products ADD COLUMN list_id INTEGER DEFAULT 1` then back-fill NULLs

## 4. Database — New Methods

- [x] 4.1 Implement `create_list(name: str) -> WatchList` on `Database`
- [x] 4.2 Implement `list_all_lists() -> list[WatchList]` on `Database`
- [x] 4.3 Implement `delete_list(list_id: int) -> None` on `Database` (move products to Standard, then delete row)
- [x] 4.4 Implement `move_product_to_list(product_id: int, list_id: int) -> None` on `Database`
- [x] 4.5 Update `add_product()` to accept and persist `list_id: int | None = None` (default 1)
- [x] 4.6 Update `list_products()` to accept and apply optional `list_id: int | None = None` filter

## 5. AppService

- [x] 5.1 Add `create_list(name: str) -> WatchList` to `AppService`
- [x] 5.2 Add `list_all_lists() -> list[WatchList]` to `AppService`
- [x] 5.3 Add `delete_list(list_id: int) -> None` to `AppService` (guard: raise `ValueError` if `list_id == 1`)
- [x] 5.4 Add `move_product(product_id: int, target_list_id: int) -> None` to `AppService`
- [x] 5.5 Update `track(url, list_id: int | None = None)` to pass `list_id` to `db.add_product()`
- [x] 5.6 Update `list_products(list_id: int | None = None)` to pass filter to `db.list_products()`

## 6. UI — Sidebar List Navigation

- [x] 6.1 Load all lists from `svc.list_all_lists()` at the top of `app.py`; store names and IDs for use across the page
- [x] 6.2 Add "Your Lists" section in the sidebar above "Actions": render a button per list; clicking sets `st.session_state["active_list_id"]`
- [x] 6.3 Add a "New List" text input + button in the sidebar; on submit call `svc.create_list()` and `st.rerun()`
- [x] 6.4 Add a delete button next to each non-Standard list in the sidebar; on confirm call `svc.delete_list()`, reset `active_list_id` to 1 if needed, and `st.rerun()`

## 7. UI — Track Form & Product List

- [x] 7.1 Add a list selector (`st.selectbox`) to the "Track a new product" form; pass selected `list_id` to `svc.track()`
- [x] 7.2 Update `svc.list_products()` call to pass `st.session_state["active_list_id"]` so only the active list's products are shown
- [x] 7.3 Update empty-state message to reference the active list name
- [x] 7.4 Add a move-to-list selectbox on each product card (showing all lists except the product's current one); on selection call `svc.move_product()` and `st.rerun()`
