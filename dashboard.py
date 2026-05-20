import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os
from dotenv import load_dotenv

# REMOVED: import sqlite3
# REMOVED: CUSTOM_THRESHOLD logic. The backend makes the decisions now!

load_dotenv()
st.set_page_config(page_title="FraudOps Dashboard", page_icon="🛡️", layout="wide")

API_URL = os.getenv("API_URL", "http://localhost:8000")

def load_data():
    """Fetches logs safely over the internet from the FastAPI backend."""
    try:
        # THE FIX: Ask the API for the logs instead of looking for a local file
        response = requests.get(f"{API_URL}/logs")
        if response.status_code == 200:
            logs = response.json().get("logs", [])
            if logs:
                df = pd.DataFrame(logs)
                # Standardize backend terms (APPROVED/DECLINED) to UI colors (SAFE/ALERT)
                if 'status' in df.columns:
                    df['status'] = df['status'].replace({"APPROVED": "SAFE", "DECLINED": "ALERT"})
                return df
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame() 

# --- FRONTEND UI (MAIN PAGE) ---
st.title("🛡️ Fraud Detection Command Center")
st.markdown("Live monitoring dashboard for the XGBoost Fraud Detection API.")

df = load_data()

# --- TOP ROW: KPI METRICS ---
if not df.empty:
    col1, col2, col3 = st.columns(3)
    total_transactions = len(df)
    fraud_caught = len(df[df["status"] == "ALERT"])
    fraud_rate = (fraud_caught / total_transactions) * 100 if total_transactions > 0 else 0

    col1.metric("Total Transactions Logged", total_transactions)
    col2.metric("Alerts", fraud_caught)
    col3.metric("Current Alert Rate", f"{fraud_rate:.2f}%")
else:
    st.info("The database is currently empty or loading. Send a test transaction using the sidebar!")

st.divider()

# --- MIDDLE ROW: CHARTS & DATA ---
col_chart, col_data = st.columns([1, 1])

with col_chart:
    st.subheader("Transaction Status Distribution")
    if not df.empty:
        fig = px.pie(df, names="status", hole=0.4, color="status",
                     color_discrete_map={"SAFE": "#00CC96", "ALERT": "#EF553B"})
        st.plotly_chart(fig, use_container_width=True)

with col_data:
    st.subheader("Recent Audit Logs")
    if not df.empty:
        st.dataframe(df.sort_values(by="id", ascending=False).head(10), use_container_width=True)
# --- SIDEBAR: CONTROLS ---
st.sidebar.title("⚙️ Control Panel")
st.sidebar.markdown("### 📁 Batch Processing")
st.sidebar.markdown("Upload a transaction CSV containing full PCA features (V1-V28), Amount, and Transaction_Hour.")

uploaded_file = st.sidebar.file_uploader("Upload Transaction CSV", type=["csv"])

if uploaded_file is not None:
    batch_df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"Loaded {len(batch_df)} transactions!")
    
    if st.sidebar.button("Run Batch Scan"):
        with st.spinner("Scanning batch for fraud..."):
            results = []
            for index, row in batch_df.iterrows():
                payload = row.to_dict() 
                try:
                    response = requests.post(f"{API_URL}/predict", json=payload)
                    if response.status_code == 200:
                        res_data = response.json()
                        display_status = "ALERT" if res_data["status"] == "DECLINED" else "SAFE"
                        
                        results.append({
                            "ID": index,
                            "Amount": payload.get("Amount", 0),
                            "Status": display_status,
                            "Confidence": res_data["probability_score"]
                        })
                except Exception as e:
                    st.sidebar.error(f"API connection failed on row {index}.")
                    break
            
            st.session_state['batch_results'] = pd.DataFrame(results)
            st.rerun()

# --- BOTTOM ROW: BATCH RESULTS ---
if 'batch_results' in st.session_state and not st.session_state['batch_results'].empty:
    st.divider()
    st.subheader("📁 Latest Batch Scan Results")
    
    results_df = st.session_state['batch_results']
    
    def highlight_alerts(val):
        color = '#ffcccc' if val == 'ALERT' else 'transparent'
        return f'background-color: {color}'
        
    st.dataframe(results_df.style.map(highlight_alerts, subset=['Status']), use_container_width=True)
    
    frauds_found = len(results_df[results_df['Status'] == 'ALERT'])
    st.warning(f"Batch Complete: Found {frauds_found} suspicious transactions.")