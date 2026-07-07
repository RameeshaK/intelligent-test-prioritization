import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Prioritization Queue", page_icon="⭐", layout="wide")
st.title("⭐ Optimally Prioritized Execution Queue")

conn = sqlite3.connect("/content/Project/database/requirements.db")
# Fetch ranked items
df = pd.read_sql_query("SELECT final_rank, calculated_priority_score, test_scenario, test_case_type FROM GeneratedTestCases ORDER BY final_rank ASC", conn)
conn.close()

st.markdown("### Final Evaluated Optimization Execution Matrix")
st.dataframe(df, use_container_width=True, hide_index=True)
st.success("🎯 Continuous Integration testing pipeline optimized successfully!")
