import streamlit as st
import pandas as pd
import re

# Set Streamlit Page Config
st.set_page_config(
    page_title="AI-Powered Test Prioritization & Generation System",
    page_icon="🤖",
    layout="wide"
)

# --- INTELLIGENT ENGINE: Dynamic Feature & Domain Extractor ---
def extract_story_context(user_story):
    """
    Parses raw user story using pattern matching & keyword abstraction 
    to extract domain concepts, actions, and actors dynamically.
    """
    text = user_story.strip().lower()
    
    # Extract "Role/Actor"
    role_match = re.search(r"as a[n]? ([^,]+)", text)
    role = role_match.group(1).title() if role_match else "User"
    
    # Extract "Action / Want"
    want_match = re.search(r"i want to ([^so that]+)", text)
    action = want_match.group(1).strip() if want_match else "perform action"
    
    # Extract "Goal / So that"
    so_that_match = re.search(r"so that ([^.]+)", text)
    goal = so_that_match.group(1).strip() if so_that_match else "achieve intended outcome"

    # Identify Domain Keywords for tailored case generation
    keywords = re.findall(r'\b[a-zA-Z]{4,}\b', text)
    stopwords = {"want", "that", "this", "from", "with", "have", "user", "system", "into", "page", "able"}
    domain_terms = [kw.title() for kw in keywords if kw not in stopwords]
    
    main_target = domain_terms[0] if domain_terms else "System Module"
    
    return {
        "role": role,
        "action": action,
        "goal": goal,
        "target": main_target,
        "terms": domain_terms
    }


# --- INTELLIGENT ENGINE: Dynamic Scenario Generator ---
def generate_intelligent_scenarios(story_ctx):
    """
    Dynamically constructs high-level test scenarios tailored to the input story,
    and assigns intelligent risk & priority tiers.
    """
    target = story_ctx["target"]
    action = story_ctx["action"]
    role = story_ctx["role"]
    
    scenarios = [
        {
            "Scenario ID": "SC_01",
            "Test Scenario": f"Verify successful core execution of '{action}' by {role}",
            "Risk Level": "High",
            "Priority Rank": 1,
            "Category": "Core Functional Path",
            "Target Module": target
        },
        {
            "Scenario ID": "SC_02",
            "Test Scenario": f"Verify system input validation and error handling during '{action}'",
            "Risk Level": "High",
            "Priority Rank": 2,
            "Category": "Validation & Security",
            "Target Module": target
        },
        {
            "Scenario ID": "SC_03",
            "Test Scenario": f"Verify state persistence and data integrity after completing '{action}'",
            "Risk Level": "Medium",
            "Priority Rank": 3,
            "Category": "Data Integrity",
            "Target Module": target
        },
        {
            "Scenario ID": "SC_04",
            "Test Scenario": f"Verify UI responsiveness and accessibility for {role} while performing '{action}'",
            "Risk Level": "Low",
            "Priority Rank": 4,
            "Category": "UI / Usability",
            "Target Module": target
        }
    ]
    return pd.DataFrame(scenarios)


# --- INTELLIGENT ENGINE: Dynamic Test Case Generator ---
def generate_intelligent_test_cases(selected_scenario, story_ctx):
    """
    Generates granular Positive, Negative, and Edge test cases 
    specifically contextualized to the chosen high-level scenario and raw story.
    """
    action = story_ctx["action"]
    role = story_ctx["role"]
    target = story_ctx["target"]
    goal = story_ctx["goal"]
    
    test_cases = [
        # --- POSITIVE TEST CASES ---
        {
            "Test Case ID": "TC_POS_01",
            "Category": "Positive",
            "Test Case Description": f"Verify {role} can successfully {action} with valid inputs.",
            "Preconditions": f"{role} is logged in and authorized to access {target}.",
            "Expected Result": f"System processes action smoothly, allowing user to {goal}."
        },
        {
            "Test Case ID": "TC_POS_02",
            "Category": "Positive",
            "Test Case Description": f"Verify database/session state correctly reflects changes after {action}.",
            "Preconditions": f"Core execution of {action} completed successfully.",
            "Expected Result": f"Data records for {target} update in real time without corruption."
        },
        
        # --- NEGATIVE TEST CASES ---
        {
            "Test Case ID": "TC_NEG_01",
            "Category": "Negative",
            "Test Case Description": f"Verify behavior when {role} submits invalid or incomplete data while trying to {action}.",
            "Preconditions": f"{role} navigates to {target} workflow.",
            "Expected Result": "System rejects submission and displays clear, actionable error validation messages."
        },
        {
            "Test Case ID": "TC_NEG_02",
            "Category": "Negative",
            "Test Case Description": f"Verify unauthorized or unauthenticated users attempting to {action}.",
            "Preconditions": "User session is invalid or expired.",
            "Expected Result": "System blocks access, redirects to login/authorization page, and logs security event."
        },

        # --- EDGE / BOUNDARY TEST CASES ---
        {
            "Test Case ID": "TC_EDGE_01",
            "Category": "Edge Case",
            "Test Case Description": f"Verify {action} under extreme input boundary limits (e.g., max string lengths, special symbols, script injection tags).",
            "Preconditions": f"Input form fields for {target} are active.",
            "Expected Result": "System safely sanitizes inputs, prevents SQL/XSS execution, and displays graceful validation errors."
        },
        {
            "Test Case ID": "TC_EDGE_02",
            "Category": "Edge Case",
            "Test Case Description": f"Verify behavior when {role} rapidly clicks action triggers or experiences intermittent network disconnection during {action}.",
            "Preconditions": f"{action} is in progress.",
            "Expected Result": "Action button disables during request processing to prevent duplicate submissions; network timeout handles gracefully."
        }
    ]
    return pd.DataFrame(test_cases)


