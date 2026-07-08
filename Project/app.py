import streamlit as st
import sqlite3
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Intelligent Test Case Prioritization Framework",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Track the active view using session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"

# 3. Global Styling
st.markdown("""
<style>
    /* No native navigation menu to hide anymore, but keeping styles clean */
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
</style>
""", unsafe_allow_html=True)

# 4. Security Gateway
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

# --- 5. THE PERFECT CUSTOM SIDEBAR (State Changer) ---
st.sidebar.markdown("<h2 style='margin-top:0; color:#242424; font-size:18px; font-weight:600;'>🧪 Research Suite</h2>", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>Workspace Overview</p>", unsafe_allow_html=True)
if st.sidebar.button("🏠 Core Dashboard Dashboard", use_container_width=True, type="primary" if st.session_state.active_page == "Dashboard" else "secondary"):
    st.session_state.active_page = "Dashboard"
    st.rerun()
    
st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>📋 Requirements & Backlogs</p>", unsafe_allow_html=True)
if st.sidebar.button("📄 Backlog Requirements Explorer", use_container_width=True, type="primary" if st.session_state.active_page == "Explorer" else "secondary"):
    st.session_state.active_page = "Explorer"
    st.rerun()
if st.sidebar.button("🧠 NLP Parsing Pipeline", use_container_width=True, type="primary" if st.session_state.active_page == "NLP" else "secondary"):
    st.session_state.active_page = "NLP"
    st.rerun()
    
st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>🤖 Intelligence & Pipelines</p>", unsafe_allow_html=True)
if st.sidebar.button("🤖 ML Risk Engine Logs", use_container_width=True, type="primary" if st.session_state.active_page == "Prediction" else "secondary"):
    st.session_state.active_page = "Prediction"
    st.rerun()
    
st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>🧪 Verification & Runs</p>", unsafe_allow_html=True)
if st.sidebar.button("🧪 Automated Test Suite", use_container_width=True, type="primary" if st.session_state.active_page == "TestGen" else "secondary"):
    st.session_state.active_page = "TestGen"
    st.rerun()
if st.sidebar.button("⭐ Optimization Queue Matrix", use_container_width=True, type="primary" if st.session_state.active_page == "Prioritization" else "secondary"):
    st.session_state.active_page = "Prioritization"
    st.rerun()

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Disconnect Session", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

# --- 6. GLOBAL TOP HEADER PANEL ---
st.markdown("<div class='app-header'><div style='font-weight: 600;'>🔬 Automated Optimization Engine &nbsp;|&nbsp; <span style='font-weight: 300;'>MSc Dissertation Research Framework</span></div><div style='font-size: 13px;'>👤 admin@university.edu</div></div>", unsafe_allow_html=True)


# --- 7. DYNAMIC PAGE ROUTER ---

# === PAGE A: DASHBOARD ===
if st.session_state.active_page == "Dashboard":
    st.markdown("<div class='blade-title'><h2>📋 Software Requirements Backlog Repository</h2><p>Parse natural language user stories dynamically into prioritized continuous testing queues.</p></div>", unsafe_allow_html=True)
    st.write("Welcome to your Core Research Workspace! Add data logs or trigger pipeline events below.")
    # [Insert your core workspace form code & tracking metrics here]

# === PAGE B: REQUIREMENTS EXPLORER ===
elif st.session_state.active_page == "Explorer":
    st.markdown("<div class='blade-title'><h2>📋 Software Requirements Backlog Matrix</h2><p>Active Epics, Features, and Functional User Stories Baseline Matrix</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect("Project/database/requirements.db")
        df = pd.read_sql_query("SELECT id AS [ID], title AS [Title], description AS [Acceptance Criteria], created_at AS [Created Date] FROM Requirements", conn)
        conn.close()
        if df.empty: st.info("ℹ️ No requirements logged in the database yet.")
        else: st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Database Link Offline: {e}")

# === PAGE C: NLP PIPELINE ===
elif st.session_state.active_page == "NLP":
    st.markdown("<div class='blade-title'><h2>🧠 NLP Feature Token Extraction Pipeline</h2><p>Normalized input vectors and analytical sequence processing logs</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect("Project/database/requirements.db")
        df = pd.read_sql_query("SELECT nlp_id AS [NLP ID], requirement_id AS [Req ID], cleaned_text AS [Normalized String], tokens AS [Tokens] FROM NLPResults", conn)
        conn.close()
        if df.empty: st.info("ℹ️ No NLP processing results found.")
        else: st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Database Link Offline: {e}")

# === PAGE D: ML ENGINE ===
elif st.session_state.active_page == "Prediction":
    st.markdown("<div class='blade-title'><h2>🤖 ML Risk Classification Analysis Engine</h2><p>Predictive risk bounds mapping requirements to automated execution vulnerabilities</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect("Project/database/requirements.db")
        df = pd.read_sql_query("SELECT p.prediction_id AS [Prediction ID], r.title AS [Requirement Title], p.predicted_risk_level AS [Predicted Risk Level], p.confidence_score AS [Confidence Score], p.xai_explanation AS [Explainable AI Log] FROM Predictions p JOIN Requirements r ON p.requirement_id = r.id", conn)
        conn.close()
        if df.empty: st.info("ℹ️ No model evaluation metrics found yet.")
        else: st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Database Link Offline: {e}")

# === PAGE E: AUTOMATED TEST SUITE ===
elif st.session_state.active_page == "TestGen":
    st.markdown("<div class='blade-title'><h2>🧪 Automated Functional Test Suite Matrix</h2><p>Synthesized system test coverage scenarios generated directly from user story validation logs</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect("Project/database/requirements.db")
        df = pd.read_sql_query("SELECT tc_id AS [Test Case ID], test_scenario AS [Scenario Context], test_objective AS [Objective Goals], expected_result AS [Expected Bounds] FROM GeneratedTestCases", conn)
        conn.close()
        if df.empty: st.info("ℹ️ Test execution profiles are currently empty.")
        else: st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Database Link Offline: {e}")

# === PAGE F: OPTIMIZATION QUEUE ===
elif st.session_state.active_page == "Prioritization":
    st.markdown("<div class='blade-title'><h2>⭐ Test Optimization & Execution Queue Prioritization Matrix</h2><p>Calculated queue hierarchy maps ordered execution indexes derived from the analytics engine</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect("Project/database/requirements.db")
        df = pd.read_sql_query("SELECT tc.final_rank AS [Execution Rank], r.title AS [Requirement Target], tc.test_scenario AS [Optimized Test Target], tc.calculated_priority_score AS [Priority Matrix Score] FROM GeneratedTestCases tc JOIN Requirements r ON tc.requirement_id = r.id ORDER BY tc.final_rank ASC", conn)
        conn.close()
        if df.empty: st.info("ℹ Broad queue prioritization is clear.")
        else: st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Database Link Offline: {e}")
