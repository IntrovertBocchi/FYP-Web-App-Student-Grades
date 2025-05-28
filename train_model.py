# train_model.py

import pandas as pd
import os
import joblib
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils.multiclass import unique_labels

# Step 1: Load synthetic data
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

# Step 3: Drop the final_grade column (not needed anymore)
df = df.drop(columns=["final_grade"])

# Step 4: Encode label to numeric values
label_map = {"F": 0, "P": 1, "C": 2, "D": 3, "HD": 4}
df["label"] = df["label"].map(label_map)

# Optional: Fail early if mapping fails
if df["label"].isna().any():
    print("❌ ERROR: Some labels could not be mapped.")
    print(df[df["label"].isna()][["label", "grade_letter"]].head())
    exit(1)

print("\n🔍 Labels after mapping:")
print(df["label"].value_counts(dropna=False))

# Step 5: Split features and labels
X = df.drop(columns=["label", "subject", "grade_letter"])
y = df["label"]

# Step 6: Train/test split
# Make sure all classes have at least one sample in the test set
from sklearn.model_selection import StratifiedShuffleSplit

splitter = StratifiedShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
for train_idx, test_idx in splitter.split(X, y):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

print("\n✅ Label distribution in test set:")
print(y_test.value_counts())

# Step 7: Train a classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 8: Evaluate
y_pred = model.predict(X_test)

from sklearn.metrics import confusion_matrix

# Ensure all labels are represented in the report
all_labels = list(label_map.values())          # [0, 1, 2, 3, 4]
all_target_names = list(label_map.keys())      # ["F", "P", "C", "D", "HD"]

# Step 8.1: Save confusion matrix
cm = confusion_matrix(y_test, y_pred, labels=all_labels)
cm_list = cm.tolist()  # JSON serializable
with open('app/models/confusion_matrix.json', 'w') as f:
    json.dump({
        "matrix": cm_list,
        "labels": all_target_names
    }, f, indent=4)

print("📊 Confusion matrix saved to app/models/confusion_matrix.json")
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:\n")

print(classification_report(
    y_test,
    y_pred,
    labels=all_labels,
    target_names=all_target_names,
    zero_division=0
))

# Save classification report as dict
report = classification_report(y_test, y_pred, output_dict=True)
with open('app/models/accuracy_report.json', 'w') as f:
    json.dump(report, f, indent=4)

# Save accuracy separately
accuracy_value = accuracy_score(y_test, y_pred)
with open('app/models/accuracy_score.txt', 'w') as f:
    f.write(str(accuracy_value))


# Step 9: Save the model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "app/models/grade_predictor.pkcls")
print("\n📦 Model saved to app/models/grade_predictor.pkcls")

# Save label mapping
label_mapping = {0: "F", 1: "P", 2: "C", 3: "D", 4: "HD"}
joblib.dump(label_mapping, 'app/models/label_mapping.pkl')
print("🧾 Label mapping saved to app/models/label_mapping.pkl")