import pandas as pd
import numpy as np
from numpy.random import default_rng
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# ── EXACT DATASET FROM QUESTION ──────────────────────
rng = default_rng(seed=99)
n = 500

study_hours        = rng.uniform(1, 10, size=n)
attendance_percent = rng.uniform(40, 100, size=n)
assignments_done   = rng.uniform(0, 10, size=n)

scores = (
    20
    + 5.5  * study_hours
    + 0.4  * attendance_percent
    + 3.0  * assignments_done
    + rng.normal(0, 8, size=n)
)

y = (scores >= 70).astype(int)
X = np.column_stack([study_hours, attendance_percent, assignments_done])

#Task1___________________________
# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=99)
#print("Training samples:", len(X_train))
#print("Testing samples :", len(X_test))

# Train
model = LogisticRegression()
model.fit(X_train, y_train)
#print("Model trained successfully!")

# Class distribution
#print("Class Distribution:")
#print("Pass (1):", sum(y == 1))
#print("Fail (0):", sum(y == 0))

#Task2_________________________________
y_pred  = model.predict(X_test)
y_proba = model.predict_proba(X_test)
p_pass  = y_proba[:, 1]

# Print table header
#print("\n#  | Study Hrs | Attendance% | Assignments | Actual | Predicted | P(Pass) | Correct?")
#print("-" * 85)

# Print first 10 students
for i in range(10):
    actual    = "Pass" if y_test[i] == 1 else "Fail"
    predicted = "Pass" if y_pred[i] == 1 else "Fail"
    correct   = "Yes"  if y_test[i] == y_pred[i] else "No"

    #print(f"{i+1:<3}| "
         # f"{X_test[i][0]:<10.2f}| "
         # f"{X_test[i][1]:<12.2f}| "
         # f"{X_test[i][2]:<12.2f}| "
         # f"{actual:<7}| "
         # f"{predicted:<10}| "
         # f"{p_pass[i]:<8.4f}| "
         # f"{correct}")


#Task3__________________________
#Confusion Matrix & Accuracy

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
TN, FP, FN, TP = cm.ravel()

# Print individually
#print("\n--- TASK 3 ---")
#print("TP (True Positive)  =", TP, "→ Correctly predicted Pass")
#print("TN (True Negative)  =", TN, "→ Correctly predicted Fail")
#print("FP (False Positive) =", FP, "→ Wrongly predicted Pass")
#print("FN (False Negative) =", FN, "→ Wrongly predicted Fail")

# Manual Accuracy
accuracy = (TP + TN) / (TP + TN + FP + FN)
#print("\nAccuracy =", round(accuracy, 4))
#print("Accuracy =", round(accuracy * 100, 2), "%")

#Task4 ___________Compare two decision thresholds
p_pass_all = model.predict_proba(X_test)[:, 1]

for threshold in [0.5, 0.6]:
    preds  = (p_pass_all >= threshold).astype(int)
    n_pass = sum(preds == 1)
    n_fail = sum(preds == 0)
    acc    = sum(preds == y_test) / len(y_test)

    print("\n--- Threshold =", threshold, "---")
    print("Students predicted Pass :", n_pass)
    print("Students predicted Fail :", n_fail)
    print("Accuracy :", round(acc * 100, 2), "%")



 
