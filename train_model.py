# train_model.py

import pandas as pd
import os
import joblib
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Step 1: Load the balanced synthetic dataset
df = pd.read_csv("data/balanced_synthetic_grades.csv")

# Step 2: Convert final numeric grade to letter grades
def grade_to_label(grade):
    if grade >= 80:
        return "HD"
    elif grade >= 70:
        return "D"
    elif grade >= 60:
        return "C"
    elif grade >= 50:
        return "P"
    else:
        return "F"

df["label"] = df["final_grade"].apply(grade_to_label)

# Drop unused columns early to avoid leakage
df = df.drop(columns=["final_grade", "grade_letter"])

# Step 3: Encode label to numeric
label_map = {"F": 0, "P": 1, "C": 2, "D": 3, "HD": 4}
df["label"] = df["label"].map(label_map)

if df["label"].isna().any():
    print("❌ ERROR: Label mapping failed.")
    exit(1)

print("\n🔍 Label distribution:")
print(df["label"].value_counts())

# Step 4: One-hot encode the subject
df = pd.get_dummies(df, columns=["subject"])

# Step 5: Define X and y
X = df.drop(columns=["label"])
y = df["label"]

# Step 6: Stratified split
splitter = StratifiedShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
for train_idx, test_idx in splitter.split(X, y):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

print("\n✅ Test set label distribution:")
print(y_test.value_counts())

# Step 7: Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 8: Evaluate
y_pred = model.predict(X_test)
labels = list(label_map.values())
target_names = list(label_map.keys())

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred, labels=labels)
cm_list = cm.tolist()
with open("app/models/confusion_matrix.json", "w") as f:
    json.dump({"matrix": cm_list, "labels": target_names}, f, indent=4)

# Accuracy & classification report
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, labels=labels, target_names=target_names, output_dict=True)

with open("app/models/accuracy_report.json", "w") as f:
    json.dump(report, f, indent=4)

with open("app/models/accuracy_score.txt", "w") as f:
    f.write(str(accuracy))

print("✅ Accuracy:", accuracy)
print("📊 Classification Report:")
print(classification_report(y_test, y_pred, labels=labels, target_names=target_names))

# Step 9: Save model & mapping
os.makedirs("app/models", exist_ok=True)
joblib.dump(model, "app/models/grade_predictor.pkcls")
joblib.dump(label_map, "app/models/label_mapping.pkl")
print("📦 Model and label mapping saved.")
