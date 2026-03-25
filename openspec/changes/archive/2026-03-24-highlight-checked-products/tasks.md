## 1. Session State Migration

- [x] 1.1 Replace the local `check_results: dict[int, object] = {}` variable with `st.session_state.setdefault("check_results", {})` at the top of the product list section
- [x] 1.2 Update the `check_clicked` branch to assign results to `st.session_state["check_results"]` (full overwrite)
- [x] 1.3 Update the `check_sel_clicked` branch to assign results to `st.session_state["check_results"]` (full overwrite)
- [x] 1.4 Replace all remaining references to the local `check_results` variable with `st.session_state["check_results"]`

## 2. Colored Stripe Rendering

- [x] 2.1 Inside the `for product in products` loop, compute `result = st.session_state["check_results"].get(product.id)` and derive `stripe_color` (green `#00c853` for drop, blue `#2196F3` for stable, red `#f44336` for error, `None` if not checked)
- [x] 2.2 As the first element inside each `st.container(border=True)`, inject a `st.markdown` with a styled `<div>` that renders a 3px left border stripe when `stripe_color` is set, and nothing when it is `None`
