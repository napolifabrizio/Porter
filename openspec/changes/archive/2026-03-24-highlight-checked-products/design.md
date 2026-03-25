## Context

The UI currently uses `st.spinner` wrapping the check operation, which triggers Streamlit's full-page loading state. After the check completes, there is no per-product visual feedback showing which products were included in the run. `check_results` is a local variable that resets on every script rerun, meaning even the ephemeral post-check feedback disappears the moment the user interacts with anything (e.g., expands a card).

## Goals / Non-Goals

**Goals:**
- Render a colored left stripe inside the product card border for every product that participated in the last check
- Green = price dropped ≥ 5%, blue = stable price, red = check error
- Stripes persist across reruns (expand/collapse, checkbox toggle) until the next check run replaces them
- Only the most recent check's products are highlighted — no accumulation across runs

**Non-Goals:**
- Removing or replacing `st.spinner` (the full-page dark flash is a Streamlit constraint, not addressed here)
- Persisting check results across browser sessions or page reloads
- Showing per-product loading state during the check

## Decisions

### 1. Store `check_results` in `st.session_state`

**Decision**: Replace the local `check_results: dict` with `st.session_state["check_results"]`.

**Rationale**: Local variables reset on every Streamlit rerun. Any interaction after the check (expand card, toggle checkbox) triggers a rerun and wipes the results. Session state survives reruns within the same browser session.

**Alternative considered**: Re-query the database to infer "what changed" — rejected because it's indirect and loses error/drop metadata that isn't stored in the DB.

**Always overwrite, never merge**: Each check assigns a fresh dict to `st.session_state["check_results"]`. This ensures only the most recent check's products carry stripes.

### 2. Colored stripe via inline `st.markdown` inside `st.container`

**Decision**: As the first element inside each `st.container(border=True)`, inject a `st.markdown` with a styled `<div>` that renders a thin vertical stripe using a left border.

**Rationale**: Streamlit does not expose CSS class hooks on `st.container`. Injecting an absolutely-positioned element is unreliable across Streamlit versions. A thin markdown div rendered as the first child of the container is the most stable and readable approach — it flows naturally and doesn't interfere with the column layout below it.

**Alternative considered**: CSS injection via `st.markdown("<style>...</style>")` targeting nth-child selectors — rejected because Streamlit's generated DOM structure is not stable across versions.

### 3. Color scheme

| State | Color | Hex |
|-------|-------|-----|
| Price dropped | Green | `#00c853` |
| Price stable | Blue | `#2196F3` |
| Check error | Red | `#f44336` |
| Not checked | — | no stripe |

## Risks / Trade-offs

- **Streamlit DOM instability** → The inline markdown div approach is tied to how Streamlit renders `st.container` children. Major Streamlit version upgrades could affect visual appearance, but won't break functionality.
- **Session state grows stale** → If a product is deleted while its id is still in `session_state["check_results"]`, the lookup `check_results.get(product.id)` returns `None` safely — no crash, just no stripe.

## Open Questions

- None. All decisions are resolved.
