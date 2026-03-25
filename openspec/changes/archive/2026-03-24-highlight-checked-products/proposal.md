## Why

When a user selects one product and clicks "Check Selected", the entire page darkens due to Streamlit's full-page loading state — making it impossible to visually distinguish which products were actually checked. After the check completes, there is no per-product feedback indicating which products ran and what their result was.

## What Changes

- After a check (all or selected), each product card that was part of the check displays a colored left stripe inside its border:
  - **Green stripe** — price dropped ≥ 5%
  - **Blue stripe** — price checked, no significant drop
  - **Red stripe** — check failed with an error
- Products not included in the last check show no stripe
- `check_results` is persisted in `st.session_state` so stripes survive reruns (expand/collapse, checkbox toggle) until the next check overwrites them
- Each new check **replaces** `session_state.check_results` entirely — only the most recent check's products are highlighted

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `tracker-ui`: Product cards gain a per-result visual stripe; check result state is now persisted in session state across reruns

## Impact

- `source/porter/ui/app.py` — move `check_results` to `st.session_state`, inject colored stripe markup inside each product container
