import requests
import json

# The URL of your local FastAPI server
url = "http://127.0.0.1:8000/predict"

# A fake transaction (simulating a hacker trying to buy something expensive at 3 AM)
# Note: I included standard Kaggle V-columns and your engineered Transaction_Hour
fake_swipe = {
    "V1": -1.2, "V2": 2.5, "V3": -3.0, "V4": 1.1, "V5": -0.5,
    "V6": -1.0, "V7": -2.0, "V8": 0.8, "V9": -1.5, "V10": -3.5,
    "V11": 2.0, "V12": -4.0, "V13": 0.5, "V14": -5.0, "V15": 0.1,
    "V16": -2.5, "V17": -4.5, "V18": -1.0, "V19": 1.5, "V20": 0.2,
    "V21": 0.5, "V22": -0.2, "V23": 0.1, "V24": -0.4, "V25": 0.2,
    "V26": 0.3, "V27": 0.4, "V28": -0.1,
    "Amount": 8500.00,  # Highly suspicious amount
    "Transaction_Hour": 3 # 3 AM
}

print("Sending fake transaction to API...")

# Send the POST request
try:
    response = requests.post(url, json=fake_swipe)
    
    # Print the AI's verdict!
    print("\n--- API RESPONSE ---")
    print(json.dumps(response.json(), indent=4))
    
except Exception as e:
    print(f"Failed to connect to API: {e}")