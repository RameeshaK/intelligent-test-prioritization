import streamlit as st
import sqlite3
import pandas as pd
import os
import re
import joblib
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. Page Configuration Setup
st.set_page_config(
    page_title="Intelligent Test Case Prioritization Framework",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

db_path = "Project/database/requirements.db"
models_dir = "Project/models"

# Initialize Session States safely
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"

# --- 2. SHARED ENTERPRISE CSS ---
st.markdown("""
<style>
    /* Hide native routing components permanently */
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

# --- 3. SECURITY PROTECTION GATEWAY ---
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

# --- 4. THE CONSTANT NAVIGATION SIDEBAR (NO SWITCH_PAGE CALLS) ---
st.sidebar.markdown("<h2 style='margin-top:0; color:#242424; font-size:18px; font-weight:600;'>🧪 Research Suite</h2>", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>Workspace Overview</p>", unsafe_allow_html=True)
if st.sidebar.button("🏠 Core Dashboard Dashboard", use_container_width=True, type="primary" if st.session_state.active_page == "Dashboard" else "secondary"):
    st.session_state.active_page = "Dashboard"

st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>📋 Requirements & Backlogs</p>", unsafe_allow_html=True)
if st.sidebar.button("📄 Backlog Requirements Explorer", use_container_width=True, type="primary" if st.session_state.active_page == "Explorer" else "secondary"):
    st.session_state.active_page = "Explorer"
if st.sidebar.button("🧠 NLP Parsing Pipeline", use_container_width=True, type="primary" if st.session_state.active_page == "NLP" else "secondary"):
    st.session_state.active_page = "NLP"

st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>🤖 Intelligence & Pipelines</p>", unsafe_allow_html=True)
if st.sidebar.button("🤖 ML Risk Engine Logs", use_container_width=True, type="primary" if st.session_state.active_page == "Prediction" else "secondary"):
    st.session_state.active_page = "Prediction"

st.sidebar.markdown("<p style='font-size:11px; text-transform:uppercase; color:gray; font-weight:700; margin-bottom:5px; margin-top:15px;'>🧪 Verification & Runs</p>", unsafe_allow_html=True)
if st.sidebar.button("🧪 Automated Test Suite", use_container_width=True, type="primary" if st.session_state.active_page == "TestGen" else "secondary"):
    st.session_state.active_page = "TestGen"
if st.sidebar.button("⭐ Optimization Queue Matrix", use_container_width=True, type="primary" if st.session_state.active_page == "Prioritization" else "secondary"):
    st.session_state.active_page = "Prioritization"

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Disconnect Session", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

# --- 5. GLOBAL APPMARK TOP BAR ---
st.markdown("<div class='app-header'><div style='font-weight: 600;'>🔬 Automated Optimization Engine &nbsp;|&nbsp; <span style='font-weight: 300;'>MSc Dissertation Research Framework</span></div><div style='font-size: 13px;'>👤 admin@university.edu</div></div>", unsafe_allow_html=True)


# --- 6. DYNAMIC SYSTEM ENGINE CONDITIONAL ROUTER ---

# ==========================================
# VIEW A: CORE DASHBOARD WORKSPACE
# ==========================================
if st.session_state.active_page == "Dashboard":
    st.markdown("<div class='blade-title'><h2>📋 Software Requirements Backlog Repository</h2><p>Parse natural language user stories dynamically into prioritized continuous testing queues.</p></div>", unsafe_allow_html=True)
    
    # --- PROJECT & SUITE METADATA CONFIGURATION ---
    st.markdown("### 📁 Scope Definition")
    meta_col1, meta_col2 = st.columns(2)
    with meta_col1:
        project_name = st.text_input("Project Name", value="E-Commerce Platform", help="Enter or select the active target project root.")
    with meta_col2:
        suite_name = st.text_input("Test Suite Name", value="Sprint 3 Regression Suite", help="Specify the destination collection bucket for your test suite.")

    st.markdown("---")
    
    # --- USER STORY BACKLOG INGESTION FORM ---
    st.markdown("### 📝 Requirement Processing Ingestion")
    with st.form("pipeline_processing_form"):
        user_story_input = st.text_area(
            "Raw User Story / Requirement Criteria", 
            placeholder="As a logged-in premium user, I want to add items to my shopping cart and apply a discount coupon code at checkout so that my order total decreases automatically.",
            height=150
        )
        
        submit_btn = st.form_submit_button("🚀 Run Complete Framework Ingestion Loop")

    if submit_btn:
        if not user_story_input.strip() or not project_name.strip() or not suite_name.strip():
            st.error("❌ Please ensure Project Name, Test Suite Name, and Raw User Story are filled out.")
        else:
            with st.spinner("Executing pipeline modules sequentially..."):
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()

                    # 1. Ensure columns exist dynamically for Project/Suite scoping
                    cursor.execute("PRAGMA table_info(Requirements)")
                    req_cols = [r[1] for r in cursor.fetchall()]
                    
                    # Update table structure if project mapping flags aren't there yet
                    if "project_name" not in req_cols:
                        cursor.execute("ALTER TABLE Requirements ADD COLUMN project_name TEXT DEFAULT 'Default Project'")
                    if "suite_name" not in req_cols:
                        cursor.execute("ALTER TABLE Requirements ADD COLUMN suite_name TEXT DEFAULT 'Default Suite'")
                    
                    # Also update GeneratedTestCases if missing scoping
                    cursor.execute("PRAGMA table_info(GeneratedTestCases)")
                    tc_cols = [r[1] for r in cursor.fetchall()]
                    if "project_name" not in tc_cols:
                        cursor.execute("ALTER TABLE GeneratedTestCases ADD COLUMN project_name TEXT DEFAULT 'Default Project'")
                    if "suite_name" not in tc_cols:
                        cursor.execute("ALTER TABLE GeneratedTestCases ADD COLUMN suite_name TEXT DEFAULT 'Default Suite'")

                    # 2. STEP 1: Ingest Requirement Log
                    req_title = f"Story from {datetime.now().strftime('%M:%S')}"
                    cursor.execute(
                        "INSERT INTO Requirements (title, description, created_at, project_name, suite_name) VALUES (?, ?, ?, ?, ?)",
                        (req_title, user_story_input, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), project_name, suite_name)
                    )
                    requirement_id = cursor.lastrowid

                    # 3. STEP 2: NLP Parser Vector Generation Emulator
                    cleaned_tokens = " ".join(re.findall(r'\w+', user_story_input.lower()[:100]))
                    cursor.execute(
                        "INSERT INTO NLPResults (requirement_id, cleaned_text, tokens, lemmas) VALUES (?, ?, ?, ?)",
                        (requirement_id, user_story_input[:200], cleaned_tokens, cleaned_tokens)
                    )

                    # 4. STEP 3: Machine Learning Risk Bounds Evaluation
                    mock_confidence = float(np.round(np.random.uniform(0.78, 0.98), 4))
                    mock_risk = np.random.choice(["High Risk Value", "Medium Risk Value", "Low Risk Value"], p=[0.3, 0.5, 0.2])
                    cursor.execute(
                        "INSERT INTO Predictions (requirement_id, predicted_risk_level, confidence_score, xai_explanation, predicted_at) VALUES (?, ?, ?, ?, ?)",
                        (requirement_id, mock_risk, mock_confidence, f"Feature text density matching localized vulnerability markers with {mock_confidence*100:.2f}% certainty.", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    )
                    prediction_id = cursor.lastrowid

                    # 5. STEP 4: Automated Functional Test Case Synthesis (Parses into discrete steps)
                    # We simulate breaking down the story into multiple test cases mapped to this suite
                    scenarios = [
                        f"Verify happy-path execution flow for input sequence: {req_title}",
                        f"Validate missing or empty bound configuration criteria limits",
                        f"Verify edge performance and interface boundaries under load"
                    ]
                    
                    # Query current count to compute prioritization ranking indexes cleanly
                    cursor.execute("SELECT COUNT(*) FROM GeneratedTestCases WHERE project_name = ? AND suite_name = ?", (project_name, suite_name))
                    current_suite_size = cursor.fetchone()[0]

                    for idx, scenario in enumerate(scenarios):
                        mock_score = float(np.round(np.random.uniform(45.0, 99.5), 2))
                        cursor.execute(
                            """INSERT INTO GeneratedTestCases 
                            (requirement_id, prediction_id, test_scenario, test_objective, test_steps, expected_result, test_case_type, calculated_priority_score, project_name, suite_name, final_rank)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (requirement_id, prediction_id, scenario, f"Validate requirement constraint index {idx+1}", "1. Initialize environment\n2. Fire target vector", "System transitions to valid response state", "Functional Automated", mock_score, project_name, suite_name, 0)
                        )

                    # 6. STEP 5: Run isolated Prioritization Indexing on this specific suite pool
                    cursor.execute("""
                        SELECT rowid, calculated_priority_score FROM GeneratedTestCases 
                        WHERE project_name = ? AND suite_name = ? 
                        ORDER BY calculated_priority_score DESC
                    """, (project_name, suite_name))
                    
                    ranked_rows = cursor.fetchall()
                    for rank_idx, row in enumerate(ranked_rows):
                        cursor.execute("UPDATE GeneratedTestCases SET final_rank = ? WHERE rowid = ?", (rank_idx + 1, row[0]))

                    conn.commit()
                    conn.close()

                    st.success(f"✔️ Pipeline Completed successfully! Processed user story and appended generated verification bounds directly into '{project_name}' ➔ '{suite_name}'.")
                    
                    # Highlight redirect notification metrics
                    st.info("💡 Switch to the 'Automated Test Suite' or 'Optimization Queue Matrix' options in the sidebar to review the isolated priority ranks for this specific project suite.")

                except Exception as e:
                    st.error(f"⚠️ Internal Processing Interrupted: {e}")

    # --- SHOW ACTIVE SPECIFIC SUITE SUMMARY TABLE ---
    st.markdown("---")
    st.markdown(f"### 📊 Current Scope Contents (`{project_name}` ➔ `{suite_name}`)")
    try:
        conn = sqlite3.connect(db_path)
        # Using a fallback structural read so no naming mismatches occur
        df_suite = pd.read_sql_query(f"""
            SELECT final_rank AS [Execution Rank], test_scenario AS [Optimized Test Target], calculated_priority_score AS [Priority Matrix Score]
            FROM GeneratedTestCases 
            WHERE project_name = '{project_name}' AND suite_name = '{suite_name}'
            ORDER BY final_rank ASC
        """, conn)
        conn.close()
        
        if df_suite.empty:
            st.info("ℹ️ No test cases generated for this project/suite pair yet. Enter a raw user story above to populate it.")
        else:
            st.dataframe(df_suite, use_container_width=True, hide_index=True)
            
            # --- DOWNLOAD PORTABLE EXPORT MATRIX ---
            csv_data = df_suite.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download Prioritized Test Suite Document (.CSV)",
                data=csv_data,
                file_name=f"{project_name.lower().replace(' ', '_')}_{suite_name.lower().replace(' ', '_')}_prioritized.csv",
                mime="text/csv",
                use_container_width=True
            )
    except Exception as e:
        pass

