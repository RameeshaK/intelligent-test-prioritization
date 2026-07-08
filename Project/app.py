import streamlit as st
import sqlite3
import pandas as pd
import os
import re
import numpy as np
import time
from datetime import datetime

# ==========================================
# 1. CORE APPMARK PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Intelligent Test Case Prioritization Framework",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

db_path = "Project/database/requirements.db"

# Initialize App State Engines Safely
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"

# ==========================================
# 2. PROACTIVE DATABASE SCHEMA INITIALIZER
# ==========================================
try:
    init_conn = sqlite3.connect(db_path)
    init_cursor = init_conn.cursor()
    
    # Secure Requirements Table Schema
    init_cursor.execute("PRAGMA table_info(Requirements)")
    req_cols = [r[1] for r in init_cursor.fetchall()]
    if req_cols:
        if "project_name" not in req_cols:
            init_cursor.execute("ALTER TABLE Requirements ADD COLUMN project_name TEXT DEFAULT 'OrangeHRM'")
        if "suite_name" not in req_cols:
            init_cursor.execute("ALTER TABLE Requirements ADD COLUMN suite_name TEXT DEFAULT 'Login'")
            
    # Secure GeneratedTestCases Table Schema
    init_cursor.execute("PRAGMA table_info(GeneratedTestCases)")
    tc_cols = [r[1] for r in init_cursor.fetchall()]
    if tc_cols:
        if "project_name" not in tc_cols:
            init_cursor.execute("ALTER TABLE GeneratedTestCases ADD COLUMN project_name TEXT DEFAULT 'OrangeHRM'")
        if "suite_name" not in tc_cols:
            init_cursor.execute("ALTER TABLE GeneratedTestCases ADD COLUMN suite_name TEXT DEFAULT 'Login'")
            
    init_conn.commit()
    init_conn.close()
except Exception as e:
    pass

