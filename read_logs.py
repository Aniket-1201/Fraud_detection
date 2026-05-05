import sqlite3
import pandas as pd

def check_database():
    print("Connecting to fraud audit logs...")
    conn = sqlite3.connect("fraud_logs.db")
    
    # Read the data into a Pandas DataFrame so it looks nice
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    
    if df.empty:
        print("The database is empty! Did you send a swipe via the /docs page?")
    else:
        print("\n--- RECENT TRANSACTIONS ---")
        print(df.tail(5).to_string(index=False))
        
    conn.close()

if __name__ == "__main__":
    check_database()