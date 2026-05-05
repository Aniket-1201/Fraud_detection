import pandas as pd
import xgboost as xgb
import wandb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

# 1. Start a W&B Run
wandb.init(project="fraud-detection-mlops", name="xgboost-baseline")

# 2. Load the data
print("Loading data...")
df = pd.read_csv("../data/creditcard.csv")

# 3. Prepare features (X) and target (y)
X = df.drop(columns=['Class', 'Time']) # Dropping Class (target) and Time
y = df['Class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train the Model
print("Training XGBoost model...")
model = xgb.XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1)
model.fit(X_train, y_train)

# 5. Evaluate and Log Metrics
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions) # Recall is the most important for fraud!

print(f"Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}")

# Log to Weights & Biases
wandb.log({
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall
})

print("Training complete and logged to W&B!")
