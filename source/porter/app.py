import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from porter.checker import check_all_prices
from porter.database import add_product, init_db, list_products
from porter.scraper import fetch_and_scrape

init_db()

st.title("Porter — Price Tracker")

# ── Add product ────────────────────────────────────────────────────────────────

st.subheader("Track a new product")

url_input = st.text_input("Product URL", placeholder="https://...")

if st.button("Add Product"):
    url = url_input.strip()
    if not url:
        st.warning("Please enter a URL.")
    else:
        with st.spinner("Fetching product data..."):
            try:
                scraped = fetch_and_scrape(url)
                add_product(scraped, url)
                st.success(f"Added: **{scraped.name}** — R$ {scraped.price:.2f}")
            except ValueError as e:
                st.warning(str(e))
            except Exception as e:
                st.error(f"Failed to add product: {e}")

st.divider()

# ── Product list ───────────────────────────────────────────────────────────────

products = list_products()

if not products:
    st.info("No products tracked yet. Paste a URL above to get started.")
else:
    # Compute selection count from checkbox widget state (before rendering buttons)
    selected_ids = {
        p.id
        for p in products
        if st.session_state.get(f"sel_{p.id}", False)
    }
    n_selected = len(selected_ids)

    col_check, col_check_sel, _ = st.columns([1, 1, 3])
    with col_check:
        check_clicked = st.button("Check All Prices", type="primary")
    with col_check_sel:
        check_sel_clicked = st.button(f"Check Selected ({n_selected})")

    check_results: dict[int, object] = {}

    if check_clicked:
        with st.spinner("Checking prices..."):
            results = check_all_prices(products)
            check_results = {r.product.id: r for r in results}
        # Reload products to show updated prices
        products = list_products()
    elif check_sel_clicked:
        if n_selected == 0:
            st.warning("Select at least one product.")
        else:
            selected_products = [p for p in products if p.id in selected_ids]
            with st.spinner("Checking selected prices..."):
                results = check_all_prices(selected_products)
                check_results = {r.product.id: r for r in results}
            products = list_products()

    st.subheader("Your products")

    for product in products:
        exp_key = f"expanded_{product.id}"
        if exp_key not in st.session_state:
            st.session_state[exp_key] = False

        with st.container(border=True):
            col_sel, col_toggle, col_status = st.columns([0.3, 3, 1.4])

            with col_sel:
                st.checkbox("", key=f"sel_{product.id}", label_visibility="collapsed")

            with col_toggle:
                arrow = "▼" if st.session_state[exp_key] else "▶"
                if st.button(f"{arrow}  {product.name}", key=f"toggle_{product.id}", use_container_width=True):
                    st.session_state[exp_key] = not st.session_state[exp_key]
                    st.rerun()

            with col_status:
                result = check_results.get(product.id)

                if result and result.error:
                    st.markdown(f":red[⚠ {result.error[:80]}]")
                elif result and result.dropped:
                    pct = result.change_pct * 100
                    st.markdown(
                        f"<span style='color:green; font-size:1.3em'>↓ -{pct:.1f}%</span><br>"
                        f"<b>R&#36; {product.current_price:.2f}</b>",
                        unsafe_allow_html=True,
                    )
                elif result:
                    st.markdown(
                        f"<span style='color:gray; font-size:1.3em'>=</span><br>"
                        f"<b>R&#36; {product.current_price:.2f}</b>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<b>R&#36; {product.current_price:.2f}</b>",
                        unsafe_allow_html=True,
                    )

            if st.session_state[exp_key]:
                st.divider()
                lines = []
                if product.description:
                    lines.append(product.description[:160])
                lines.append(f"🔗 {product.url}")
                lines.append(f"Initial: R$ {product.initial_price:.2f}")
                st.markdown(
                    "<br>".join(f"<span style='color:#cccccc; font-size:0.85em'>{l}</span>" for l in lines),
                    unsafe_allow_html=True,
                )


# ── API key warning ────────────────────────────────────────────────────────────

if not os.environ.get("OPENAI_API_KEY"):
    st.sidebar.warning(
        "OPENAI_API_KEY not set. The LLM fallback scraper won't work. "
        "Simple sites (with structured HTML) will still be scraped."
    )
