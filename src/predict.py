import pandas as pd
import joblib
import os

# Use forward slash or raw string for Windows path
MODEL = "models/best_model.pkl"

FEATURES = [
    "Hours_Studied", "Attendance", "Parental_Involvement", "Access_to_Resources",
    "Extracurricular_Activities", "Sleep_Hours", "Previous_Scores", "Motivation_Level",
    "Internet_Access", "Tutoring_Sessions", "Family_Income", "Teacher_Quality",
    "School_Type", "Peer_Influence", "Physical_Activity", "Learning_Disabilities",
    "Parental_Education_Level", "Distance_from_Home", "Gender",
    "study_efficiency", "engagement_score", "risk_score",
]

encode = {
    "Parental_Involvement":      {"Low": 0, "Medium": 1, "High": 2},
    "Access_to_Resources":       {"Low": 0, "Medium": 1, "High": 2},
    "Motivation_Level":          {"Low": 0, "Medium": 1, "High": 2},
    "Family_Income":             {"Low": 0, "Medium": 1, "High": 2},
    "Teacher_Quality":           {"Low": 0, "Medium": 1, "High": 2},
    "Parental_Education_Level":  {"High School": 0, "College": 1, "Postgraduate": 2},
    "Distance_from_Home":        {"Near": 0, "Moderate": 1, "Far": 2},
    "Peer_Influence":            {"Negative": 0, "Neutral": 1, "Positive": 2},
    "Extracurricular_Activities": {"No": 0, "Yes": 1},
    "Internet_Access":           {"No": 0, "Yes": 1},
    "Learning_Disabilities":     {"No": 0, "Yes": 1},
    "Gender":                    {"Female": 0, "Male": 1},
    "School_Type":               {"Public": 0, "Private": 1},
}

# ── Edit this student ──────────────────────────────────────
student = {
    "Hours_Studied":             10,
    "Attendance":                60,
    "Parental_Involvement":      "Low",
    "Access_to_Resources":       "Low",
    "Extracurricular_Activities": "No",
    "Sleep_Hours":               5,
    "Previous_Scores":           55,
    "Motivation_Level":          "Low",
    "Internet_Access":           "No",
    "Tutoring_Sessions":         0,
    "Family_Income":             "Low",
    "Teacher_Quality":           "Low",
    "School_Type":               "Public",
    "Peer_Influence":            "Negative",
    "Physical_Activity":         1,
    "Learning_Disabilities":     "Yes",
    "Parental_Education_Level":  "High School",
    "Distance_from_Home":        "Far",
    "Gender":                    "Male",
}
# ──────────────────────────────────────────────────────────

# Encode categorical values
for col, mapping in encode.items():
    student[col] = mapping[student[col]]

# Calculate engineered features
student["study_efficiency"] = round(
    student["Hours_Studied"] / max(student["Sleep_Hours"], 1), 2)
student["engagement_score"] = round(
    student["Attendance"]/100*2 + student["Motivation_Level"] + student["Extracurricular_Activities"], 2)
student["risk_score"] = sum([
    student["Motivation_Level"] == 0,
    student["Family_Income"] == 0,
    student["Learning_Disabilities"] == 1,
    student["Access_to_Resources"] == 0,
    student["Peer_Influence"] == 0,
    student["Parental_Involvement"] == 0,
    student["Internet_Access"] == 0,
    student["Distance_from_Home"] == 2,
])

# Check if model exists
if not os.path.exists(MODEL):
    print(f"Error: Model not found at {MODEL}")
    print("Make sure you're in the correct directory and the model file exists.")
    exit(1)

# Load model and predict
model = joblib.load(MODEL)
X = pd.DataFrame([student])[FEATURES]
pred = model.predict(X)[0]
prob = model.predict_proba(X)[0][1]

# Output results
print("\n" + "="*40)
print("STUDENT PREDICTION RESULTS")
print("="*40)
print(f"Decision:     {'SKIP' if pred == 1 else 'ATTEND'}")
print(f"Confidence:   {round(prob * 100, 1)}%")
print(f"Risk Score:   {student['risk_score']} / 8")
print("="*40)
