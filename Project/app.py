import streamlit as st
import sqlite3
import pandas as pd
import os
import re
import joblib
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

st.set_page_config(
    page_title="Intelligent Test Case Prioritization Framework",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PORTABLE RELATIVE DATABASE PATHS ---
db_path = "Project/database/requirements.db"
models_dir = "Project/models"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- NATIVE SIDEBAR BRANDING STYLES ---
st.markdown("""
<style>
    /* Global Clean Typography Reset */
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: "Segoe UI", -apple-system, sans-serif !important;
        background-color: #f8f9fa !important;
    }
    
    /* Native Sidebar Menu Link Customizations */
    [data-testid="stSidebarNav"] {
        padding-top: 20px !important;
    }
    [data-testid="stSidebarNav"] ul {
        padding-top: 10px !important;
    }
    
    /* Topbar Header Design */
    .app-header {
        background-color: #24292e; 
        padding: 16px 24px; 
        margin: -6rem -5rem 2rem -5rem;
        color: white; 
        display: flex; 
        justify-content: space-between; 
        align-items: center;
        position: relative;
        z-index: 999999;
    }
    
    .blade-title {
        border-left: 4px solid #005a9e; 
        padding-left: 16px; 
        margin-top: 10px;
        margin-bottom: 25px;
    }
    .blade-title h2 { font-size: 22px !important; font-weight: 600; color: #242424; margin: 0; }
    div[data-testid="stForm"] { border: 1px solid #dadada !important; border-radius: 4px !important; background-color: #ffffff; padding: 24px !important; }
    div[data-testid="stMetricValue"] { font-size: 26px !important; color: #005a9e !important; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --- SECURITY SYSTEM SIGN-IN ---
if not st.session_state.authenticated:
    st.markdown("<div class='app-header'><div style='font-weight: 600;'>🔬 Intelligent Test Case Prioritization Framework</div></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<div style='text-align: center; margin-top: 40px; margin-bottom: 20px;'><h2 style='font-weight:400; color:#242424;'>MSc Research Portal Sign-In</h2></div>", unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("Directory ID / Email", placeholder="admin")
            password = st.text_input("Access Security Key", type="password")
            if st.form_submit_button("Sign In"):
                if username == "admin" and password == "msc_secure2026":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Access Denied.")
    st.stop()

# --- MAIN DASHBOARD WORKSPACE PANELS ---
st.markdown("<div class='app-header'><div style='font-weight: 600;'>🔬 Automated Optimization Engine &nbsp;|&nbsp; <span style='font-weight: 300;'>MSc Dissertation Research Framework</span></div><div style='font-size: 13px;'>👤 admin@university.edu</div></div>", unsafe_allow_html=True)
st.markdown("<div class='blade-title'><h2>📋 Software Requirements Backlog Repository</h2><p>Parse natural language user stories dynamically into prioritized continuous testing queues.</p></div>", unsafe_allow_html=True)

def load_dashboard_metrics():
    try:
        conn = sqlite3.connect(db_path)
        req_count = pd.read_sql_query("SELECT COUNT(*) as total FROM Requirements", conn)['total'].iloc[0]
        pred_count = pd.read_sql_query("SELECT COUNT(*) as total FROM Predictions", conn)['total'].iloc[0]
        tc_count = pd.read_sql_query("SELECT COUNT(*) as total FROM GeneratedTestCases", conn)['total'].iloc[0]
        risk_df = pd.read_sql_query("SELECT predicted_risk_level AS [Risk Category], COUNT(*) as [Work Items Count] FROM Predictions GROUP BY predicted_risk_level", conn)
        conn.close()
        return req_count, pred_count, tc_count, risk_df
    except Exception:
        return 0, 0, 0, pd.DataFrame()

req_count, pred_count, tc_count, risk_df = load_dashboard_metrics()

col1, col2, col3 = st.columns(3)
with col1: st.metric(label="Total Logged Requirements", value=req_count)
with col2: st.metric(label="Evaluated ML Risk Indexes", value=pred_count)
with col3: st.metric(label="Automated Test Scenarios Created", value=tc_count)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### ➕ Analyze New User Story / Requirement")
with st.form("requirement_form", clear_on_submit=True):
    col_t, col_d = st.columns([1, 2])
    with col_t: new_title = st.text_input("Requirement Title", placeholder="As a system user...")
    with col_d: new_desc = st.text_area("Acceptance Criteria Details", placeholder="Given some context...")
    submit_button = st.form_submit_button("⚡ Run Pipeline & Analyze Requirement")

if submit_button and new_title.strip() and new_desc.strip():
    try:
        rf_model = joblib.load(os.path.join(models_dir, "random_forest_model.pkl"))
        combined_text = f"{new_title} {new_desc}".lower()
        cleaned_text = re.sub(r'[^a-zA-Z\s]', '', combined_text)
        
        vectorizer = TfidfVectorizer(max_features=rf_model.n_features_in_)
        try:
            conn = sqlite3.connect(db_path)
            backup_text = pd.read_sql_query("SELECT cleaned_text FROM NLPResults", conn)
            conn.close()
            corpus = backup_text['cleaned_text'].tolist() if not backup_text.empty else []
        except Exception:
            corpus = []
            
        corpus.append(cleaned_text)
        vectorizer.fit(corpus)
        
        tfidf_vector = vectorizer.transform([cleaned_text])
        dense_vector = tfidf_vector.toarray()[0]
        
        expected_features = rf_model.n_features_in_
        if dense_vector.shape[0] < expected_features:
            dense_vector = np.pad(dense_vector, (0, expected_features - dense_vector.shape[0]), 'constant')
        else:
            dense_vector = dense_vector[:expected_features]
            
        final_input_matrix = dense_vector.reshape(1, -1)
        pred_idx = rf_model.predict(final_input_matrix)[0]
        probabilities = rf_model.predict_proba(final_input_matrix)[0]
        
        label_map = {0: "High", 1: "Medium", 2: "Low"}
        predicted_label = label_map.get(pred_idx, "Medium")
        confidence_score = probabilities[pred_idx]
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("INSERT INTO Requirements (title, description, created_at) VALUES (?, ?, ?)", (new_title.strip(), new_desc.strip(), timestamp))
        req_id = cursor.lastrowid
        cursor.execute("INSERT INTO NLPResults (requirement_id, cleaned_text, tokens, lemmas, processed_at) VALUES (?, ?, ?, ?, ?)", (req_id, cleaned_text, str(cleaned_text.split()), str(cleaned_text.split()), timestamp))
        cursor.execute("INSERT INTO Predictions (requirement_id, predicted_risk_level, confidence_score, xai_explanation, predicted_at) VALUES (?, ?, ?, ?, ?)", (req_id, predicted_label, float(confidence_score), "Top Keywords used", timestamp))
        
        pred_id = cursor.lastrowid
        cursor.execute("INSERT INTO GeneratedTestCases (requirement_id, prediction_id, test_scenario, test_objective, preconditions, test_steps, expected_result, test_case_type, calculated_priority_score, final_rank, created_at) VALUES (?, ?, ?, ?, 'Session context verified', '1. Execute interfaces.', 'System success.', 'Positive', 2.50, 1, ?)", (req_id, pred_id, f"Verify {new_title} integrity", "Validate functional states", timestamp))
        
        conn.commit()
        conn.close()
        st.success("🎯 Requirement pipeline run executed successfully.")
        st.rerun()
    except Exception as e:
        st.error(f"Execution Error: {e}")

if not risk_df.empty:
    st.markdown("### 📊 Active Repository Risk Balance Index Summary")
    st.dataframe(risk_df, use_container_width=True, hide_index=True)
