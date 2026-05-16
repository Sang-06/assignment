import pandas as pd
import joblib

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# ── Load Dataset ──────────────────────────────────────
data = load_breast_cancer()
X = data.data
y = data.target

# ── Train Test Split ──────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Feature Scaling ───────────────────────────────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ── Define Models — Simplest to Most Complex ──────────
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree":       DecisionTreeClassifier(max_depth=5, random_state=42),
    "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42)
}

# ── PART 1 — Metric Comparison Table ─────────────────
print("\n======== Part 1: Metric Comparison Table ========\n")

results       = []
trained_models = {}
f1_scores      = {}

for model_name, model in models.items():

    # Train
    model.fit(X_train_scaled, y_train)

    # Save trained model
    trained_models[model_name] = model

    # Predict
    y_pred = model.predict(X_test_scaled)

    # Metrics
    accuracy  = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall    = recall_score(y_test, y_pred)
    f1        = f1_score(y_test, y_pred)

    # Store f1 for Part 3
    f1_scores[model_name] = f1

    results.append({
        "Model":     model_name,
        "Accuracy":  round(accuracy,  4),
        "Precision": round(precision, 4),
        "Recall":    round(recall,    4),
        "F1-Score":  round(f1,        4)
    })

# Create DataFrame
metrics_df = pd.DataFrame(results)
metrics_df.set_index("Model", inplace=True)
print(metrics_df)

# ── PART 2 — Overfitting Check ────────────────────────
print("\n======== Part 2: Overfitting Check ==============\n")

decision_tree = trained_models["Decision Tree"]

# Train predictions
y_train_pred_dt = decision_tree.predict(X_train_scaled)

# Test predictions
y_test_pred_dt  = decision_tree.predict(X_test_scaled)

# Accuracy scores
train_accuracy = accuracy_score(y_train, y_train_pred_dt)
test_accuracy  = accuracy_score(y_test,  y_test_pred_dt)

# Gap
gap = train_accuracy - test_accuracy

print(f"Training Accuracy : {train_accuracy:.4f}")
print(f"Test Accuracy     : {test_accuracy:.4f}")
print(f"Train-Test Gap    : {gap:.4f}")

# Diagnostic
if gap > 0.05:
    print("⚠ Overfitting detected — gap exceeds 5%")
elif train_accuracy < 0.85:
    print("⚠ Underfitting detected — training accuracy too low")
else:
    print("✓ Model is at the sweet spot — acceptable gap")

# ── PART 3 — Start Simple Go Complex Protocol ─────────
print("\n======== Part 3: Model Selection ================\n")

# Best F1 Score
best_f1 = max(f1_scores.values())

selected_model_name = None
selected_model      = None
selected_score      = None

# Iterate simplest to most complex
for model_name in models.keys():
    score = f1_scores[model_name]

    # Within 2 percentage points of best
    if score >= (best_f1 - 0.02):
        selected_model_name = model_name
        selected_model      = trained_models[model_name]
        selected_score      = score
        break

print(
    f"Selected Model: {selected_model_name} | "
    f"F1-Score: {selected_score:.4f}"
)

# ── PART 4 — Save Selected Model ─────────────────────
print("\n======== Part 4: Saving Model ===================\n")

# Save model
joblib.dump(selected_model, "tumour_classifier_v1.joblib")
print("✓ Model saved as tumour_classifier_v1.joblib")

# Save scaler
joblib.dump(scaler, "tumour_scaler_v1.joblib")
print("✓ Scaler saved as tumour_scaler_v1.joblib")

# ── PART 5 — Verify Model Persistence ────────────────
print("\n======== Part 5: Persistence Verification =======\n")

# Load model and scaler
loaded_model  = joblib.load("tumour_classifier_v1.joblib")
loaded_scaler = joblib.load("tumour_scaler_v1.joblib")

# Transform test data
X_test_loaded_scaled = loaded_scaler.transform(X_test)

# Predict
loaded_predictions = loaded_model.predict(X_test_loaded_scaled)

# Print first 10
print("Predictions vs Actual (first 10):")
print("Predicted:", loaded_predictions[:10])
print("Actual:   ", y_test[:10])

# Verification
if (loaded_predictions[:10] == y_test[:10]).all():
    print("\n✓ Pipeline verified successfully end-to-end")
else:
    print("\n⚠ Verification mismatch detected")

print("\n✅ All 5 Parts Complete!")