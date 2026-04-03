import pandas as pd

RAW = "data/raw/StudentPerformanceFactors.csv"
PROCESSED = "data/processed/cleaned.csv"

df = pd.read_csv(RAW)

for col in ["Teacher_Quality", "Parental_Education_Level", "Distance_from_Home"]:
    df[col] = df[col].fillna(df[col].mode()[0])

df["Exam_Score"] = df["Exam_Score"].clip(upper=100)

df.to_csv(PROCESSED, index=False)
print("Done. Rows:", len(df))
