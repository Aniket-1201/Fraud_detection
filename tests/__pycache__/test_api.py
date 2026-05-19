from fastapi.testclient import TestClient
from api.app import app 

def test_health_check():
    """Test if the API is running and returning a 200 status code."""
    # The 'with' statement forces the app to run its startup events (loading the model)
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200

def test_predict_endpoint_valid_data():
    """Test if the /predict endpoint accepts valid data and returns a prediction."""
    dummy_payload = {
        "Time": 0.0,
        "Transaction_Hour": 0.0,
        "V1": 0.0, "V2": 0.0, "V3": 0.0, "V4": 0.0, "V5": 0.0, 
        "V6": 0.0, "V7": 0.0, "V8": 0.0, "V9": 0.0, "V10": 0.0,
        "V11": 0.0, "V12": 0.0, "V13": 0.0, "V14": 0.0, "V15": 0.0,
        "V16": 0.0, "V17": 0.0, "V18": 0.0, "V19": 0.0, "V20": 0.0,
        "V21": 0.0, "V22": 0.0, "V23": 0.0, "V24": 0.0, "V25": 0.0,
        "V26": 0.0, "V27": 0.0, "V28": 0.0,
        "Amount": 100.50
    }
    
    # Using 'with' here guarantees the model is loaded before we post the data!
    with TestClient(app) as client:
        response = client.post("/predict", json=dummy_payload)
        
        # If it fails, print the exact reason
        assert response.status_code == 200, f"API rejected payload. Reason: {response.text}"
        
        response_data = response.json()
        assert "prediction" in response_data or "status" in response_data