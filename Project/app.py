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

db_path = "Project/database/requirements.db"
models_dir = "Project/models"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- SHARED ENTERPRISE CSS ---
st.markdown("""
<style>
    /* Hide the ugly default native page links permanently */
    div[data-testid="stSidebarNav"] { display: none !important; }
    
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: "Segoe UI", -apple-system, sans-serif !important;
        background-color: #f8f9fa !important;
    }
    .app-header {
        background-color: #24292e; padding: 16px 24px; margin: -6rem -5rem 2rem -5rem;
        color: white; display: flex; justify-content: space-between; align-items: center;
        position: relative; z-index: 999999;
    }
    .blade-title {
        border-left: 4px solid #005a9e; padding-left: 16px; margin-top: 10px; margin-bottom: 25px;
    }
    .blade-title h2 { font-size: 22px !important; font-weight: 600; color: #242424; margin: 0; }
    div[data-testid="stForm"] { border: 1px solid #dadada !important; border-radius: 4px !important; background-color: #ffffff; padding: 24px !important; }
    div[data-testid="stMetricValue"] { font-size: 26px !important; color: #005a9e !important; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --- THE CONSTANT NAVIGATION BAR FUNCTION ---
def render_constant_sidebar(current_page="home"):
    st.sidebar.markdown("<h2 style='margin-top:0; color:#242424; font-size:18px; font-weight:600;'>🧪 Research Suite</h2>", unsafe_allow_html=True)
    
    st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>Workspace Overview</p>", unsafe_allow_html=True)
    if st.sidebar.button("🏠 Core Dashboard Dashboard", use_container_width=True, type="primary" if current_page == "home" else "secondary"):
        st.switch_page("app.py")
        
    st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>📋 Requirements & Backlogs</p>", unsafe_allow_html=True)
    if st.sidebar.button("📄 Backlog Requirements Explorer", use_container_width=True, type="primary" if current_page == "req" else "secondary"):
        st.switch_page("pages/1_📄_Requirements.py")
    if st.sidebar.button("🧠 NLP Parsing Pipeline", use_container_width=True, type="primary" if current_page == "nlp" else "secondary"):
        st.switch_page("pages/2_🧠_NLP_Processing.py")
        
    st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>🤖 Intelligence & Pipelines</p>", unsafe_allow_html=True)
    if st.sidebar.button("🤖 ML Risk Engine Logs", use_container_width=True, type="primary" if current_page == "pred" else "secondary"):
        st.switch_page("pages/3_🤖_Prediction.py")
        
    st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>🧪 Verification & Runs</p>", unsafe_allow_html=True)
    if st.sidebar.button("🧪 Automated Test Suite", use_container_width=True, type="primary" if current_page == "test" else "secondary"):
        st.switch_page("pages/4_🧪_Test_Generation.py")
    if st.sidebar.button("⭐ Optimization Queue Matrix", use_container_width=True, type="primary" if current_page == "priorit" else "secondary"):
        st.switch_page("pages/5_⭐_Prioritization.py")
        
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Disconnect Session", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# --- SECURITY PROTECTION GATEWAY ---
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
                else: st.error("❌ Access Denied.")
    st.stop()

# Force rendering of the static sidebar layout
render_constant_sidebar(current_page="home")

# Main Content Layout
st.markdown("<div class='app-header'><div style='font-weight: 600;'>🔬 Automated Optimization Engine &nbsp;|&nbsp; <span style='font-weight: 300;'>MSc Dissertation Research Framework</span></div><div style='font-size: 13px;'>👤 admin@university.edu</div></div>", unsafe_allow_html=True)
st.markdown("<div class='blade-title'><h2>📋 Software Requirements Backlog Repository</h2><p>Parse natural language user stories dynamically into prioritized continuous testing queues.</p></div>", unsafe_allow_html=True)

# [Remaining dashboard elements, charts, and database submission form logic from your file...]
