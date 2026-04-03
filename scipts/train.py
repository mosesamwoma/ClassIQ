import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from xgboost import XGBClassifier

DATA = "data/processed/ClassIQ_ready.csv"

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

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

rf = RandomForestClassifier(
    n_estimators=200, max_depth=10, class_weight="balanced", random_state=42)
rf.fit(X_train, y_train)
rf_f1 = f1_score(y_test, rf.predict(X_test))
print("Random Forest F1:", round(rf_f1, 4))

xgb = XGBClassifier(n_estimators=300, max_depth=6,
                    learning_rate=0.05, eval_metric="logloss", random_state=42)
xgb.fit(X_train, y_train)
xgb_f1 = f1_score(y_test, xgb.predict(X_test))
print("XGBoost F1:      ", round(xgb_f1, 4))

best = xgb if xgb_f1 >= rf_f1 else rf
joblib.dump(best, "models/best_model.pkl")
print("Saved:", "XGBoost" if xgb_f1 >= rf_f1 else "RandomForest")
