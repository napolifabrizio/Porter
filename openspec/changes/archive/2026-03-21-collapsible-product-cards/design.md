## Context

The product list in `app.py` renders each product in a `st.container(border=True)` with three columns: checkbox, info (name + description + URL), and price/status. All fields are always visible. With many tracked products this creates a dense, hard-to-scan list.

## Goals / Non-Goals

**Goals:**
- Cards collapsed by default — only name and price visible
- Click to expand and reveal description, URL, and initial price
- Checkbox always visible regardless of expand state (needed for "Check Selected")
- Expand/collapse state persists within the Streamlit session

**Non-Goals:**
- Persisting expand state across sessions
- Animations or transitions
- Changes to scraper, database, checker, or models

## Decisions

### Use `st.session_state` toggle, not `st.expander`

`st.expander` was considered but its header is a static string — it cannot hold a styled price column alongside the product name. A `session_state` boolean per product gives full layout control.

**Chosen approach**: `st.session_state[f"expanded_{product.id}"]` (default `False`). A button in the always-visible row toggles it. Because Streamlit rerenders on each interaction, the conditional block below the header row simply reads that boolean.

### Always-visible row layout

```
[ ☐ ] [ ▶/▼ Name ]              [ R$ price ]
```

- Column 1 (narrow): checkbox (existing `sel_{product.id}` key, unchanged)
- Column 2 (wide): expand toggle button styled as text (`▶ Name` / `▼ Name`)
- Column 3 (narrow): price / status (existing logic, unchanged)

The toggle is a `st.button` with `use_container_width=True` and `type="tertiary"` to avoid heavy button styling.

### Expanded section

Rendered conditionally below the always-visible row (no extra columns):

```
─────────────────────────────────────────
Description text (if present)
🔗 URL
initial: R$ X.XX
```

Uses `st.caption` for secondary info, consistent with current style.

## Risks / Trade-offs

- [Button rerenders page] → Streamlit rerenders on every button click; state is preserved in `session_state`, so this is acceptable and expected behavior.
- [Many open cards] → No limit enforced; user controls expand state manually.
