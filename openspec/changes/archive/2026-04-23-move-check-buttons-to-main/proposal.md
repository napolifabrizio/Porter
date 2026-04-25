## Why

The "Check All Prices" and "Check Selected" buttons are currently anchored at the bottom of the sidebar, visually disconnected from the product list they act on. Moving them to the main content area — directly above the product list — makes the action-target relationship obvious and keeps the sidebar focused on navigation.

## What Changes

- Remove the Actions section (Check All / Check Selected buttons) from the Sidebar component
- Remove the related props (`onCheckAll`, `onCheckSelected`, `selectedCount`, `isChecking`) from the `SidebarProps` interface
- Add an action bar in the main content area of `ListPage`, positioned between `AddProductForm` and the product list

## Capabilities

### New Capabilities

_None — this is a layout relocation, no new behaviour is introduced._

### Modified Capabilities

- `tracker-ui`: The placement of price-check actions changes from the sidebar footer to the main content area above the product list.

## Impact

- `App/src/components/Sidebar.tsx` — props interface shrinks, Actions `<div>` removed
- `App/src/pages/ListPage.tsx` — new action bar `<div>` inserted between `AddProductForm` and the product list; `<Sidebar>` usage loses 4 props
