import streamlit as st
import sqlite3
import pandas as pd
import os
import re
import joblib
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="MSc Prioritization Framework Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- REUSABLE DATABASE & ASSET PATH LOCATOR ---
db_path = "Project/database/requirements.db"
models_dir = "Project/models"

st.title("🏠 Intelligent Test Case Prioritization Framework")
st.markdown("This interactive portal executes natural language parsing, predictive risk indexing, and optimized test case generation workflows in real-time.")

st.markdown("---")

# --- SECTION 1: USER INPUT INTERFACE ---
st.subheader("➕ Add New Software Requirement")
st.markdown("Input a raw human-language requirement below to route it through the machine learning pipeline.")

with st.form("requirement_form", clear_on_submit=True):
    col_t, col_d = st.columns([1, 2])
    with col_t:
        new_title = st.text_input("Requirement Title", placeholder="e.g., Enable FaceID Login")
    with col_d:
        new_desc = st.text_area("Requirement Description", placeholder="e.g., The system must allow users to authenticate using biometric face scanning parameters securely.")
    
    submit_button = st.form_submit_button("⚡ Run Pipeline & Analyze Requirement")

if submit_button:
    if not new_title.strip() or not new_desc.strip():
        st.error("⚠️ Both Title and Description fields are strictly required.")
    else:
        try:
            # 1. Load trained machine learning assets
            rf_model = joblib.load(os.path.join(models_dir, "random_forest_model.pkl"))
            vectorizer = joblib.load(os.path.join(models_dir, "tfidf_vectorizer.pkl"))
            label_mapping = joblib.load(os.path.join(models_dir, "label_encoder.pkl"))
            inv_label_mapping = {v: k for k, v in label_mapping.items()}
            
            # 2. Live NLP Text Cleaning (Matching Phase 3)
            combined_text = f"{new_title} {new_desc}".lower()
            cleaned_text = re.sub(r'[^a-zA-Z\s]', '', combined_text)
            
            # 3. Model Inference & XAI Processing
            tfidf_vector = vectorizer.transform([cleaned_text])
            dense_vector = tfidf_vector.toarray()[0]
            
            pred_idx = rf_model.predict(tfidf_vector)[0]
            probabilities = rf_model.predict_proba(tfidf_vector)[0]
            
            predicted_label = inv_label_mapping[pred_idx]
            confidence_score = probabilities[pred_idx]
            
            # Extract top active word drivers
            feature_names = vectorizer.get_feature_names_out()
            importances = rf_model.feature_importances_
            active_indices = np.where(dense_vector > 0)[0]
            word_contributions = sorted(
                [(feature_names[i], importances[i]) for i in active_indices],
                key=lambda x: x[1], reverse=True
            )[:3]
            explanation_str = ", ".join([f"'{w}' ({wt:.2f})" for w, wt in word_contributions])
            if not explanation_str:
                explanation_str = "General vocabulary features applied."

            # 4. Save Directly to Relational Database Tables
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Insert into Requirements
            cursor.execute("INSERT INTO Requirements (title, description, created_at) VALUES (?, ?, ?)", 
                           (new_title.strip(), new_desc.strip(), timestamp))
            req_id = cursor.lastrowid
            
            # Insert into NLPResults
            tokens = cleaned_text.split()
            cursor.execute("INSERT INTO NLPResults (requirement_id, cleaned_text, tokens, lemmas, processed_at) VALUES (?, ?, ?, ?, ?)",
                           (req_id, cleaned_text, str(tokens), str(tokens), timestamp))
            
            # Insert into Predictions
            cursor.execute("INSERT INTO Predictions (requirement_id, predicted_risk_level, confidence_score, xai_explanation, predicted_at) VALUES (?, ?, ?, ?, ?)",
                           (req_id, predicted_label, float(confidence_score), f"Top Keywords: {explanation_str}", timestamp))
            
            # 5. Rule-Based Test Case Assignment Engine (Phase 6 Replication)
            pred_id = cursor.lastrowid
            if "auth" in combined_text or "login" in combined_text or "biometric" in combined_text:
                scenarios = [
                    ("Verify Successful Biometric Auth Processing", "Positive", "Ensure credentials validate completely.", 2.60),
                    ("Block Malformed or Mismatched Token Access Requests", "Negative", "Prevent unauthorized system entry configurations.", 2.60)
                ]
            else:
                scenarios = [
                    ("Verify Functional Requirement Feature UI Behaviors", "Positive", "Confirm components adhere to layout specs.", 2.00)
                ]
                
            for scen, ttype, obj, p_score in scenarios:
                cursor.execute("""
                    INSERT INTO GeneratedTestCases (requirement_id, prediction_id, test_scenario, test_objective, preconditions, test_steps, expected_result, test_case_type, calculated_priority_score, final_rank, created_at)
                    VALUES (?, ?, ?, ?, 'System fully functional', '1. Trigger input interface.\\n2. Submit data parameters.', 'Success validation.', ?, ?, 99, ?)
                """, (req_id, pred_id, scen, obj, ttype, p_score, timestamp))
            
            # Re-rank execution ranks globally (Phase 7 Replication)
            cursor.execute("""
                UPDATE GeneratedTestCases 
                SET final_rank = (
                    SELECT COUNT(*) + 1 FROM GeneratedTestCases g2 
                    WHERE g2.calculated_priority_score > GeneratedTestCases.calculated_priority_score
                )
            """)
            
            conn.commit()
            conn.close()
            
            st.balloons()
            st.success(f"🎉 Pipeline completed for Requirement #{req_id}! Classified as **{predicted_label} Risk** ({confidence_score*100:.1f}% Confidence).")
            
        except Exception as e:
            st.error(f"Execution Error: {e}")

st.markdown("---")

# --- SECTION 2: SYSTEM SUMMARY METRICS ---
st.subheader("📊 System-Wide Statistics")

def load_dashboard_metrics():
    try:
        conn = sqlite3.connect(db_path)
        req_count = pd.read_sql_query("SELECT COUNT(*) as total FROM Requirements", conn)['total'].iloc[0]
        pred_count = pd.read_sql_query("SELECT COUNT(*) as total FROM Predictions", conn)['total'].iloc[0]
        tc_count = pd.read_sql_query("SELECT COUNT(*) as total FROM GeneratedTestCases", conn)['total'].iloc[0]
        risk_df = pd.read_sql_query("SELECT predicted_risk_level, COUNT(*) as count FROM Predictions GROUP BY predicted_risk_level", conn)
        conn.close()
        return req_count, pred_count, tc_count, risk_df
    except Exception:
        return 0, 0, 0, pd.DataFrame()

req_count, pred_count, tc_count, risk_df = load_dashboard_metrics()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Requirements Logged", value=req_count)
with col2:
    st.metric(label="ML Predictions Processed", value=pred_count)
with col3:
    st.metric(label="Automated Test Cases Compiled", value=tc_count)

if not risk_df.empty:
    st.markdown("### Current Risk Classifications Summary Balance")
    st.dataframe(risk_df, use_container_width=True, hide_index=True)
