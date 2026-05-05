import streamlit as st
import sqlite3
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="FraudOps Dashboard", page_icon="🛡️", layout="wide")

API_URL = "http://127.0.0.1:8000/predict"

# 1. We declare our strict threshold globally so the whole app uses it!
CUSTOM_THRESHOLD = 0.005 

def load_data():
    """Loads logs and forces the Database to respect our strict UI threshold!"""
    try:
        conn = sqlite3.connect("fraud_logs.db")
        df = pd.read_sql_query("SELECT * FROM transactions", conn)
        conn.close()
        
        if not df.empty:
            # If the DB logged the probability score, we recalculate the status right here!
            if 'probability_score' in df.columns:
                df['status'] = df['probability_score'].apply(
                    lambda x: "ALERT" if float(x) > CUSTOM_THRESHOLD else "SAFE"
                )
            # Fallback just in case
            elif 'status' in df.columns:
                df['status'] = df['status'].replace({"APPROVED": "SAFE", "DECLINED": "ALERT"})
                
        return df
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
    st.info("The database is currently empty. Send a test transaction using the sidebar!")

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
tab_single, tab_batch = st.sidebar.tabs(["💳 Single Swipe", "📁 Batch Scan"])

# --- TAB 1: SINGLE TRANSACTION ---
with tab_single:
    st.markdown("Simulate a single transaction.")
    with st.form("swipe_form"):
        test_amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=150.0)
        test_hour = st.slider("Transaction Hour (0-23)", 0, 23, 14)
        submit_button = st.form_submit_button(label="Swipe Card")

    if submit_button:
        payload = {f"V{i}": 0.0 for i in range(1, 29)}
        payload["Amount"] = test_amount
        payload["Transaction_Hour"] = test_hour
        
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    # Apply our strict UI threshold
                    display_status = "ALERT" if result["probability_score"] > CUSTOM_THRESHOLD else "SAFE"
                    
                    if display_status == "ALERT":
                        st.error(f"🚨 ALERT! AI Confidence: {result['probability_score']:.4f}")
                    else:
                        st.success(f"✅ SAFE. AI Confidence: {result['probability_score']:.4f}")
                    st.rerun() # Refresh the page to update the charts!
                else:
                    st.error("API Error: Check if server is running!")
            except Exception as e:
                st.error("Failed to connect.")

# --- TAB 2: BATCH PROCESSING ---
with tab_batch:
    st.markdown("Upload a CSV of transactions.")
    uploaded_file = st.file_uploader("Upload Transaction CSV", type=["csv"])

    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)
        st.success(f"Loaded {len(batch_df)} transactions!")
        
        if st.button("Run Batch Scan"):
            with st.spinner("Scanning batch for fraud..."):
                results = []
                for index, row in batch_df.iterrows():
                    payload = row.to_dict() 
                    try:
                        response = requests.post(API_URL, json=payload)
                        if response.status_code == 200:
                            res_data = response.json()
                            
                            display_status = "ALERT" if res_data["probability_score"] > CUSTOM_THRESHOLD else "SAFE"
                            results.append({
                                "ID": index,
                                "Amount": payload.get("Amount", 0),
                                "Status": display_status,
                                "Confidence": res_data["probability_score"]
                            })
                    except Exception as e:
                        st.error(f"API connection failed on row {index}.")
                        break
                
                # 2. Save the results into Streamlit's temporary memory, then refresh the page!
                st.session_state['batch_results'] = pd.DataFrame(results)
                st.rerun()

# --- BOTTOM ROW: BATCH RESULTS (Moved out of sidebar!) ---
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