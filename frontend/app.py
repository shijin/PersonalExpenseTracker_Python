import streamlit as st
from add_update_ui import add_update_tab
from analytics_ui import analytics_tab
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #0f0f13;
    color: #e8e4dc;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #16161d !important;
    border-right: 1px solid #2a2a35;
}
[data-testid="stSidebar"] * {
    color: #e8e4dc !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid #2a2a35;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6b6b7a !important;
    padding: 0.8rem 2rem;
    border: none;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    color: #c9a96e !important;
    border-bottom: 2px solid #c9a96e !important;
    background: transparent !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #16161d;
    border: 1px solid #2a2a35;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
}
[data-testid="metric-container"] label {
    color: #6b6b7a !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #c9a96e !important;
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem !important;
}

/* ── Inputs ── */
input, textarea, select {
    background: #1e1e28 !important;
    border: 1px solid #2a2a35 !important;
    border-radius: 8px !important;
    color: #e8e4dc !important;
}
input:focus, textarea:focus {
    border-color: #c9a96e !important;
    box-shadow: 0 0 0 2px rgba(201, 169, 110, 0.15) !important;
}

/* ── Select boxes ── */
[data-baseweb="select"] > div {
    background: #1e1e28 !important;
    border: 1px solid #2a2a35 !important;
    border-radius: 8px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #c9a96e, #a8834a) !important;
    color: #0f0f13 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.6rem 1.8rem !important;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #d4b87a, #c9a96e) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(201, 169, 110, 0.3) !important;
}

/* ── Form submit button ── */
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #c9a96e, #a8834a) !important;
    color: #0f0f13 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    width: 100%;
    padding: 0.7rem !important;
}

/* ── Tables ── */
[data-testid="stTable"] table {
    background: #16161d;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #2a2a35;
}
[data-testid="stTable"] th {
    background: #1e1e28 !important;
    color: #c9a96e !important;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border-bottom: 1px solid #2a2a35 !important;
    padding: 1rem !important;
}
[data-testid="stTable"] td {
    color: #e8e4dc !important;
    border-bottom: 1px solid #1e1e28 !important;
    padding: 0.85rem 1rem !important;
}
[data-testid="stTable"] tr:hover td {
    background: #1e1e28 !important;
}

/* ── Alerts ── */
.stSuccess {
    background: rgba(74, 180, 120, 0.1) !important;
    border: 1px solid rgba(74, 180, 120, 0.3) !important;
    border-radius: 8px !important;
    color: #4ab478 !important;
}
.stError {
    background: rgba(220, 80, 80, 0.1) !important;
    border: 1px solid rgba(220, 80, 80, 0.3) !important;
    border-radius: 8px !important;
}
.stWarning {
    background: rgba(201, 169, 110, 0.1) !important;
    border: 1px solid rgba(201, 169, 110, 0.3) !important;
    border-radius: 8px !important;
}

/* ── Date input ── */
[data-testid="stDateInput"] input {
    background: #1e1e28 !important;
    border: 1px solid #2a2a35 !important;
    color: #e8e4dc !important;
}

/* ── Number input ── */
[data-testid="stNumberInput"] input {
    background: #1e1e28 !important;
    border: 1px solid #2a2a35 !important;
    color: #e8e4dc !important;
}

/* ── Divider ── */
hr {
    border-color: #2a2a35 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f0f13; }
::-webkit-scrollbar-thumb { background: #2a2a35; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #c9a96e; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1.5rem 0 1rem;'>
        <div style='font-size: 2.5rem;'>💳</div>
        <div style='font-family: "DM Serif Display", serif; font-size: 1.4rem; color: #c9a96e; margin-top: 0.5rem;'>
            Expense<br>Tracker
        </div>
        <div style='font-size: 0.72rem; color: #6b6b7a; letter-spacing: 0.12em; text-transform: uppercase; margin-top: 0.4rem;'>
            Personal Finance
        </div>
    </div>
    <hr style='border-color: #2a2a35; margin: 0.5rem 0 1.5rem;'/>
    """, unsafe_allow_html=True)

    # Backend health check
    try:
        health = requests.get(f"{API_URL}/health", timeout=2)
        if health.status_code == 200:
            st.markdown("""
            <div style='display:flex; align-items:center; gap:0.5rem; padding: 0.6rem 1rem;
                        background: rgba(74,180,120,0.08); border: 1px solid rgba(74,180,120,0.2);
                        border-radius: 8px; margin-bottom: 1rem;'>
                <div style='width:8px; height:8px; border-radius:50%; background:#4ab478;
                            box-shadow: 0 0 6px #4ab478;'></div>
                <span style='font-size:0.78rem; color:#4ab478; letter-spacing:0.05em;'>API Connected</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            raise Exception()
    except Exception:
        st.markdown("""
        <div style='display:flex; align-items:center; gap:0.5rem; padding: 0.6rem 1rem;
                    background: rgba(220,80,80,0.08); border: 1px solid rgba(220,80,80,0.2);
                    border-radius: 8px; margin-bottom: 1rem;'>
            <div style='width:8px; height:8px; border-radius:50%; background:#dc5050;'></div>
            <span style='font-size:0.78rem; color:#dc5050; letter-spacing:0.05em;'>API Offline</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='padding: 0 0.5rem;'>
        <div style='font-size:0.72rem; color:#6b6b7a; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:1rem;'>
            Categories
        </div>
    </div>
    """, unsafe_allow_html=True)

    categories_info = {
        "🏠 Rent": "#c9a96e",
        "🍔 Food": "#7eb8c9",
        "🛍️ Shopping": "#c97eb8",
        "🎬 Entertainment": "#7ec98a",
        "⚡ Utilities": "#c9c47e",
        "📦 Others": "#9e9e9e"
    }
    for cat, color in categories_info.items():
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:0.6rem; padding:0.3rem 0.5rem;
                    margin-bottom:0.3rem;'>
            <div style='width:6px; height:6px; border-radius:50%; background:{color};'></div>
            <span style='font-size:0.82rem; color:#a0a0b0;'>{cat}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='position:absolute; bottom:2rem; left:0; right:0; text-align:center;'>
        <div style='font-size:0.7rem; color:#3a3a45; letter-spacing:0.05em;'>
            Built with FastAPI + Streamlit
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Main Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding: 2rem 0 1.5rem;'>
    <div style='font-family: "DM Serif Display", serif; font-size: 2.6rem;
                color: #e8e4dc; line-height: 1.1;'>
        Personal Finance
        <span style='color: #c9a96e; font-style: italic;'> Dashboard</span>
    </div>
    <div style='font-size: 0.82rem; color: #6b6b7a; letter-spacing: 0.08em;
                text-transform: uppercase; margin-top: 0.5rem;'>
        Track · Analyse · Optimise
    </div>
</div>
<hr style='border-color: #2a2a35; margin-bottom: 1.5rem;'/>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["  ✦  Add / Update  ", "  ✦  Analytics  "])

with tab1:
    add_update_tab()

with tab2:
    analytics_tab()