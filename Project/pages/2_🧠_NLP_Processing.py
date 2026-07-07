import streamlit as st
import sqlite3
import pandas as pd
import json

st.set_page_config(page_title="NLP Features", page_icon="🧠", layout="wide")
st.title("🧠 Natural Language Processing Tokenizer View")

conn = sqlite3.connect("/content/Project/database/requirements.db")
df = pd.read_sql_query("SELECT nlp_id, requirement_id, cleaned_text FROM NLPResults", conn)
conn.close()

st.markdown("### Normalized Linguistic Features (Stop Words Removed)")
st.dataframe(df, use_container_width=True, hide_index=True)
