import streamlit as st
import sqlite3
import pandas as pd

# Notice: No st.set_page_config() here anymore! The master navigation manager handles it.

st.markdown("""
<style>
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

st.markdown("<div class='blade-title'><h2>📋 Requirements Backlog Matrix</h2><p>Active Epics, Features, and Functional User Stories Baseline Matrix</p></div>", unsafe_allow_html=True)

try:
    conn = sqlite3.connect("Project/database/requirements.db")
    df = pd.read_sql_query("SELECT id AS [ID], title AS [Title], description AS [Acceptance Criteria], created_at AS [Created Date] FROM Requirements", conn)
    conn.close()
    st.dataframe(df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Database Connection Link Offline: {e}")
