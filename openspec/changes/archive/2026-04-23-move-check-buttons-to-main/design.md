## Context

The Porter frontend (React/Vite) uses a two-panel layout: a fixed `Sidebar` on the left for navigation and an `AddProductForm` + product list in the main panel. The "Check All Prices" and "Check Selected" buttons currently live at the bottom of `Sidebar` as an "Actions" section. This makes them visually distant from the list they act on and requires that `Sidebar` holds action callbacks it has no natural ownership over.

## Goals / Non-Goals

**Goals:**
- Move the two check buttons into the main content area, between `AddProductForm` and the product list
- Decouple `Sidebar` from price-check concerns (remove 4 props)
- Preserve all existing button behaviour (disabled states, selection count label, warning on empty selection)

**Non-Goals:**
- Restyling or redesigning the buttons beyond placement
- Changing the check logic in hooks or backend

## Decisions

### 1. Render buttons directly in `ListPage`, not a new component

The check handlers (`handleCheckAll`, `handleCheckSelected`), loading states (`isChecking`), and selection count (`selectedIds.size`) already live in `ListPage`. Inlining a small `<div>` with two `<Button>` elements avoids introducing an unnecessary component and an extra props chain.

*Alternative considered*: Extract an `ActionBar` component. Rejected — it would be a two-prop wrapper around two buttons, adding indirection with no reuse.

### 2. Remove the four Sidebar props entirely

`onCheckAll`, `onCheckSelected`, `selectedCount`, and `isChecking` served only the Actions section. Once the section is removed, `Sidebar` has no use for them. Keeping them as unused props would be misleading; deleting them is cleaner.

*Alternative considered*: Keep props but ignore them inside Sidebar. Rejected — dead props create confusion.

### 3. Action bar placement

The bar is inserted as a bordered bottom section between the `AddProductForm` block and the `flex-1 overflow-y-auto` product list. Using `border-b border-border px-6 py-3` (matching the existing form section style) keeps visual consistency without new CSS.

## Risks / Trade-offs

- **Risk**: The sidebar "above the Actions section" wording in the `tracker-ui` spec becomes stale.  
  → Mitigation: Delta spec updates the requirement to remove that reference.
