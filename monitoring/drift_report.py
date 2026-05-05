import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

print("Loading data...")
# Load the engineered data Aniket created
df = pd.read_csv("data/engineered_creditcard.csv")

# Simulate a production environment
# We use older data as the "Reference" (what the model learned on)
reference_data = df[:50000]
# We use newer data as the "Current" (what is hitting the API today)
current_data = df[50000:60000]

print("Generating Data Drift Report...")
# Initialize the Evidently Report with the Data Drift preset
drift_report = Report(metrics=[DataDriftPreset()])

# Run the comparison
drift_report.run(reference_data=reference_data, current_data=current_data)

# Save the dashboard as an interactive HTML file
file_name = "fraud_data_drift_report.html"
drift_report.save_html(file_name)

print(f"✅ Success! Open '{file_name}' in your web browser to see the dashboard.")
