import pandas as pd
import numpy as np

def generate_test_batch():
    # Define our 30 columns
    columns = [f"V{i}" for i in range(1, 29)] + ["Amount", "Transaction_Hour"]
    
    # --- 1. Generate 15 "SAFE" Transactions ---
    # Normal behavior: V columns are clustered around 0, amounts are small/medium, daytime hours
    safe_v = np.random.normal(loc=0.0, scale=0.5, size=(15, 28))
    safe_amounts = np.random.uniform(5.0, 300.0, size=(15, 1))
    safe_hours = np.random.randint(8, 22, size=(15, 1)) # 8 AM to 10 PM
    safe_data = np.hstack((safe_v, safe_amounts, safe_hours))
    
    # --- 2. Generate 5 "ALERT" (Fraudulent) Transactions ---
    # Hacker behavior: V1-V3 highly negative, V4 highly positive, massive amounts, 2 AM - 4 AM
    fraud_v = np.random.normal(loc=0.0, scale=1.0, size=(5, 28))
    fraud_v[:, 0] = np.random.uniform(-15.0, -5.0, size=5) # V1 extreme negative
    fraud_v[:, 1] = np.random.uniform(5.0, 15.0, size=5)   # V2 extreme positive
    fraud_v[:, 2] = np.random.uniform(-20.0, -10.0, size=5) # V3 extreme negative
    fraud_amounts = np.random.uniform(5000.0, 15000.0, size=(5, 1))
    fraud_hours = np.random.randint(2, 5, size=(5, 1)) # 2 AM to 4 AM
    fraud_data = np.hstack((fraud_v, fraud_amounts, fraud_hours))
    
    # Combine them
    all_data = np.vstack((safe_data, fraud_data))
    
    # Create DataFrame
    df = pd.DataFrame(all_data, columns=columns)
    
    # Shuffle the rows so the frauds are mixed in randomly!
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Round columns to look nice
    for col in columns:
        if col == "Transaction_Hour":
            df[col] = df[col].astype(int)
        else:
            df[col] = df[col].round(4)
            
    # Save to CSV
    df.to_csv("test_batch.csv", index=False)
    print("✅ Successfully generated 'test_batch.csv' with 20 mixed transactions!")

if __name__ == "__main__":
    generate_test_batch()