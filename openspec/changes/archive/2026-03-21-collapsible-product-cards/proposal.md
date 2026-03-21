## Why

When tracking many products, the list becomes dense and hard to scan — description and URL are always visible even when the user only needs a quick price glance. Collapsible cards reduce visual noise by default while keeping full details one click away.

## What Changes

- Each product in the list is rendered as a collapsible card
- **Collapsed (default)**: shows checkbox, product name, and current price only
- **Expanded (on click)**: reveals description, URL, and initial price
- Expand/collapse state is tracked per product in `st.session_state`
- The selection checkbox remains visible in both states

## Capabilities

### New Capabilities

(none — this is a UI behavior change within an existing capability)

### Modified Capabilities

- `tracker-ui`: Product list items gain collapsible expand/collapse behavior; the always-visible row changes from showing all fields to showing only name and price when collapsed.

## Impact

- `source/porter/app.py` — product list rendering loop
- No changes to scraper, database, checker, or models
- No new dependencies
