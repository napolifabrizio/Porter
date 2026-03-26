## 1. Update Column Layout

- [x] 1.1 Change column proportions in `app.py` from `[0.3, 3, 1.4, 0.5]` to `[0.3, 3, 1.4, 0.4, 0.5]` and name the new variable `col_llm`

## 2. Move LLM Icon

- [x] 2.1 Remove the `llm_icon` variable and its interpolation from the `col_toggle` button label, leaving only the arrow and product name
- [x] 2.2 In `col_llm`, render a disabled 🤖 button with `help="This product was scraped via LLM fallback"` when `scraped_by_llm` is true; render nothing otherwise
