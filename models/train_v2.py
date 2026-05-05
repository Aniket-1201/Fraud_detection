import pandas as pd
import xgboost as xgb
import wandb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

# 1. Start a NEW W&B Run
wandb.init(project="fraud-detection-mlops", name="xgboost-tuned-v2")

# 2. Load the NEW engineered data
print("Loading engineered data...")
df = pd.read_csv("../data/engineered_creditcard.csv")

# 3. Prepare features (X) and target (y)
# (Assuming Aniket kept the target column named 'Class')
X = df.drop(columns=["Class"])
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Train the Tuned Model
print("Training Tuned XGBoost model...")
# We increased max_depth to find more complex patterns
# We added scale_pos_weight to heavily penalize missing a fraudulent transaction
model = xgb.XGBClassifier(
    n_estimators=150, max_depth=5, learning_rate=0.05, scale_pos_weight=10
)
model.fit(X_train, y_train)

# 5. Evaluate and Log Metrics
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)

print(f"Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}")

# Log to Weights & Biases
wandb.log({"accuracy": accuracy, "precision": precision, "recall": recall})

print("V2 Training complete and logged to W&B!")
model.save_model("xgb_model.json")
