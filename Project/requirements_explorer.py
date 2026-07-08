import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Requirements Explorer", page_icon="📄", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    div[data-testid="stSidebarNav"] { display: none !important; }
    html, body, [data-testid="stAppViewContainer"], .main { font-family: "Segoe UI", sans-serif !important; background-color: #f8f9fa !important; }
    .app-header { background-color: #24292e; padding: 16px 24px; margin: -6rem -5rem 2rem -5rem; color: white; display: flex; justify-content: space-between; align-items: center; position: relative; z-index: 999999; }
    .blade-title { border-left: 4px solid #005a9e; padding-left: 16px; margin-top: 10px; margin-bottom: 25px; }
    .blade-title h2 { font-size: 22px !important; font-weight: 600; color: #242424; margin: 0; }
</style>
""", unsafe_allow_html=True)

# --- REPLICATED CONSTANT SIDEBAR ---
st.sidebar.markdown("<h2 style='margin-top:0; color:#242424; font-size:18px; font-weight:600;'>🧪 Research Suite</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>Workspace Overview</p>", unsafe_allow_html=True)
if st.sidebar.button("🏠 Core Dashboard Dashboard", use_container_width=True): st.switch_page("Project/app.py")

st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>📋 Requirements & Backlogs</p>", unsafe_allow_html=True)
if st.sidebar.button("📄 Backlog Requirements Explorer", use_container_width=True, type="primary"): st.switch_page("Project/requirements_explorer.py")
if st.sidebar.button("🧠 NLP Parsing Pipeline", use_container_width=True): st.switch_page("Project/nlp_processing.py")

st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>🤖 Intelligence & Pipelines</p>", unsafe_allow_html=True)
if st.sidebar.button("🤖 ML Risk Engine Logs", use_container_width=True): st.switch_page("Project/prediction.py")

st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>🧪 Verification & Runs</p>", unsafe_allow_html=True)
if st.sidebar.button("🧪 Automated Test Suite", use_container_width=True): st.switch_page("Project/test_generation.py")
if st.sidebar.button("⭐ Optimization Queue Matrix", use_container_width=True): st.switch_page("Project/prioritization.py")

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Disconnect Session", use_container_width=True):
    st.session_state.authenticated = False
    st.switch_page("Project/app.py")

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Please sign in via the Core Dashboard first.")
    st.stop()

st.markdown("<div class='app-header'><div style='font-weight: 600;'>🔬 Automated Optimization Engine &nbsp;|&nbsp; <span style='font-weight: 300;'>MSc Dissertation Research Framework</span></div><div style='font-size: 13px;'>👤 admin@university.edu</div></div>", unsafe_allow_html=True)
st.markdown("<div class='blade-title'><h2>📋 Software Requirements Backlog Matrix</h2><p>Active Epics, Features, and Functional User Stories Baseline Matrix</p></div>", unsafe_allow_html=True)

try:
    conn = sqlite3.connect("Project/database/requirements.db")
    df = pd.read_sql_query("SELECT id AS [ID], title AS [Title], description AS [Acceptance Criteria], created_at AS [Created Date] FROM Requirements", conn)
    conn.close()
    st.dataframe(df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"❌ Database error: {e}")
