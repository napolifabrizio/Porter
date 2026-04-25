## 1. Remove buttons from Sidebar

- [x] 1.1 Delete the `/* Actions */` div (lines 114–134) from `App/src/components/Sidebar.tsx`
- [x] 1.2 Remove `onCheckAll`, `onCheckSelected`, `selectedCount`, and `isChecking` from the `SidebarProps` interface and function signature in `Sidebar.tsx`

## 2. Add action bar to main content area

- [x] 2.1 In `App/src/pages/ListPage.tsx`, insert an action bar `<div>` between the `AddProductForm` block and the product list block, containing both "Check All Prices" and "Check Selected (N)" buttons with correct disabled states
- [x] 2.2 Remove the four props (`onCheckAll`, `onCheckSelected`, `selectedCount`, `isChecking`) from the `<Sidebar>` usage in `ListPage.tsx`
