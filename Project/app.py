import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="MSc Prioritization Framework Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_dashboard_metrics():
    db_path = "/content/Project/database/requirements.db"
    try:
        conn = sqlite3.connect(db_path)
        req_count = pd.read_sql_query("SELECT COUNT(*) as total FROM Requirements", conn)['total'].iloc[0]
        pred_count = pd.read_sql_query("SELECT COUNT(*) as total FROM Predictions", conn)['total'].iloc[0]
        tc_count = pd.read_sql_query("SELECT COUNT(*) as total FROM GeneratedTestCases", conn)['total'].iloc[0]
        risk_df = pd.read_sql_query("SELECT predicted_risk_level, COUNT(*) as count FROM Predictions GROUP BY predicted_risk_level", conn)
        conn.close()
        return req_count, pred_count, tc_count, risk_df
    except Exception:
        return 0, 0, 0, pd.DataFrame()

req_count, pred_count, tc_count, risk_df = load_dashboard_metrics()

st.sidebar.markdown("## 📚 MSc Research Profile")
st.sidebar.info("**Project:** Intelligent Test Case Prioritization Framework\n\n**Infrastructure:** Cloud Engine")

st.title("🏠 Framework Executive Dashboard")
st.markdown("Welcome to the analytical center of your **MSc Dissertation Framework**.")

st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Raw Requirements Logged", value=req_count)
with col2:
    st.metric(label="ML Predictions Processed", value=pred_count)
with col3:
    st.metric(label="Automated Test Cases Compiled", value=tc_count)

st.markdown("---")
st.subheader("📊 Empirical Risk Distribution (ML Classifier Output)")
if not risk_df.empty:
    st.dataframe(risk_df, use_container_width=True, hide_index=True)
else:
    st.warning("No classification matrix results found.")

st.success("✅ Main framework operational center loaded seamlessly.")
