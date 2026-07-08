import streamlit as st
import sqlite3
import pandas as pd

# 1. Configure page settings
st.set_page_config(
    page_title="Optimization Queue",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Apply shared styling and hide native navigation completely
st.markdown("""
<style>
    /* Hide default sidebar links */
    div[data-testid="stSidebarNav"] { display: none !important; }
    
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: "Segoe UI", -apple-system, sans-serif !important;
        background-color: #f8f9fa !important;
    }
    
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
</style>
""", unsafe_allow_html=True)

# 3. Render the identical custom sidebar navigation layout
st.sidebar.markdown("<h2 style='margin-top:0; color:#242424; font-size:18px; font-weight:600;'>🧪 Research Suite</h2>", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>Workspace Overview</p>", unsafe_allow_html=True)
if st.sidebar.button("🏠 Core Dashboard Dashboard", use_container_width=True):
    st.switch_page("app.py")
    
st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>📋 Requirements & Backlogs</p>", unsafe_allow_html=True)
if st.sidebar.button("📄 Backlog Requirements Explorer", use_container_width=True):
    st.switch_page("requirements_explorer.py")
if st.sidebar.button("🧠 NLP Parsing Pipeline", use_container_width=True):
    st.switch_page("nlp_processing.py")
    
st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>🤖 Intelligence & Pipelines</p>", unsafe_allow_html=True)
if st.sidebar.button("🤖 ML Risk Engine Logs", use_container_width=True):
    st.switch_page("prediction.py")
    
st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>🧪 Verification & Runs</p>", unsafe_allow_html=True)
if st.sidebar.button("🧪 Automated Test Suite", use_container_width=True):
    st.switch_page("test_generation.py")
if st.sidebar.button("⭐ Optimization Queue Matrix", use_container_width=True, type="primary"):
    st.switch_page("prioritization.py")

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Disconnect Session", use_container_width=True):
    st.session_state.authenticated = False
    st.switch_page("app.py")

# 4. Check Authentication State
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Please sign in via the Core Dashboard first.")
    st.stop()

# 5. Render Page Headers
st.markdown("<div class='app-header'><div style='font-weight: 600;'>🔬 Automated Optimization Engine &nbsp;|&nbsp; <span style='font-weight: 300;'>MSc Dissertation Research Framework</span></div><div style='font-size: 13px;'>👤 admin@university.edu</div></div>", unsafe_allow_html=True)
st.markdown("<div class='blade-title'><h2>⭐ Test Optimization & Execution Queue Prioritization Matrix</h2><p>Calculated queue hierarchy maps ordered execution indexes derived from the analytics engine</p></div>", unsafe_allow_html=True)

# 6. Database Connection and UI View Data Rendering
try:
    conn = sqlite3.connect("Project/database/requirements.db")
    df = pd.read_sql_query("""
        SELECT 
            tc.final_rank AS [Execution Rank],
            r.title AS [Requirement Target],
            tc.test_scenario AS [Optimized Test Target],
            p.predicted_risk_level AS [Engine Risk Profile],
            tc.calculated_priority_score AS [Priority Matrix Score]
        FROM GeneratedTestCases tc
        JOIN Requirements r ON tc.requirement_id = r.id
        JOIN Predictions p ON tc.prediction_id = p.prediction_id
        ORDER BY tc.final_rank ASC
    """, conn)
    conn.close()
    
    if df.empty:
        st.info("ℹ️ Queue prioritization is clear. Complete a pipeline run from the dashboard to optimize test execution paths.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"❌ Database Connection Link Offline: {e}")
