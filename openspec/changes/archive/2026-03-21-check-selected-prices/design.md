## Context

The UI currently has a single "Check All Prices" button that calls `check_all_prices(products)` with the full product list. `checker.py` already accepts any list of `Product` objects, so selective checking requires no backend changes — only UI state management in `app.py`.

## Goals / Non-Goals

**Goals:**
- Let users select a subset of products via checkboxes and check only those
- Warn when "Check Selected" is clicked with no products checked

**Non-Goals:**
- Persisting checkbox state across page reloads
- Per-product inline "check this one" buttons (different UX pattern, out of scope)
- Modifying `checker.py` or `database.py`

## Decisions

**Checkbox state via `st.session_state`**
Streamlit reruns the script on every widget interaction. Checkbox values are read directly from their widget keys each render cycle — no explicit session state management needed beyond Streamlit's built-in widget state.

**Button label shows selection count**
"Check Selected (2)" gives immediate feedback on how many are selected without requiring the user to count checkboxes. Implemented by summing checkbox values before rendering the button.

**Checkbox placement inside each product card**
Keeps selection visually tied to the product it controls. Placed in a narrow left column before the product info column.

**Reuse `check_all_prices` with filtered list**
No new function needed. `check_all_prices([p for p in products if selected[p.id]])` is sufficient.

## Risks / Trade-offs

- [Streamlit rerun on checkbox toggle] → Expected behavior; results are cleared between reruns unless stored in `st.session_state`. This is acceptable — results only show after an explicit button click.
- [All checkboxes unchecked by default] → User must actively select before using "Check Selected". This is intentional; the existing "Check All" covers the zero-selection case.
