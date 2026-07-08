import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="NLP Pipelines", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    div[data-testid="stSidebarNav"] { display: none !important; }
    html, body, [data-testid="stAppViewContainer"], .main { font-family: "Segoe UI", sans-serif !important; }
    .blade-title { border-left: 4px solid #005a9e; padding-left: 16px; margin-bottom: 25px; }
    .blade-title h2 { font-size: 22px !important; font-weight: 600; color: #242424; margin:0; }
</style>
""", unsafe_allow_html=True)

# Re-render Unified Navigation Menu Sidebar
st.sidebar.markdown("<h2 style='margin-top:0; color:#242424; font-size:18px; font-weight:600;'>🧪 Research Suite</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>Workspace Overview</p>", unsafe_allow_html=True)
if st.sidebar.button("🏠 Core Dashboard Dashboard", use_container_width=True): st.switch_page("app.py")
st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>📋 Requirements & Backlogs</p>", unsafe_allow_html=True)
if st.sidebar.button("📄 Backlog Requirements Explorer", use_container_width=True): st.switch_page("pages/1_📄_Requirements.py")
if st.sidebar.button("🧠 NLP Parsing Pipeline", use_container_width=True, type="primary"): st.switch_page("pages/2_🧠_NLP_Processing.py")
st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>🤖 Intelligence & Pipelines</p>", unsafe_allow_html=True)
if st.sidebar.button("🤖 ML Risk Engine Logs", use_container_width=True): st.switch_page("pages/3_🤖_Prediction.py")
st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>🧪 Verification & Runs</p>", unsafe_allow_html=True)
if st.sidebar.button("🧪 Automated Test Suite", use_container_width=True): st.switch_page("pages/4_🧪_Test_Generation.py")
if st.sidebar.button("⭐ Optimization Queue Matrix", use_container_width=True): st.switch_page("pages/5_⭐_Prioritization.py")

st.markdown("<div class='blade-title'><h2>🧠 NLP Feature Token Extraction Pipeline</h2></div>", unsafe_allow_html=True)

try:
    conn = sqlite3.connect("Project/database/requirements.db") # Corrected portable path
    df = pd.read_sql_query("SELECT nlp_id AS [NLP ID], requirement_id AS [Req ID], cleaned_text AS [Normalized String], tokens AS [Tokens] FROM NLPResults", conn)
    conn.close()
    st.dataframe(df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Database Connection Link Offline: {e}")
