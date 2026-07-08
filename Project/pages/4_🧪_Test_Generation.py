import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Automated Test Cases", page_icon="🧪", layout="wide")
st.title("🧪 Automatically Generated Test Suites")

conn = sqlite3.connect("Project/database/requirements.db")
df = pd.read_sql_query("SELECT test_case_id, test_scenario, test_objective, test_case_type FROM GeneratedTestCases", conn)
conn.close()

st.markdown("### Derived Functional Verification Test Requirements")
st.dataframe(df, use_container_width=True, hide_index=True)
