import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="NLP Pipelines", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: "Segoe UI", -apple-system, sans-serif !important;
        background-color: #f8f9fa !important;
    }
    .blade-title {
        border-left: 4px solid #005a9e; 
        padding-left: 16px; 
        margin-top: 10px;
        margin-bottom: 25px;
    }
    .blade-title h2 { font-size: 22px !important; font-weight: 600; color: #242424; margin:0; }
    .blade-title p { color: #616161; font-size: 13px; margin: 4px 0 0 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='blade-title'><h2>🧠 NLP Feature Token Extraction Pipeline</h2><p>Normalized input vectors and analytical sequence processing logs</p></div>", unsafe_allow_html=True)

try:
    conn = sqlite3.connect("Project/database/requirements.db")
    df = pd.read_sql_query("SELECT nlp_id AS [NLP ID], requirement_id AS [Req ID], cleaned_text AS [Normalized String], tokens AS [Tokens] FROM NLPResults", conn)
    conn.close()
    st.dataframe(df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Database Connection Link Offline: {e}")
