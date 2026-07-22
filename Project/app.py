import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# Set Streamlit Page Config
st.set_page_config(
    page_title="AI Test Case Prioritization Framework",
    page_icon="🧪",
    layout="wide"
)

# --- Helper Function: Generate Detailed Test Cases from Scenarios ---
def derive_detailed_test_cases(scenario_name, target_feature):
    """
    Acts as a Senior QA Engineer rule engine to expand a high-level scenario
    into Positive, Negative, and Edge Case test cases.
    """
    feature = target_feature.strip() if target_feature else "feature"
    
    test_cases = [
        # Positive Cases
        {
            "Test Case ID": "TC_POS_01",
            "Category": "Positive",
            "Test Case Description": f"Verify {scenario_name} with valid inputs and normal user workflow.",
            "Expected Result": f"System successfully processes the request and displays expected success confirmation for {feature}."
        },
        {
            "Test Case ID": "TC_POS_02",
            "Category": "Positive",
            "Test Case Description": f"Verify state persistence after successful execution of {scenario_name}.",
            "Expected Result": "System state updates correctly and session/database updates are properly saved."
        },
        
        # Negative Cases
        {
            "Test Case ID": "TC_NEG_01",
            "Category": "Negative",
            "Test Case Description": f"Verify {scenario_name} with invalid/incorrect credentials or payload.",
            "Expected Result": "System rejects the request and displays a clear, user-friendly error message."
        },
        {
            "Test Case ID": "TC_NEG_02",
            "Category": "Negative",
            "Test Case Description": f"Verify {scenario_name} execution without required/mandatory fields.",
            "Expected Result": "Validation error triggers, highlighting missing fields before submission."
        },
        
        # Edge Cases
        {
            "Test Case ID": "TC_EDGE_01",
            "Category": "Edge Case",
            "Test Case Description": f"Verify {scenario_name} with maximum character boundary limits and special characters (@, #, $, <script>).",
            "Expected Result": "System safely sanitizes inputs without crashing, throwing unhandled exceptions, or rendering raw scripts."
        },
        {
            "Test Case ID": "TC_EDGE_02",
            "Category": "Edge Case",
            "Test Case Description": f"Verify behavior of {scenario_name} during rapid repeated clicks or weak/intermittent network connection.",
            "Expected Result": "Button disables after initial click to prevent duplicate submissions; handles network timeouts gracefully."
        }
    ]
    return pd.DataFrame(test_cases)


# --- UI Interface ---
st.title("🧪 Intelligent Test Prioritization & Scenario Derivation System")
st.markdown("---")

# Navigation Tabs
tab_scenarios, tab_detailed_cases = st.tabs([
    "📋 High-Level Test Scenarios (Prioritized)", 
    "🔍 Detailed Test Case Breakdown (Positive / Negative / Edge)"
])

# Initialize Session State
if "scenarios_df" not in st.session_state:
    st.session_state.scenarios_df = None
if "user_story_text" not in st.session_state:
    st.session_state.user_story_text = ""

# --- TAB 1: High-Level Scenarios & Prioritization ---
with tab_scenarios:
    st.header("1. Input Raw User Story")
    
    user_story = st.text_area(
        "Enter User Story / Requirement:",
        height=120,
        placeholder="As a registered user, I want to log in using my email and password so that I can access my dashboard."
    )
    
    if st.button("🚀 Process & Prioritize Test Scenarios", type="primary"):
        if user_story.strip():
            st.session_state.user_story_text = user_story
            
            # Simulated NLP / ML Risk Classification Logic
            # (Replace with your loaded pickle model predictions as needed)
            scenarios_data = [
                {
                    "Scenario ID": "SC_01",
                    "Test Scenario": "Verify User Authentication with Credentials",
                    "Risk Level": "High",
                    "Priority Rank": 1,
                    "Target Feature": "Login Engine"
                },
                {
                    "Scenario ID": "SC_02",
                    "Test Scenario": "Verify Session Timeout & Security Boundaries",
                    "Risk Level": "High",
                    "Priority Rank": 2,
                    "Target Feature": "Session Management"
                },
                {
                    "Scenario ID": "SC_03",
                    "Test Scenario": "Verify Dashboard UI Loading & Elements Display",
                    "Risk Level": "Medium",
                    "Priority Rank": 3,
                    "Target Feature": "User Dashboard"
                },
                {
                    "Scenario ID": "SC_04",
                    "Test Scenario": "Verify Remember Me Functionality",
                    "Risk Level": "Low",
                    "Priority Rank": 4,
                    "Target Feature": "Cookie Storage"
                }
            ]
            
            st.session_state.scenarios_df = pd.DataFrame(scenarios_data)
            st.success("Test Scenarios Prioritized Successfully!")
        else:
            st.warning("Please enter a valid user story.")

    # Display Scenarios Table
    if st.session_state.scenarios_df is not None:
        st.subheader("🎯 Prioritized Test Scenarios Matrix")
        
        # Color formatting helper
        def color_risk(val):
            if val == "High":
                return "background-color: #ff4b4b; color: white; font-weight: bold;"
            elif val == "Medium":
                return "background-color: #ffa726; color: black; font-weight: bold;"
            return "background-color: #66bb6a; color: white; font-weight: bold;"

        styled_df = st.session_state.scenarios_df.style.map(color_risk, subset=["Risk Level"])
        st.dataframe(styled_df, use_container_width=True)
        
        st.info("💡 Switch to the **'Detailed Test Case Breakdown'** tab to generate positive, negative, and edge-case test cases for these scenarios.")

# --- TAB 2: Detailed Test Case Breakdown ---
with tab_detailed_cases:
    st.header("2. Derive Detailed Test Cases from Scenarios")
    
    if st.session_state.scenarios_df is None:
        st.info(" Please generate test scenarios in Tab 1 first.")
    else:
        scenarios_list = st.session_state.scenarios_df["Test Scenario"].tolist()
        
        selected_scenario = st.selectbox(
            "Select a High-Level Test Scenario to expand:",
            scenarios_list
        )
        
        if selected_scenario:
            # Fetch target feature for the selected scenario
            row = st.session_state.scenarios_df[
                st.session_state.scenarios_df["Test Scenario"] == selected_scenario
            ].iloc[0]
            
            target_feature = row["Target Feature"]
            risk_tier = row["Risk Level"]
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Selected Scenario Risk Tier", value=risk_tier)
            with col2:
                st.metric(label="Target Component/Feature", value=target_feature)
            
            st.markdown("### 🧪 Generated Test Cases (Positive, Negative & Edge)")
            
            # Derive test cases
            test_cases_df = derive_detailed_test_cases(selected_scenario, target_feature)
            
            # Filter options by Category
            category_filter = st.multiselect(
                "Filter Test Cases by Category:",
                options=["Positive", "Negative", "Edge Case"],
                default=["Positive", "Negative", "Edge Case"]
            )
            
            filtered_df = test_cases_df[test_cases_df["Category"].isin(category_filter)]
            
            st.dataframe(filtered_df, use_container_width=True)
            
            # Download Option
            csv_data = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Derived Test Cases (CSV)",
                data=csv_data,
                file_name=f"{selected_scenario.replace(' ', '_')}_test_cases.csv",
                mime="text/csv"
            )
