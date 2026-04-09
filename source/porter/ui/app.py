import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from porter.application.service import AppService

svc = AppService()

# ── Load lists ─────────────────────────────────────────────────────────────────

all_lists = svc.list_all_lists()
list_map = {wl.id: wl.name for wl in all_lists}

if "active_list_id" not in st.session_state:
    st.session_state["active_list_id"] = 1

active_list_id: int = st.session_state["active_list_id"]
active_list_name: str = list_map.get(active_list_id, "Standard")

st.title("Porter — Price Tracker")

# ── Sidebar ────────────────────────────────────────────────────────────────────

with st.sidebar:
    # ── Your Lists ────────────────────────────────────────────────────────────
    st.subheader("Your Lists")

    for wl in all_lists:
        col_btn, col_del = st.columns([4, 1])
        with col_btn:
            is_active = wl.id == active_list_id
            label = f"**{wl.name}**" if is_active else wl.name
            if st.button(label, key=f"list_btn_{wl.id}", use_container_width=True):
                st.session_state["active_list_id"] = wl.id
                st.rerun()
        with col_del:
            if wl.id != 1:
                if st.button("🗑", key=f"del_list_{wl.id}", help=f"Delete '{wl.name}'"):
                    st.session_state[f"confirm_del_list_{wl.id}"] = True

        if st.session_state.get(f"confirm_del_list_{wl.id}", False):
            st.warning(
                f"Delete **{wl.name}**? Its products will move to Standard.",
                icon="⚠️",
            )
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Confirm", key=f"confirm_yes_{wl.id}", type="primary"):
                    svc.delete_list(wl.id)
                    if st.session_state["active_list_id"] == wl.id:
                        st.session_state["active_list_id"] = 1
                    del st.session_state[f"confirm_del_list_{wl.id}"]
                    st.rerun()
            with c2:
                if st.button("Cancel", key=f"confirm_no_{wl.id}"):
                    del st.session_state[f"confirm_del_list_{wl.id}"]
                    st.rerun()

    st.divider()

    # ── New List ──────────────────────────────────────────────────────────────
    with st.expander("New List"):
        new_list_name = st.text_input("List name", key="new_list_name_input")
        if st.button("Create", key="create_list_btn"):
            name = new_list_name.strip()
            if not name:
                st.warning("List name cannot be empty.")
            else:
                try:
                    svc.create_list(name)
                    st.rerun()
                except ValueError as e:
                    st.warning(str(e))

    st.divider()

    # ── Actions ───────────────────────────────────────────────────────────────
    st.subheader("Actions")

    products_for_sel = svc.list_products()
    selected_ids = {
        p.id
        for p in products_for_sel
        if st.session_state.get(f"sel_{p.id}", False)
    }
    n_selected = len(selected_ids)

    check_clicked = st.button("Check All Prices", type="primary", use_container_width=True)
    check_sel_clicked = st.button(
        f"Check Selected ({n_selected})", use_container_width=True
    )

# ── Add product ────────────────────────────────────────────────────────────────

st.subheader("Track a new product")

url_input = st.text_input("Product URL", placeholder="https://...")
list_options = {wl.name: wl.id for wl in all_lists}
default_index = next(
    (i for i, wl in enumerate(all_lists) if wl.id == active_list_id), 0
)
selected_list_name = st.selectbox(
    "Add to list",
    options=list(list_options.keys()),
    index=default_index,
    key="track_list_selector",
)
selected_list_id = list_options[selected_list_name]

if st.button("Add Product"):
    url = url_input.strip()
    if not url:
        st.warning("Please enter a URL.")
    else:
        with st.spinner("Fetching product data..."):
            try:
                track_result = svc.track(url, list_id=selected_list_id)
                product = track_result.product
                if "llm_scraped" not in st.session_state:
                    st.session_state["llm_scraped"] = {}
                st.session_state["llm_scraped"][product.id] = track_result.scraped_by_llm
                st.success(f"Added: **{product.name}** — R$ {product.current_price:.2f}")
            except ValueError as e:
                st.warning(str(e))
            except Exception as e:
                st.error(f"Failed to add product: {e}")

st.divider()

# ── Product list ───────────────────────────────────────────────────────────────

products = svc.list_products(list_id=active_list_id)