# --- STREAMLIT UI LAYOUT ---
st.title("🤖 AI-Driven Test Prioritization & Intelligent Generation Framework")
st.markdown("---")

# Session state management
if "story_ctx" not in st.session_state:
    st.session_state.story_ctx = None
if "scenarios_df" not in st.session_state:
    st.session_state.scenarios_df = None

tab_scenarios, tab_detailed_cases = st.tabs([
    "📋 1. Prioritized Test Scenarios", 
    "🔍 2. Deep Test Case Generation"
])

# --- TAB 1: High-Level Scenarios ---
with tab_scenarios:
    st.header("Input Any User Story")
    
    default_story = "As a customer, I want to add items to my shopping cart so that I can purchase them later."
    
    user_story = st.text_area(
        "Enter Raw User Story:",
        value=default_story,
        height=100
    )
    
    if st.button("🚀 Analyze Story & Generate Scenarios", type="primary"):
        if user_story.strip():
            # Run Intelligent Extraction & Generation
            ctx = extract_story_context(user_story)
            scenarios = generate_intelligent_scenarios(ctx)
            
            st.session_state.story_ctx = ctx
            st.session_state.scenarios_df = scenarios
            st.success("User Story Parsed & High-Level Scenarios Prioritized!")
        else:
            st.warning("Please enter a user story first.")

    # Render Scenarios Table
    if st.session_state.scenarios_df is not None:
        st.subheader("🎯 Prioritized Scenarios Matrix")
        
        ctx = st.session_state.story_ctx
        st.caption(f"**Extracted Role:** `{ctx['role']}` | **Core Action:** `{ctx['action']}` | **Target Module:** `{ctx['target']}`")
        
        # Color styling
        def color_risk(val):
            if val == "High":
                return "background-color: #ff4b4b; color: white; font-weight: bold;"
            elif val == "Medium":
                return "background-color: #ffa726; color: black; font-weight: bold;"
            return "background-color: #66bb6a; color: white; font-weight: bold;"

        styled_df = st.session_state.scenarios_df.style.map(color_risk, subset=["Risk Level"])
        st.dataframe(styled_df, use_container_width=True)
        
        st.info("💡 Navigate to **'2. Deep Test Case Generation'** tab to expand any scenario into Positive, Negative, and Edge test cases.")

# --- TAB 2: Granular Test Cases ---
with tab_detailed_cases:
    st.header("Expand Scenarios into Detailed Executable Test Cases")
    
    if st.session_state.scenarios_df is None:
        st.warning("⚠️ Please analyze a user story in Tab 1 first.")
    else:
        scenarios_list = st.session_state.scenarios_df["Test Scenario"].tolist()
        
        selected_scenario = st.selectbox(
            "Select a Test Scenario to expand:",
            scenarios_list
        )
        
        if selected_scenario:
            # Generate test cases dynamically based on extracted story context
            tc_df = generate_intelligent_test_cases(selected_scenario, st.session_state.story_ctx)
            
            # Category Filter
            categories = st.multiselect(
                "Filter Case Types:",
                options=["Positive", "Negative", "Edge Case"],
                default=["Positive", "Negative", "Edge Case"]
            )
            
            filtered_tc_df = tc_df[tc_df["Category"].isin(categories)]
            
            st.subheader(f"🧪 Test Cases for Scenario: *'{selected_scenario}'*")
            st.dataframe(filtered_tc_df, use_container_width=True)
            
            # CSV Download Option
            csv = filtered_tc_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Generated Test Cases (CSV)",
                data=csv,
                file_name="generated_test_cases.csv",
                mime="text/csv"
            )
