from fastapi import FastAPI
from pydantic import BaseModel
import xgboost as xgb
import pandas as pd
import sqlite3
import sys
import os
from datetime import datetime

# Allow importing from your pipeline folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pipeline.schema import TransactionSchema

app = FastAPI(title="Fraud Detection API", version="1.0")

# Global variable to hold our AI model
ml_model = None

def init_db():
    """Creates a local database file to log transactions."""
    conn = sqlite3.connect("fraud_logs.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            probability REAL,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

@app.on_event("startup")
def startup_event():
    """Runs when the server turns on."""
    global ml_model
    
    # 1. Initialize the database
    init_db()
    
    # 2. Load the model
    print("Loading XGBoost model...")
    ml_model = xgb.XGBClassifier()
    ml_model.load_model("models/xgb_model.json") 
    print("Model loaded successfully!")

@app.get("/")
def home():
    return {"message": "Fraud Detection Server is Live with Logging!"}

@app.post("/predict")
def predict_fraud(transaction: TransactionSchema):
    """Receives a swipe, scores it, and logs it to the database."""
    
    input_data = pd.DataFrame([transaction.dict()])
    fraud_probability = ml_model.predict_proba(input_data)[:, 1][0]
    
    # Business Logic
    if fraud_probability > 0.005: 
        status = "DECLINED"
        alert = "HIGH RISK: Fraud Detected"
    else:
        status = "APPROVED"
        alert = "None"
    # --- NEW: Log the transaction to SQLite ---
    conn = sqlite3.connect("fraud_logs.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (amount, probability, status)
        VALUES (?, ?, ?)
    ''', (transaction.Amount, float(fraud_probability), status))
    conn.commit()
    conn.close()
    # ----------------------------------------
    
    return {
        "status": status,
        "alert": alert,
        "probability_score": float(fraud_probability)
    }
@app.get("/logs")
def get_logs():
    """API Endpoint for the frontend to fetch logs safely."""
    try:
        conn = sqlite3.connect("fraud_logs.db")
        # This makes sqlite return dictionaries instead of raw tuples!
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        # Fetch the latest transactions
        cursor.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT 100")
        rows = cursor.fetchall()
        conn.close()
        
        # Send the data over the internet as JSON
        return {"logs": [dict(row) for row in rows]}
    except Exception as e:
        return {"logs": []}