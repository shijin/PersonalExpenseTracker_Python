import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

CATEGORIES = ["Rent", "Food", "Shopping", "Entertainment", "Utilities", "Others"]

CATEGORY_ICONS = {
    "Rent": "🏠",
    "Food": "🍔",
    "Shopping": "🛍️",
    "Entertainment": "🎬",
    "Utilities": "⚡",
    "Others": "📦"
}


def add_update_tab():
    st.markdown("""
    <div style='padding: 1rem 0 0.5rem;'>
        <div style='font-family: "DM Serif Display", serif; font-size: 1.5rem; color: #e8e4dc;'>
            Record Expenses
        </div>
        <div style='font-size: 0.78rem; color: #6b6b7a; letter-spacing: 0.06em; margin-top: 0.2rem;'>
            Select a date and log your expenses below
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Date Picker ───────────────────────────────────────────────────────────
    col_date, col_spacer = st.columns([1, 3])
    with col_date:
        selected_date = st.date_input(
            "Select Date",
            datetime.today(),
            label_visibility="collapsed"
        )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── Fetch existing expenses ───────────────────────────────────────────────
    try:
        response = requests.get(f"{API_URL}/expenses/{selected_date}", timeout=5)
        if response.status_code == 200:
            existing_expenses = response.json()
        else:
            st.error("Failed to retrieve expenses for this date.")
            existing_expenses = []
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Please ensure the FastAPI server is running.")
        return

    # ── Daily summary card ────────────────────────────────────────────────────
    if existing_expenses:
        daily_total = sum(e['amount'] for e in existing_expenses)
        num_entries = len(existing_expenses)
        top_category = max(
            set(e['category'] for e in existing_expenses),
            key=lambda c: sum(e['amount'] for e in existing_expenses if e['category'] == c)
        )
        icon = CATEGORY_ICONS.get(top_category, "📦")

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Daily Total", f"₹ {daily_total:,.2f}")
        with m2:
            st.metric("Entries", num_entries)
        with m3:
            st.metric("Top Category", f"{icon} {top_category}")

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Expense Form ──────────────────────────────────────────────────────────
    num_rows = max(5, len(existing_expenses))

    # Column headers
    st.markdown("""
    <div style='display:grid; grid-template-columns: 2fr 2fr 3fr;
                gap:1rem; padding: 0.6rem 0.5rem;
                border-bottom: 1px solid #2a2a35; margin-bottom: 0.5rem;'>
        <div style='font-size:0.72rem; color:#6b6b7a; letter-spacing:0.1em; text-transform:uppercase;'>Amount (₹)</div>
        <div style='font-size:0.72rem; color:#6b6b7a; letter-spacing:0.1em; text-transform:uppercase;'>Category</div>
        <div style='font-size:0.72rem; color:#6b6b7a; letter-spacing:0.1em; text-transform:uppercase;'>Notes</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form(key="expense_form"):
        expenses = []
        for i in range(num_rows):
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes = existing_expenses[i]['notes']
            else:
                amount = 0.0
                category = "Food"
                notes = ""

            if category not in CATEGORIES:
                category = "Others"

            col1, col2, col3 = st.columns([2, 2, 3])
            with col1:
                amount_input = st.number_input(
                    label="Amount", min_value=0.0, step=100.0,
                    value=float(amount),
                    key=f"amount_{selected_date}_{i}",
                    label_visibility="collapsed"
                )
            with col2:
                category_input = st.selectbox(
                    label="Category", options=CATEGORIES,
                    index=CATEGORIES.index(category),
                    key=f"category_{selected_date}_{i}",
                    label_visibility="collapsed"
                )
            with col3:
                notes_input = st.text_input(
                    label="Notes", value=notes,
                    placeholder="Add a note...",
                    key=f"notes_{selected_date}_{i}",
                    label_visibility="collapsed"
                )
            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        submit_button = st.form_submit_button("💾  Save Expenses")

        if submit_button:
            filtered_expenses = [e for e in expenses if e['amount'] > 0]
            if not filtered_expenses:
                st.warning("Please enter at least one expense with an amount greater than 0.")
            else:
                try:
                    response = requests.post(
                        f"{API_URL}/expenses/{selected_date}",
                        json=filtered_expenses,
                        timeout=5
                    )
                    if response.status_code == 200:
                        total_saved = sum(e['amount'] for e in filtered_expenses)
                        st.success(f"✓ {len(filtered_expenses)} expense(s) saved — ₹ {total_saved:,.2f} recorded for {selected_date.strftime('%d %b %Y')}")
                        st.rerun()
                    else:
                        st.error("Failed to update expenses. Please try again.")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to backend. Please ensure the FastAPI server is running.")