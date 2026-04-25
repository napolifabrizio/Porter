## Context

Product names are scraped once and stored in the `products` table as a plain text column. There is currently no mechanism to update a product's name after insertion. The `ProductRepository` protocol has `update_price` but no `update_name`. The UI (`ProductCard`) renders the name as a static label inside a collapse-toggle button.

## Goals / Non-Goals

**Goals:**
- Single-click inline rename from the product card header (no modal).
- Persist via a new `PATCH /products/{id}` API endpoint.
- Name change is reflected immediately in the UI after save (optimistic update or refetch).

**Non-Goals:**
- Bulk rename.
- Rename history / audit log.
- Re-scraping the name automatically in the background.

## Decisions

**Inline edit over a modal**
A click-to-edit `<input>` inside the card header is less disruptive than a dialog. The user clicks the name, edits it, and presses Enter or blurs to save. Escape cancels. This is the standard pattern used by list names elsewhere in the UI.

**`PATCH /products/{id}` with `{ name }` body**
A dedicated partial-update route is the cleanest REST shape. Putting it on the existing `/products` collection would require a PUT with the full product body, which is verbose and fragile. A PATCH with a single field matches what the UI sends.

**Protocol extension on `ProductRepository`**
`update_name(product_id, name)` is added to the port. The SQLite implementation gets the matching method. This keeps the dependency rule intact (application never imports infrastructure).

**React Query mutation with cache invalidation**
A `useRenameProduct` hook wraps the PATCH call and invalidates the products query on success, causing the card to rerender with the new name without a full page reload.

## Risks / Trade-offs

- [Empty name submitted] → Validate on the frontend (trim + non-empty check before firing the request); also validate on the backend (400 if blank). 
- [Optimistic update flicker] → Using cache invalidation (refetch) rather than optimistic write keeps the UI simple; the round-trip latency is negligible on localhost.

## Migration Plan

No schema migration needed — the `name` column already exists in the `products` table. Deploy is a straight code push.
