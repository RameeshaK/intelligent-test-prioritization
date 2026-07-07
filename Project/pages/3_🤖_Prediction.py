import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="ML Predictions", page_icon="🤖", layout="wide")
st.title("🤖 ML Risk Level Classifications")

conn = sqlite3.connect("/content/Project/database/requirements.db")
df = pd.read_sql_query("SELECT requirement_id, predicted_risk_level, confidence_score, xai_explanation FROM Predictions", conn)
conn.close()

st.markdown("### Supervised Model Outputs & XAI Accountability Log")
st.dataframe(df, use_container_width=True, hide_index=True)
