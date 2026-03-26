## Why

The 🤖 icon indicating LLM-fallback scraping is currently embedded inside the product name button label, making it easy to miss and semantically awkward. Moving it to a dedicated column gives it a clearer visual identity and allows a descriptive tooltip.

## What Changes

- Remove the 🤖 icon from inside the `col_toggle` button label
- Add a new narrow column between `col_status` (price) and `col_del` (trash) to display the icon
- The icon column renders 🤖 with a `help` tooltip ("This product was scraped via LLM fallback") when `scraped_by_llm` is true, and is empty otherwise
- Column proportions updated from `[0.3, 3, 1.4, 0.5]` to `[0.3, 3, 1.4, 0.4, 0.5]`

## Capabilities

### New Capabilities

- none

### Modified Capabilities

- `tracker-ui`: The LLM indicator is now a standalone column element with a tooltip, not part of the product name button label

## Impact

- `source/porter/ui/app.py` — column layout and icon rendering logic only
