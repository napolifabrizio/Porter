## 1. Backend — Port & Infrastructure

- [x] 1.1 Add `update_name(product_id: int, name: str) -> None` to `ProductRepository` protocol in `source/porter/application/ports.py`
- [x] 1.2 Implement `update_name` in `source/porter/infrastructure/database.py` (UPDATE products SET name=? WHERE id=?)

## 2. Backend — API

- [x] 2.1 Add `RenameProductRequest` Pydantic model (field: `name: str`) to `source/porter/models.py`
- [x] 2.2 Add `PATCH /products/{id}` route to `source/porter/app.py` — validate non-blank name, call `db.update_name`, return updated product or 404

## 3. Frontend — API hook

- [x] 3.1 Add `renameProduct(id, name)` API call in `App/src/api.ts` (or equivalent API layer file)
- [x] 3.2 Create `useRenameProduct` React Query mutation hook in `App/src/hooks/` that calls the API and invalidates the products query on success

## 4. Frontend — ProductCard inline edit

- [x] 4.1 Add editing state (`isEditing`, `draftName`) to `ProductCard` component
- [x] 4.2 Replace the static name label with a toggle: click on name → show `<input>` pre-filled with current name
- [x] 4.3 On Enter or blur: if `draftName.trim()` is non-empty, fire `useRenameProduct` mutation; otherwise restore original name
- [x] 4.4 On Escape: cancel edit and restore original name without API call
