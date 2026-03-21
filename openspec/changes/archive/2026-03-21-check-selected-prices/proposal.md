## Why

"Check All Prices" re-scrapes every tracked product on every click, which is slow and wasteful when the user only cares about a subset. A selective check lets users target specific products without waiting for the full list.

## What Changes

- Add a checkbox to each product card in the UI
- Add a "Check Selected" button alongside "Check All Prices" that runs only on checked products
- Show a warning if "Check Selected" is clicked with no products selected

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `tracker-ui`: Adding a new requirement — user can select individual products and trigger a price check only for those products.

## Impact

- `source/porter/app.py` — only file that changes; checkbox state management and new button logic
- `openspec/specs/tracker-ui/spec.md` — new requirement and scenarios added
- `checker.py` and `database.py` — no changes needed