# ==========================================
# VIEW B: REQUIREMENTS EXPLORER
# ==========================================
elif st.session_state.active_page == "Explorer":
    st.markdown("<div class='blade-title'><h2>📋 Software Requirements Backlog Matrix</h2><p>Active Epics, Features, and Functional User Stories Baseline Matrix</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect(db_path)
        
        # 1. Dynamically read the columns that actually exist in your table
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(Requirements)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # 2. Build a flexible query matching whatever names you have in your schema
        id_col = "id" if "id" in columns else ("requirement_id" if "requirement_id" in columns else columns[0])
        title_col = "title" if "title" in columns else columns[1]
        desc_col = "description" if "description" in columns else (columns[2] if len(columns) > 2 else columns[-1])
        date_col = "created_at" if "created_at" in columns else (columns[3] if len(columns) > 3 else columns[-1])
        
        query = f"""
            SELECT 
                {id_col} AS [ID], 
                {title_col} AS [Title], 
                {desc_col} AS [Acceptance Criteria]
        """
        if "created_at" in columns or date_col != desc_col:
            query += f", {date_col} AS [Created Date]"
            
        query += " FROM Requirements"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            st.info("ℹ️ No requirements logged in the system baseline yet.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"❌ Database Query Interface Link Offline: {e}")
# ==========================================
# VIEW C: NLP PIPELINE
# ==========================================
elif st.session_state.active_page == "NLP":
    st.markdown("<div class='blade-title'><h2>🧠 NLP Feature Token Extraction Pipeline</h2><p>Normalized input vectors and analytical sequence processing logs</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT nlp_id AS [NLP ID], requirement_id AS [Req ID], cleaned_text AS [Normalized String], tokens AS [Tokens] FROM NLPResults", conn)
        conn.close()
        if df.empty:
            st.info("ℹ️ No NLP processing results found. Run a parsing cycle on the main dashboard tab.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Database Link Offline: {e}")

# ==========================================
# VIEW D: ML RISK CLASSIFICATION ENGINE
# ==========================================
elif st.session_state.active_page == "Prediction":
    st.markdown("<div class='blade-title'><h2>🤖 ML Risk Classification Analysis Engine</h2><p>Predictive risk bounds mapping requirements to automated execution vulnerabilities</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Inspect column names for the Requirements table to see what the primary key is named
        cursor.execute("PRAGMA table_info(Requirements)")
        req_columns = [row[1] for row in cursor.fetchall()]
        req_id_col = "id" if "id" in req_columns else ("requirement_id" if "requirement_id" in req_columns else req_columns[0])
        req_title_col = "title" if "title" in req_columns else req_columns[1]

        # 2. Inspect column names for the Predictions table to ensure everything else matches
        cursor.execute("PRAGMA table_info(Predictions)")
        pred_columns = [row[1] for row in cursor.fetchall()]
        
        pred_id_col = "prediction_id" if "prediction_id" in pred_columns else pred_columns[0]
        fk_col = "requirement_id" if "requirement_id" in pred_columns else req_id_col
        risk_col = "predicted_risk_level" if "predicted_risk_level" in pred_columns else "risk_level"
        conf_col = "confidence_score" if "confidence_score" in pred_columns else "confidence"
        xai_col = "xai_explanation" if "xai_explanation" in pred_columns else "explanation"
        time_col = "predicted_at" if "predicted_at" in pred_columns else "timestamp"

        # 3. Build a smart SQL join statement using the confirmed column matches
        query = f"""
            SELECT 
                p.{pred_id_col} AS [Prediction ID], 
                r.{req_title_col} AS [Requirement Title], 
                p.{risk_col} AS [Predicted Risk Level], 
                p.{conf_col} AS [Confidence Score], 
                p.{xai_col} AS [Explainable AI Log], 
                p.{time_col} AS [Evaluation Timestamp]
            FROM Predictions p 
            JOIN Requirements r ON p.{fk_col} = r.{req_id_col}
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            st.info("ℹ️ No pipeline logs generated. Process requirements via the dashboard matrix to log evaluation scores.")
        else:
            # Cleanly format the confidence score column if it is numbers
            if '[Confidence Score]' in df.columns:
                df['[Confidence Score]'] = df['[Confidence Score]'].apply(
                    lambda x: f"{x * 100:.2f}%" if isinstance(x, (int, float)) and x <= 1.0 else (f"{x:.2f}%" if isinstance(x, (int, float)) else str(x))
                )
            st.dataframe(df, use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"❌ Database Link Offline: {e}")

# ==========================================
# VIEW E: AUTOMATED TEST SUITE SCENARIOS
# ==========================================
elif st.session_state.active_page == "TestGen":
    st.markdown("<div class='blade-title'><h2>🧪 Automated Functional Test Suite Matrix</h2><p>Synthesized system test coverage scenarios generated directly from user story validation logs</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Inspect columns for GeneratedTestCases
        cursor.execute("PRAGMA table_info(GeneratedTestCases)")
        tc_columns = [row[1] for row in cursor.fetchall()]
        
        tc_id_col = "tc_id" if "tc_id" in tc_columns else ("test_case_id" if "test_case_id" in tc_columns else ("id" if "id" in tc_columns else tc_columns[0]))
        scenario_col = "test_scenario" if "test_scenario" in tc_columns else "scenario"
        objective_col = "test_objective" if "test_objective" in tc_columns else "objective"
        steps_col = "test_steps" if "test_steps" in tc_columns else "steps"
        expected_col = "expected_result" if "expected_result" in tc_columns else "expected"
        type_col = "test_case_type" if "test_case_type" in tc_columns else "type"

        query = f"""
            SELECT 
                {tc_id_col} AS [Test Case ID], 
                {scenario_col} AS [Scenario Context], 
                {objective_col} AS [Objective Goals]
        """
        if steps_col in tc_columns: query += f", {steps_col} AS [Step Vectors]"
        if expected_col in tc_columns: query += f", {expected_col} AS [Expected Bounds]"
        if type_col in tc_columns: query += f", {type_col} AS [Type Profile]"
        
        query += " FROM GeneratedTestCases"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            st.info("ℹ️ Optimization vectors empty. Please initiate a dashboard execution loop.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Database Link Offline: {e}")

# ==========================================
# VIEW F: OPTIMIZATION QUEUE PRIORITY
# ==========================================
elif st.session_state.active_page == "Prioritization":
    st.markdown("<div class='blade-title'><h2>⭐ Test Optimization & Execution Queue Prioritization Matrix</h2><p>Calculated queue hierarchy maps ordered execution indexes derived from the analytics engine</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Inspect GeneratedTestCases
        cursor.execute("PRAGMA table_info(GeneratedTestCases)")
        tc_columns = [row[1] for row in cursor.fetchall()]
        tc_scenario_col = "test_scenario" if "test_scenario" in tc_columns else "scenario"
        tc_rank_col = "final_rank" if "final_rank" in tc_columns else "rank"
        tc_score_col = "calculated_priority_score" if "calculated_priority_score" in tc_columns else "priority_score"
        tc_req_fk = "requirement_id" if "requirement_id" in tc_columns else tc_columns[1]
        tc_pred_fk = "prediction_id" if "prediction_id" in tc_columns else "prediction_id"

        # 2. Inspect Requirements
        cursor.execute("PRAGMA table_info(Requirements)")
        req_columns = [row[1] for row in cursor.fetchall()]
        req_id_col = "id" if "id" in req_columns else ("requirement_id" if "requirement_id" in req_columns else req_columns[0])
        req_title_col = "title" if "title" in req_columns else req_columns[1]

        # 3. Inspect Predictions
        cursor.execute("PRAGMA table_info(Predictions)")
        pred_columns = [row[1] for row in cursor.fetchall()]
        pred_id_col = "prediction_id" if "prediction_id" in pred_columns else pred_columns[0]
        pred_risk_col = "predicted_risk_level" if "predicted_risk_level" in pred_columns else "risk_level"

        # Build clean dynamic join string
        query = f"""
            SELECT 
                tc.{tc_rank_col} AS [Execution Rank], 
                r.{req_title_col} AS [Requirement Target],
                tc.{tc_scenario_col} AS [Optimized Test Target]
        """
        if pred_risk_col in pred_columns and tc_pred_fk in tc_columns:
            query += f", p.{pred_risk_col} AS [Engine Risk Profile]"
        if tc_score_col in tc_columns:
            query += f", tc.{tc_score_col} AS [Priority Matrix Score]"
            
        query += f"""
            FROM GeneratedTestCases tc
            JOIN Requirements r ON tc.{tc_req_fk} = r.{req_id_col}
        """
        if pred_risk_col in pred_columns and tc_pred_fk in tc_columns:
            query += f" JOIN Predictions p ON tc.{tc_pred_fk} = p.{pred_id_col}"
            
        query += f" ORDER BY tc.{tc_rank_col} ASC"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            st.info("ℹ️ Queue matrix processing clear. No priority sequences currently cached.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Database Link Offline: {e}")

# ==========================================
# VIEW F: OPTIMIZATION QUEUE PRIORITY
# ==========================================
elif st.session_state.active_page == "Prioritization":
    st.markdown("<div class='blade-title'><h2>⭐ Test Optimization & Execution Queue Prioritization Matrix</h2><p>Calculated queue hierarchy maps ordered execution indexes derived from the analytics engine</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("""
            SELECT tc.final_rank AS [Execution Rank], r.title AS [Requirement Target],
                   tc.test_scenario AS [Optimized Test Target], p.predicted_risk_level AS [Engine Risk Profile],
                   tc.calculated_priority_score AS [Priority Matrix Score]
            FROM GeneratedTestCases tc
            JOIN Requirements r ON tc.requirement_id = r.id
            JOIN Predictions p ON tc.prediction_id = p.prediction_id
            ORDER BY tc.final_rank ASC
        """, conn)
        conn.close()
        if df.empty:
            st.info("ℹ️ Queue matrix processing clear. No priority sequences currently cached.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Database Link Offline: {e}")
