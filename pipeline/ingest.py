import pandas as pd
from prefect import task, flow
from schema import TransactionSchema
from pydantic import ValidationError

@task
def load_data(file_path: str) -> pd.DataFrame:
    print(f"Loading data from {file_path}...")
    return pd.read_csv(file_path)

@task
def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    print("Validating data structure with Pydantic...")
    # To keep your laptop fast, we validate a sample row. 
    # In enterprise production, you'd validate in batches!
    try:
        sample_row = df.iloc[0].to_dict()
        TransactionSchema(**sample_row)
        print("Schema validation passed successfully!")
    except ValidationError as e:
        print(f"CRITICAL: Data validation failed: {e}")
        raise # Crash the pipeline if the schema is fundamentally broken
    return df

@task
def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    print("Engineering temporal features...")
    # Convert elapsed seconds into 'Hour of the Day' (0-23)
    df['Transaction_Hour'] = (df['Time'] // 3600) % 24
    
    # Drop the old, useless Time column
    df = df.drop(columns=['Time'])
    return df

@task
def save_data(df: pd.DataFrame, output_path: str):
    print(f"Saving engineered data to {output_path}...")
    df.to_csv(output_path, index=False)

@flow(name="Fraud-Data-Pipeline-V2")
def feature_engineering_flow():
    raw_path = "data/creditcard.csv"
    engineered_path = "data/engineered_creditcard.csv"
    
    df = load_data(raw_path)
    df = validate_data(df)
    df = engineer_features(df)
    save_data(df, engineered_path)

if __name__ == "__main__":
    feature_engineering_flow()