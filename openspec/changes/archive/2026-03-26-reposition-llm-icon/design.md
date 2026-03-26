## Context

The product list row currently uses four Streamlit columns: `[0.3, 3, 1.4, 0.5]` (select, name/toggle, price/status, delete). The 🤖 LLM indicator is embedded in the toggle button label string. This is a purely cosmetic change confined to `ui/app.py`.

## Goals / Non-Goals

**Goals:**
- Give the 🤖 indicator its own visual slot between the price and the delete button
- Add a tooltip explaining what the icon means

**Non-Goals:**
- Changing when or how `scraped_by_llm` is determined
- Making the icon interactive (click, navigate, etc.)
- Any changes outside `ui/app.py`

## Decisions

**Add a fifth column for the icon**

Column proportions change from `[0.3, 3, 1.4, 0.5]` to `[0.3, 3, 1.4, 0.4, 0.5]`.
The icon column width (0.4) is intentionally narrow — it only needs to hold a single emoji.

Alternative considered: render the icon inline after the price in `col_status` via markdown. Rejected because mixing an informational badge with price text clutters the status column and makes alignment inconsistent when the icon is absent.

**Use `st.button` with `help=` for the tooltip**

Streamlit's `st.button` accepts a `help` kwarg that renders a native tooltip on hover. Wrapping the emoji in a disabled button is the idiomatic way to show a non-interactive element with a tooltip in Streamlit.

Alternative considered: plain `st.markdown` with an HTML `title` attribute. Rejected because Streamlit strips unsafe HTML attributes by default; using `unsafe_allow_html=True` for a tooltip is excessive.

**Empty column when not LLM-scraped**

When `scraped_by_llm` is false, the icon column renders nothing. The column still occupies its width, keeping all rows aligned (name, price, delete all stay in consistent positions).

## Risks / Trade-offs

- [Narrow column may clip on very small screens] → Acceptable for a personal desktop app; no mobile requirement exists.
- [Disabled button styling varies by Streamlit theme] → Icon is purely decorative; style consistency is low-priority.
