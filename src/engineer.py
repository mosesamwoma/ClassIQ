import pandas as pd

PROCESSED = "data/processed/cleaned.csv"
ENGINEERED = "data/processed/ClassIQ_ready.csv"

df = pd.read_csv(PROCESSED)

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

for col, mapping in encode.items():
    df[col] = df[col].map(mapping)

df["study_efficiency"] = (df["Hours_Studied"] /
                          df["Sleep_Hours"].clip(lower=1)).round(2)
df["engagement_score"] = (df["Attendance"]/100*2 +
                          df["Motivation_Level"] + df["Extracurricular_Activities"]).round(2)
df["risk_score"] = (
    (df["Motivation_Level"] == 0).astype(int) +
    (df["Family_Income"] == 0).astype(int) +
    (df["Learning_Disabilities"] == 1).astype(int) +
    (df["Access_to_Resources"] == 0).astype(int) +
    (df["Peer_Influence"] == 0).astype(int) +
    (df["Parental_Involvement"] == 0).astype(int) +
    (df["Internet_Access"] == 0).astype(int) +
    (df["Distance_from_Home"] == 2).astype(int)
)

df["skip_recommended"] = ((df["Attendance"] < 75) &
                          (df["risk_score"] > 3)).astype(int)

df.to_csv(ENGINEERED, index=False)
print("Skip rate:", round(df["skip_recommended"].mean()*100, 1), "%")
