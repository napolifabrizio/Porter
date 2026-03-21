## 1. UI — Checkboxes and Button

- [x] 1.1 Add a checkbox column to each product card in `app.py`, keyed by product ID
- [x] 1.2 Compute selection count from checkbox values before rendering the buttons row
- [x] 1.3 Add "Check Selected (N)" button alongside "Check All Prices"

## 2. Logic — Selective Check

- [x] 2.1 On "Check Selected" click: if count == 0, call `st.warning` and skip scraping
- [x] 2.2 On "Check Selected" click with selections: filter products list and call `check_all_prices` with filtered list
- [x] 2.3 Merge selective check results into `check_results` dict and reload products (same pattern as "Check All")
