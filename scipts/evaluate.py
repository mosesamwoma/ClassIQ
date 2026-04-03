import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

DATA = "data/processed/skipsense_ready.csv"
MODEL = "models/best_model.pkl"

FEATURES = [
    "Hours_Studied", "Attendance", "Parental_Involvement", "Access_to_Resources",
    "Extracurricular_Activities", "Sleep_Hours", "Previous_Scores", "Motivation_Level",
    "Internet_Access", "Tutoring_Sessions", "Family_Income", "Teacher_Quality",
    "School_Type", "Peer_Influence", "Physical_Activity", "Learning_Disabilities",
    "Parental_Education_Level", "Distance_from_Home", "Gender",
    "study_efficiency", "engagement_score", "risk_score",
]

df = pd.read_csv(DATA)
X = df[FEATURES]
y = df["skip_recommended"]

_, X_test, _, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

model = joblib.load(MODEL)
y_pred = model.predict(X_test)

print("Accuracy:", round(accuracy_score(y_test, y_pred), 4))
print(classification_report(y_test, y_pred, target_names=["Attend", "Skip"]))

cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(
    f"  Actual Attend → Predicted Attend: {cm[0][0]}  |  Predicted Skip: {cm[0][1]}")
print(
    f"  Actual Skip   → Predicted Attend: {cm[1][0]}  |  Predicted Skip: {cm[1][1]}")