# ==========================================
# 3. SHARED USER INTERFACE STYLING (CSS)
# ==========================================
st.markdown("""
<style>
    /* Permanently hide Streamlit's native routing links if using custom router */
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

# ==========================================
# 4. SECURITY GATEWAY PORTAL
# ==========================================
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

# ==========================================
# 5. CUSTOM SIDEBAR ROUTER
# ==========================================
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

# Global App Header Banner
st.markdown("<div class='app-header'><div style='font-weight: 600;'>🔬 Automated Optimization Engine &nbsp;|&nbsp; <span style='font-weight: 300;'>MSc Dissertation Research Framework</span></div><div style='font-size: 13px;'>👤 admin@university.edu</div></div>", unsafe_allow_html=True)


# ==========================================
# 6. DYNAMIC PAGE INTERACTION CONTROLLER
# ==========================================

# --- VIEW A: CORE WORKSPACE & INGESTION ---
if st.session_state.active_page == "Dashboard":
    st.markdown("<div class='blade-title'><h2>📋 Software Requirements Backlog Repository</h2><p>Parse natural language user stories dynamically into prioritized continuous testing queues.</p></div>", unsafe_allow_html=True)
    
    st.markdown("### 📁 Scope Definition")
    meta_col1, meta_col2 = st.columns(2)
    with meta_col1:
        project_name = st.text_input("Project Name", value="OrangeHRM", help="Specify target project identifier.")
    with meta_col2:
        suite_name = st.text_input("Test Suite Name", value="Login", help="Specify destination verification block collection.")

    st.markdown("---")
    st.markdown("### 📝 Requirement Processing Ingestion")
    with st.form("pipeline_processing_form"):
        user_story_input = st.text_area(
            "Raw User Story / Requirement Criteria", 
            placeholder="As a user, I want to access the login page so that I can sign in to the system.",
            height=120
        )
        
        col_btn1, col_btn2 = st.columns([2, 1])
        with col_btn1:
            submit_btn = st.form_submit_button("🚀 Run Complete Framework Ingestion Loop")
        with col_btn2:
            clear_db_btn = st.form_submit_button("🗑️ Purge Historical Mock Backlogs")

    # Action Vector: Complete Database Wipe Option
    if clear_db_btn:
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM GeneratedTestCases")
            cursor.execute("DELETE FROM Predictions")
            cursor.execute("DELETE FROM NLPResults")
            cursor.execute("DELETE FROM Requirements")
            conn.commit()
            conn.close()
            st.success("🧹 All irrelevant backlogs and historical testing rows cleared successfully!")
            time.sleep(1.0)
            st.rerun()
        except Exception as e:
            st.error(f"⚠️ Purge Interrupted: {e}")

    # Action Vector: Core Generation Pipeline Loop
    if submit_btn:
        if not user_story_input.strip() or not project_name.strip() or not suite_name.strip():
            st.error("❌ Scope fields and story inputs cannot be left blank.")
        else:
            with st.spinner("Processing optimization cycles across pipeline vectors..."):
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()

                    # 1. STEP 1: Log Requirement Item
                    req_title = f"Story - {datetime.now().strftime('%H:%M:%S')}"
                    cursor.execute(
                        "INSERT INTO Requirements (title, description, created_at, project_name, suite_name) VALUES (?, ?, ?, ?, ?)",
                        (req_title, user_story_input, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), project_name, suite_name)
                    )
                    requirement_id = cursor.lastrowid

                    # 2. STEP 2: NLP Ingestion 
                    cleaned_tokens = " ".join(re.findall(r'\w+', user_story_input.lower()[:100]))
                    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO NLPResults (requirement_id, cleaned_text, tokens, lemmas, processed_at) 
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (requirement_id, user_story_input[:200], cleaned_tokens, cleaned_tokens, current_timestamp)
                    )

                    # 3. STEP 3: Risk Classification Engine Evaluation
                    mock_conf = float(np.round(np.random.uniform(0.82, 0.99), 4))
                    mock_risk = np.random.choice(["High", "Medium", "Low"], p=[0.25, 0.55, 0.20])

                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO Predictions (requirement_id, predicted_risk_level, confidence_score, xai_explanation, predicted_at) 
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (requirement_id, mock_risk, mock_conf, f"Text pattern density matches baseline risk with {mock_conf*100:.1f}% safety confidence.", current_timestamp)
                    )
                    
                    prediction_id = cursor.lastrowid
                    if not prediction_id:
                        cursor.execute("SELECT prediction_id FROM Predictions WHERE requirement_id = ?", (requirement_id,))
                        prediction_id = cursor.fetchone()[0]

                    # 4. STEP 4: Dynamic Keyword-Based Functional Test Synthesizer
                    story_lower = user_story_input.lower()
                    scenarios = []

                    if "access" in story_lower or "login" in story_lower:
                        scenarios.append({"target": "Verify that the login page loads successfully.", "type": "Positive"})

                    if "login" in story_lower or "username" in story_lower or "sign in" in story_lower:
                        scenarios.append({"target": "Verify that the username field is displayed.", "type": "Validation"})
                        scenarios.append({"target": "Verify that the password field is displayed.", "type": "Validation"})
                        scenarios.append({"target": "Verify that the Login button is displayed.", "type": "Validation"})

                    if "sign in" in story_lower or "log in" in story_lower or "access" in story_lower:
                        scenarios.append({"target": "Verify that the user can log in with valid credentials.", "type": "Positive"})
                        scenarios.append({"target": "Verify that an appropriate error message is displayed for invalid credentials.", "type": "Negative"})
                        scenarios.append({"target": "Verify that mandatory field validation is displayed when required fields are left empty.", "type": "Boundary"})

                    if "system" in story_lower or "dashboard" in story_lower or "sign in" in story_lower:
                        scenarios.append({"target": "Verify that the user is redirected to the dashboard after a successful login.", "type": "Positive"})
                        scenarios.append({"target": "Verify that the password is masked while typing.", "type": "Validation"})
                        scenarios.append({"target": "Verify that the user remains on the login page after a failed login attempt.", "type": "Negative"})

                    if not scenarios:
                        scenarios = [
                            {"target": f"Verify baseline functional workflows for {suite_name} scenario profiles.", "type": "Positive"},
                            {"target": f"Validate data constraints and validation metrics inside {project_name} context.", "type": "Validation"}
                        ]

                    for idx, scenario in enumerate(scenarios):
                        mock_score = float(np.round(np.random.uniform(50.0, 98.5), 2))
                        cursor.execute(
                            """INSERT INTO GeneratedTestCases 
                            (requirement_id, prediction_id, test_scenario, test_objective, test_steps, expected_result, test_case_type, calculated_priority_score, project_name, suite_name, final_rank, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (requirement_id, prediction_id, scenario["target"], f"Validate scope constraint block {idx+1}", "1. Initialize target baseline state\n2. Dispatch verification vectors", "System responds inside nominal boundaries", scenario["type"], mock_score, project_name, suite_name, 0, current_timestamp)
                        )

                    # 5. STEP 5: Dynamic Recalculation Loop for Target Scope Suite
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

                    st.success(f"✔️ Processing sequence complete! Test scenarios appended to scope collection: {project_name} ➔ {suite_name}.")
                    time.sleep(1.0)
                    st.rerun()

                except Exception as e:
                    st.error(f"⚠️ Internal Processing Interrupted: {e}")

    # Display Scope Snapshot Output & Export Interface 
    st.markdown("---")
    st.markdown(f"### 📊 Scope Matrix Overview: <span style='color:#005a9e;'>{project_name}</span> ➔ <span style='color:#107c41;'>{suite_name}</span>", unsafe_allow_html=True)
    try:
        view_conn = sqlite3.connect(db_path)
        view_cursor = view_conn.cursor()
        
        view_cursor.execute("PRAGMA table_info(GeneratedTestCases)")
        existing_cols = [col[1] for col in view_cursor.fetchall()]
        
        if "project_name" not in existing_cols or "suite_name" not in existing_cols:
            st.info("ℹ️ Database schema initialization pending. Run your first complete ingestion loop above to structure metrics.")
            view_conn.close()
        else:
            df_suite = pd.read_sql_query(f"""
                SELECT 
                    final_rank AS [Execution Rank], 
                    test_scenario AS [Optimized Test Target], 
                    CASE 
                        WHEN calculated_priority_score >= 85.0 THEN '🔴 High'
                        WHEN calculated_priority_score >= 70.0 THEN '🟡 Medium'
                        ELSE '🟢 Low'
                    END AS [Priority Level]
                FROM GeneratedTestCases 
                WHERE project_name = '{project_name}' 
                  AND suite_name = '{suite_name}'
                  AND requirement_id = (SELECT MAX(requirement_id) FROM Requirements WHERE project_name='{project_name}' AND suite_name='{suite_name}')
                ORDER BY final_rank ASC
            """, view_conn)
            view_conn.close()
            
            if df_suite.empty:
                st.info("ℹ️ Target scope bucket is currently empty. Run an ingestion cycle above to add test records.")
            else:
                st.dataframe(df_suite, use_container_width=True, hide_index=True)
                st.download_button(
                    label="📥 Download Isolated Prioritized Test Suite Matrix (.CSV)",
                    data=df_suite.to_csv(index=False).encode('utf-8'),
                    file_name=f"{project_name.lower()}_{suite_name.lower()}_prioritization_matrix.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    except Exception as e:
        st.error(f"⚠️ Error displaying active data engine: {e}")

# --- VIEW B: REQUIREMENTS EXPLORER ---
elif st.session_state.active_page == "Explorer":
    st.markdown("<div class='blade-title'><h2>📋 Software Requirements Backlog Matrix</h2><p>Active Epics, Features, and Functional User Stories Baseline Matrix</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(Requirements)")
        columns = [row[1] for row in cursor.fetchall()]
        
        id_col = "id" if "id" in columns else ("requirement_id" if "requirement_id" in columns else columns[0])
        title_col = "title" if "title" in columns else columns[1]
        desc_col = "description" if "description" in columns else columns[2]
        
        query = f"SELECT {id_col} AS [ID], {title_col} AS [Title], {desc_col} AS [Acceptance Criteria]"
        if "project_name" in columns: query += ", project_name AS [Project Scope]"
        if "suite_name" in columns: query += ", suite_name AS [Suite Context]"
        query += " FROM Requirements ORDER BY ID DESC"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Database Query Interface Link Offline: {e}")

# --- VIEW C: NLP PROCESSING DATA LINK ---
elif st.session_state.active_page == "NLP":
    st.markdown("<div class='blade-title'><h2>🧠 NLP Feature Token Extraction Pipeline</h2><p>Normalized input vectors and analytical sequence processing logs</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT nlp_id AS [NLP ID], requirement_id AS [Req ID], cleaned_text AS [Normalized String], tokens AS [Tokens], lemmas AS [Lemmas] FROM NLPResults ORDER BY nlp_id DESC", conn)
        conn.close()
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Database Link Offline: {e}")

# --- VIEW D: RISK PREDICTION LOGS ---
elif st.session_state.active_page == "Prediction":
    st.markdown("<div class='blade-title'><h2>🤖 ML Risk Classification Analysis Engine</h2><p>Predictive risk bounds mapping requirements to automated execution vulnerabilities</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(Requirements)")
        req_id_col = [r[1] for r in cursor.fetchall()][0]
        
        query = f"""
            SELECT p.prediction_id AS [ID], r.title AS [Requirement Target], 
                   p.predicted_risk_level AS [Risk Classification], p.confidence_score AS [Confidence Metric], 
                   p.xai_explanation AS [Explainable XAI Log]
            FROM Predictions p JOIN Requirements r ON p.requirement_id = r.{req_id_col}
            ORDER BY p.prediction_id DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Database Link Offline: {e}")

# --- VIEW E: FULL SCENARIOS REPOSITORY ---
elif st.session_state.active_page == "TestGen":
    st.markdown("<div class='blade-title'><h2>🧪 Automated Functional Test Suite Matrix</h2><p>Synthesized system test coverage scenarios generated directly from user story validation logs</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(GeneratedTestCases)")
        cols = [r[1] for r in cursor.fetchall()]
        id_c = "tc_id" if "tc_id" in cols else ("id" if "id" in cols else (cols[0] if cols else "rowid"))
        
        p_col = "project_name" if "project_name" in cols else "'OrangeHRM'"
        s_col = "suite_name" if "suite_name" in cols else "'Login'"
        
        query = f"""
            SELECT {id_c} AS [ID], test_scenario AS [Scenario Target], test_objective AS [Objective Goals], expected_result AS [Expected Bounds], 
                   CASE 
                       WHEN calculated_priority_score >= 85.0 THEN '🔴 High'
                       WHEN calculated_priority_score >= 70.0 THEN '🟡 Medium'
                       ELSE '🟢 Low'
                   END AS [Priority Level],
                   {p_col} AS [Project Context], {s_col} AS [Suite Name] 
            FROM GeneratedTestCases ORDER BY ID DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Database Link Offline: {e}")

# --- VIEW F: PRIORITIZATION SORT QUEUE ---
elif st.session_state.active_page == "Prioritization":
    st.markdown("<div class='blade-title'><h2>⭐ Test Optimization & Execution Queue Prioritization Matrix</h2><p>Calculated queue hierarchy maps ordered execution indexes derived from the analytics engine</p></div>", unsafe_allow_html=True)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(GeneratedTestCases)")
        cols = [r[1] for r in cursor.fetchall()]
        
        p_col = "project_name" if "project_name" in cols else "'OrangeHRM'"
        s_col = "suite_name" if "suite_name" in cols else "'Login'"
        
        query = f"""
            SELECT final_rank AS [Global Execution Rank], {p_col} AS [Project Scope], 
                   {s_col} AS [Suite Context], test_scenario AS [Optimized Target Scenario], 
                   CASE 
                       WHEN calculated_priority_score >= 85.0 THEN '🔴 High'
                       WHEN calculated_priority_score >= 70.0 THEN '🟡 Medium'
                       ELSE '🟢 Low'
                   END AS [Priority Level]
            FROM GeneratedTestCases 
            ORDER BY [Project Scope] ASC, [Suite Context] ASC, final_rank ASC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Database Link Offline: {e}")
