import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Requirements View", page_icon="📄", layout="wide")
st.title("📄 Software Requirements Repository")

conn = sqlite3.connect("Project/database/requirements.db")
df = pd.read_sql_query("SELECT * FROM Requirements", conn)
conn.close()

st.markdown("### Active Research Requirements Baseline")
st.dataframe(df, use_container_width=True, hide_index=True)