if check_clicked:
    with st.spinner("Checking prices..."):
        results = svc.check_all_prices(list_id=active_list_id)
        st.session_state["check_results"] = {r.product.id: r for r in results}
        if "llm_scraped" not in st.session_state:
            st.session_state["llm_scraped"] = {}
        for r in results:
            st.session_state["llm_scraped"][r.product.id] = r.scraped_by_llm
    products = svc.list_products(list_id=active_list_id)
elif check_sel_clicked:
    if n_selected == 0:
        st.warning("Select at least one product.")
    else:
        with st.spinner("Checking selected prices..."):
            results = svc.check_selected(list(selected_ids))
            st.session_state["check_results"] = {r.product.id: r for r in results}
            if "llm_scraped" not in st.session_state:
                st.session_state["llm_scraped"] = {}
            for r in results:
                st.session_state["llm_scraped"][r.product.id] = r.scraped_by_llm
        products = svc.list_products(list_id=active_list_id)

st.subheader(f"{active_list_name}")

if not products:
    st.info(f"No products in {active_list_name}. Paste a URL above to get started.")
else:
    for product in products:
        exp_key = f"expanded_{product.id}"
        if exp_key not in st.session_state:
            st.session_state[exp_key] = False

        check_results = st.session_state.get("check_results", {})
        result = check_results.get(product.id)
        if result is None:
            stripe_color = None
        elif result.error:
            stripe_color = "#f44336"
        elif result.dropped:
            stripe_color = "#00c853"
        elif result.change_pct < 0:
            stripe_color = "#f44336"
        else:
            stripe_color = "#2196F3"

        with st.container(border=True):
            if stripe_color:
                st.markdown(
                    f"<div style='height: 4px; background-color: {stripe_color}; "
                    f"margin: -0.5rem -1rem 0.75rem -1rem; border-radius: 2px 2px 0 0'></div>",
                    unsafe_allow_html=True,
                )

            col_sel, col_toggle, col_status, col_llm, col_del = st.columns([0.3, 3, 1.4, 0.4, 0.5])

            with col_sel:
                st.checkbox("", key=f"sel_{product.id}", label_visibility="collapsed")

            with col_toggle:
                arrow = "▼" if st.session_state[exp_key] else "▶"
                if st.button(f"{arrow}  {product.name}", key=f"toggle_{product.id}", use_container_width=True):
                    st.session_state[exp_key] = not st.session_state[exp_key]
                    st.rerun()

            with col_status:
                if result and result.error:
                    st.markdown(f":red[⚠ {result.error[:80]}]")
                elif result and result.dropped:
                    pct = result.change_pct * 100
                    st.markdown(
                        f"<span style='color:green; font-size:1.3em'>↓ -{pct:.1f}%</span><br>"
                        f"<b>R&#36; {product.current_price:.2f}</b>",
                        unsafe_allow_html=True,
                    )
                elif result and result.change_pct < 0:
                    pct = abs(result.change_pct) * 100
                    st.markdown(
                        f"<span style='color:red; font-size:1.3em'>↑ +{pct:.1f}%</span><br>"
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

            with col_llm:
                if st.session_state.get("llm_scraped", {}).get(product.id, False):
                    st.button("🤖", key=f"llm_{product.id}", help="This product was scraped via LLM fallback", disabled=True)

            with col_del:
                if st.button("🗑", key=f"del_{product.id}", help="Remove product"):
                    svc.remove_product(product.id)
                    st.rerun()

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

            # ── Move to list ───────────────────────────────────────────────────
            other_lists = [wl for wl in all_lists if wl.id != product.list_id]
            if other_lists:
                move_options = {wl.name: wl.id for wl in other_lists}
                chosen = st.selectbox(
                    "Move to",
                    options=["— move to —"] + list(move_options.keys()),
                    key=f"move_{product.id}",
                    label_visibility="collapsed",
                )
                if chosen != "— move to —":
                    svc.move_product(product.id, move_options[chosen])
                    st.rerun()


# ── API key warning ────────────────────────────────────────────────────────────

if not os.environ.get("OPENAI_API_KEY"):
    st.sidebar.warning(
        "OPENAI_API_KEY not set. The LLM fallback scraper won't work. "
        "Simple sites (with structured HTML) will still be scraped."
    )
