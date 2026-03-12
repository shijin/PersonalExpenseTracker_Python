import streamlit as st
from datetime import datetime, date, timedelta
import requests
import pandas as pd

API_URL = "http://localhost:8000"

CATEGORY_COLORS = {
    "Rent":          "#c9a96e",
    "Food":          "#7eb8c9",
    "Shopping":      "#c97eb8",
    "Entertainment": "#7ec98a",
    "Utilities":     "#c9c47e",
    "Others":        "#9e9e9e"
}


def get_quick_range(label: str):
    today = date.today()
    if label == "This Week":
        start = today - timedelta(days=today.weekday())
        return start, today
    elif label == "This Month":
        return today.replace(day=1), today
    elif label == "Last Month":
        first_this = today.replace(day=1)
        last_prev = first_this - timedelta(days=1)
        return last_prev.replace(day=1), last_prev
    elif label == "Last 3 Months":
        return (today - timedelta(days=90)), today
    return today.replace(day=1), today


def analytics_tab():
    st.markdown("""
    <div style='padding: 1rem 0 0.5rem;'>
        <div style='font-family: "DM Serif Display", serif; font-size: 1.5rem; color: #e8e4dc;'>
            Spending Analytics
        </div>
        <div style='font-size: 0.78rem; color: #6b6b7a; letter-spacing: 0.06em; margin-top: 0.2rem;'>
            Analyse your spending patterns across any date range
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick filter buttons ──────────────────────────────────────────────────
    st.markdown("""
    <div style='font-size:0.72rem; color:#6b6b7a; letter-spacing:0.1em;
                text-transform:uppercase; margin-bottom:0.5rem;'>
        Quick Select
    </div>
    """, unsafe_allow_html=True)

    qcols = st.columns(4)
    quick_labels = ["This Week", "This Month", "Last Month", "Last 3 Months"]
    selected_quick = None
    for i, label in enumerate(quick_labels):
        with qcols[i]:
            if st.button(label, key=f"quick_{label}", use_container_width=True):
                selected_quick = label

    if selected_quick:
        st.session_state['qs_start'], st.session_state['qs_end'] = get_quick_range(selected_quick)

    default_start = st.session_state.get('qs_start', date.today().replace(day=1))
    default_end = st.session_state.get('qs_end', date.today())

    # ── Date range inputs ─────────────────────────────────────────────────────
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        start_date = st.date_input("From", default_start, key="analytics_start")
    with col2:
        end_date = st.date_input("To", default_end, key="analytics_end")
    with col3:
        st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)
        run = st.button("Analyse →", use_container_width=True)

    if start_date > end_date:
        st.error("Start date cannot be after end date.")
        return

    if not run and 'analytics_data' not in st.session_state:
        st.markdown("""
        <div style='text-align:center; padding: 4rem 0; color: #3a3a45;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>📊</div>
            <div style='font-size: 0.85rem; letter-spacing: 0.08em; text-transform: uppercase;'>
                Select a date range and click Analyse
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Fetch analytics data ──────────────────────────────────────────────────
    if run:
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        try:
            resp = requests.post(f"{API_URL}/analytics/", json=payload, timeout=5)
            resp.raise_for_status()
            result = resp.json()

            total_resp = requests.post(f"{API_URL}/analytics/total", json=payload, timeout=5)
            grand_total = total_resp.json().get("total", 0) if total_resp.status_code == 200 else 0

            monthly_resp = requests.get(f"{API_URL}/analytics/monthly", timeout=5)
            monthly_data = monthly_resp.json() if monthly_resp.status_code == 200 else []

            st.session_state['analytics_data'] = result
            st.session_state['analytics_total'] = grand_total
            st.session_state['analytics_monthly'] = monthly_data
            st.session_state['analytics_range'] = (start_date, end_date)

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend. Please ensure the FastAPI server is running.")
            return
        except requests.exceptions.HTTPError as e:
            st.error(f"Server error: {e}")
            return

    result = st.session_state.get('analytics_data', {})
    grand_total = st.session_state.get('analytics_total', 0)
    monthly_data = st.session_state.get('analytics_monthly', [])
    date_range = st.session_state.get('analytics_range', (start_date, end_date))

    if not result:
        st.info("No expenses found for the selected date range.")
        return

    st.markdown("<hr style='border-color:#2a2a35; margin: 1.5rem 0;'>", unsafe_allow_html=True)

    # ── KPI Metrics ───────────────────────────────────────────────────────────
    top_cat = max(result, key=lambda c: result[c]['total'])
    top_icon = {"Rent": "🏠","Food": "🍔","Shopping": "🛍️","Entertainment": "🎬","Utilities": "⚡","Others": "📦"}.get(top_cat, "📦")
    days_in_range = (date_range[1] - date_range[0]).days + 1
    daily_avg = grand_total / days_in_range if days_in_range > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total Spend", f"₹ {grand_total:,.2f}")
    with k2:
        st.metric("Daily Average", f"₹ {daily_avg:,.2f}")
    with k3:
        st.metric("Top Category", f"{top_icon} {top_cat}")
    with k4:
        st.metric("Categories Tracked", len(result))

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── Charts Row ────────────────────────────────────────────────────────────
    chart_col, table_col = st.columns([3, 2])

    with chart_col:
        st.markdown("""
        <div style='font-size:0.72rem; color:#6b6b7a; letter-spacing:0.1em;
                    text-transform:uppercase; margin-bottom:0.8rem;'>
            Spend by Category
        </div>
        """, unsafe_allow_html=True)

        df = pd.DataFrame({
            "Category": list(result.keys()),
            "Total": [result[c]['total'] for c in result],
            "Percentage": [result[c]['percentage'] for c in result]
        }).sort_values("Percentage", ascending=False)

        st.bar_chart(
            data=df.set_index("Category")["Total"],
            use_container_width=True,
            height=280,
            color="#c9a96e"
        )

    with table_col:
        st.markdown("""
        <div style='font-size:0.72rem; color:#6b6b7a; letter-spacing:0.1em;
                    text-transform:uppercase; margin-bottom:0.8rem;'>
            Breakdown
        </div>
        """, unsafe_allow_html=True)

        display_df = df.copy()
        display_df["Total"] = display_df["Total"].map("₹ {:,.2f}".format)
        display_df["Percentage"] = display_df["Percentage"].map("{:.1f}%".format)
        display_df = display_df.reset_index(drop=True)
        st.table(display_df)

    # ── Monthly Trend Chart ───────────────────────────────────────────────────
    if monthly_data and len(monthly_data) > 1:
        st.markdown("<hr style='border-color:#2a2a35; margin: 1rem 0;'>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size:0.72rem; color:#6b6b7a; letter-spacing:0.1em;
                    text-transform:uppercase; margin-bottom:0.8rem;'>
            Month-over-Month Trend
        </div>
        """, unsafe_allow_html=True)

        monthly_df = pd.DataFrame(monthly_data)
        monthly_df.columns = ["Month", "Total"]
        monthly_df = monthly_df.set_index("Month")

        st.line_chart(
            data=monthly_df,
            use_container_width=True,
            height=220,
            color="#c9a96e"
        )

    # ── Progress Bars per Category ────────────────────────────────────────────
    st.markdown("<hr style='border-color:#2a2a35; margin: 1rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem; color:#6b6b7a; letter-spacing:0.1em;
                text-transform:uppercase; margin-bottom:1rem;'>
        Category Distribution
    </div>
    """, unsafe_allow_html=True)

    for _, row in df.iterrows():
        cat = row['Category']
        pct = row['Percentage']
        color = CATEGORY_COLORS.get(cat, "#9e9e9e")
        icon = {"Rent": "🏠","Food": "🍔","Shopping": "🛍️","Entertainment": "🎬","Utilities": "⚡","Others": "📦"}.get(cat, "📦")
        st.markdown(f"""
        <div style='margin-bottom: 0.9rem;'>
            <div style='display:flex; justify-content:space-between; margin-bottom:0.3rem;'>
                <span style='font-size:0.82rem; color:#e8e4dc;'>{icon} {cat}</span>
                <span style='font-size:0.82rem; color:{color}; font-weight:600;'>{pct:.1f}%</span>
            </div>
            <div style='background:#1e1e28; border-radius:4px; height:6px; overflow:hidden;'>
                <div style='width:{pct}%; height:100%; background:{color};
                            border-radius:4px; transition: width 0.8s ease;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)