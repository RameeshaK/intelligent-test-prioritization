import streamlit as st
import sqlite3
import pandas as pd
import os
import re
import joblib
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

# --- CLEAN INTERFACE CONFIGURATION ---
st.set_page_config(
    page_title="Intelligent Test Case Prioritization Framework",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

db_path = "Project/database/requirements.db"
models_dir = "Project/models"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- FRONTEND STRUCTURE & ALIGNMENT ENHANCEMENTS ---
st.markdown("""
<style>
    /* Hide default Streamlit sidebar page list navigation links */
    div[data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Global Clean Typography Reset */
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif !important;
        background-color: #f8f9fa !important;
        color: #333333 !important;
    }
    
    /* Premium Application Topbar Header */
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
    
    /* Structured Left-border Accent Blade Header */
    .blade-title {
        border-left: 4px solid #005a9e; 
        padding-left: 16px; 
        margin-top: 10px;
        margin-bottom: 25px;
    }
    .blade-title h2 {
        font-size: 22px !important;
        font-weight: 600 !important;
        color: #242424 !important;
        margin: 0 !important;
    }
    .blade-title p {
        color: #616161 !important; 
        margin: 4px 0 0 0 !important; 
        font-size: 13px !important;
    }

    /* Crisp Enterprise Input Container */
    div[data-testid="stForm"] {
        border: 1px solid #dadada !important;
        border-radius: 4px !important;
        background-color: #ffffff !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        padding: 24px !important;
    }

    /* Dynamic Metric Displays Metrics Formatting */
    div[data-testid="stMetricValue"] {
        font-size: 26px !important; 
        color: #005a9e !important; 
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SECURE SPREAD ACCESSIBILITY GATEWAY ---
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

# --- PROFESSIONAL APPLICATION SIDEBAR NAVIGATION OVERHAUL ---
st.sidebar.markdown("<h2 style='margin-top:0; color:#242424; font-size:18px; font-weight:600;'>🧪 Research Suite</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>Workspace Overview</p>", unsafe_allow_html=True)

# Navigation Buttons replacing the ugly default list
if st.sidebar.button("🏠 Core Dashboard Dashboard", use_container_width=True, type="primary"):
    st.switch_page("app.py")

st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>📋 Requirements & Backlogs</p>", unsafe_allow_html=True)
if st.sidebar.button("📄 Backlog Requirements Explorer", use_container_width=True):
    st.switch_page("pages/1_📄_Requirements.py")
if st.sidebar.button("🧠 NLP Parsing Pipeline", use_container_width=True):
    st.switch_page("pages/2_🧠_NLP_Processing.py")

st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>🤖 Intelligence & Pipelines</p>", unsafe_allow_html=True)
if st.sidebar.button("🤖 ML Risk Engine Logs", use_container_width=True):
    st.switch_page("pages/3_🤖_Prediction.py")

st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>🧪 Verification & Runs</p>", unsafe_allow_html=True)
if st.sidebar.button("🧪 Automated Test Suite", use_container_width=True):
    st.switch_page("pages/4_🧪_Test_Generation.py")
if st.sidebar.button("⭐ Optimization Queue Matrix", use_container_width=True):
    st.switch_page("pages/5_⭐_Prioritization.py")

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Disconnect Session", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

# --- MAIN DASHBOARD AREA ---
st.markdown("<div class='app-header'><div style='font-weight: 600;'>🔬 Automated Optimization Engine &nbsp;|&nbsp; <span style='font-weight: 300;'>MSc Dissertation Research Framework</span></div><div style='font-size: 13px;'>👤 admin@university.edu</div></div>", unsafe_allow_html=True)

st.markdown("<div class='blade-title'><h2>📋 Software Requirements Backlog Repository</h2><p>Parse natural language user stories dynamically into prioritized continuous testing and validation queues.</p></div>", unsafe_allow_html=True)

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
with col1:
    st.metric(label="Total Logged Requirements", value=req_count)
with col2:
    st.metric(label="Evaluated ML Risk Indexes", value=pred_count)
with col3:
    st.metric(label="Automated Test Scenarios Created", value=tc_count)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### ➕ Analyze New User Story / Requirement")
with st.form("requirement_form", clear_on_submit=True):
    col_t, col_d = st.columns([1, 2])
    with col_t:
        new_title = st.text_input("Requirement Title", placeholder="As a system user...")
    with col_d:
        new_desc = st.text_area("Acceptance Criteria Details", placeholder="Given some initial context, when an action happens, then validate results...")
    submit_button = st.form_submit_button("⚡ Commit Content to Framework Pipeline")

if submit_button and new_title.strip() and new_desc.strip():
    try:
        rf_model = joblib.load(os.path.join(models_dir, "random_forest_model.pkl"))
        combined_text = f"{new_title} {new_desc}".lower()
        cleaned_text = re.sub(r'[^a-zA-Z\s]', '', combined_text)
        
        conn = sqlite3.connect(db_path)
        backup_text = pd.read_sql_query("SELECT cleaned_text FROM NLPResults", conn)
        conn.close()
        
        training_corpus = backup_text['cleaned_text'].tolist() if not backup_text.empty else []
        training_corpus.append(cleaned_text)
        
        vectorizer = TfidfVectorizer(max_features=100)
        vectorizer.fit(training_corpus)
        tfidf_vector = vectorizer.transform([cleaned_text])
        dense_vector = tfidf_vector.toarray()[0]
        
        expected_features = rf_model.n_features_in_
        if dense_vector.shape[0] < expected_features:
            dense_vector = np.pad(dense_vector, (0, expected_features - dense_vector.shape[0]), 'constant')
        elif dense_vector.shape[0] > expected_features:
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
        scenarios = [("Verify Functional Requirement User Story Feature UI", "Positive", "Confirm components adhere to specs.", 2.00)]
        for scen, ttype, obj, p_score in scenarios:
            cursor.execute("INSERT INTO GeneratedTestCases (requirement_id, prediction_id, test_scenario, test_objective, preconditions, test_steps, expected_result, test_case_type, calculated_priority_score, final_rank, created_at) VALUES (?, ?, ?, ?, 'Secure session loaded', '1. Input.', 'Success.', ?, ?, 99, ?)", (req_id, pred_id, scen, obj, ttype, p_score, timestamp))
        
        cursor.execute("UPDATE GeneratedTestCases SET final_rank = (SELECT COUNT(*) + 1 FROM GeneratedTestCases g2 WHERE g2.calculated_priority_score > GeneratedTestCases.calculated_priority_score)")
        conn.commit()
        conn.close()
        st.success("🚀 Work Item Committed.")
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")

if not risk_df.empty:
    st.markdown("### 📊 Active Repository Risk Balance Index Summary")
    st.dataframe(risk_df, use_container_width=True, hide_index=True)
