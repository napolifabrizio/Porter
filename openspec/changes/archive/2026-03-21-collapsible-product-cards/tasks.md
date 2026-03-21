## 1. Collapsible Card Rendering

- [x] 1.1 Add `expanded_{product.id}` boolean to `st.session_state` (default `False`) for each product before rendering
- [x] 1.2 Replace the current three-column product container with an always-visible header row: checkbox | toggle button (▶/▼ + name) | price/status
- [x] 1.3 Wire the toggle button to flip `st.session_state[f"expanded_{product.id}"]` on click
- [x] 1.4 Render the expanded section (description, URL, initial price) conditionally below the header row when the state is `True`
