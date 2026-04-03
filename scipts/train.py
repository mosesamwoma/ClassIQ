import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(
    page_title="SkipSense",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: white;
}
.card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 0 10px rgba(0,0,0,0.4);
}
.metric-box {
    background-color: #1f2937;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
.stButton>button {
    background: linear-gradient(90deg, #4f46e5, #9333ea);
    color: white;
    border-radius: 10px;
    height: 50px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

MODEL = "models/best_model.pkl"


@st.cache_resource
def load_model():
    if os.path.exists(MODEL):
        return joblib.load(MODEL)
    else:
        st.error("Model not found")
        return None


model = load_model()

FEATURES = [
    "Hours_Studied", "Attendance", "Parental_Involvement", "Access_to_Resources",
    "Extracurricular_Activities", "Sleep_Hours", "Previous_Scores", "Motivation_Level",
    "Internet_Access", "Tutoring_Sessions", "Family_Income", "Teacher_Quality",
    "School_Type", "Peer_Influence", "Physical_Activity", "Learning_Disabilities",
    "Parental_Education_Level", "Distance_from_Home", "Gender",
    "study_efficiency", "engagement_score", "risk_score",
]

encode = {
    "Parental_Involvement": {"Low": 0, "Medium": 1, "High": 2},
    "Access_to_Resources": {"Low": 0, "Medium": 1, "High": 2},
    "Motivation_Level": {"Low": 0, "Medium": 1, "High": 2},
    "Family_Income": {"Low": 0, "Medium": 1, "High": 2},
    "Teacher_Quality": {"Low": 0, "Medium": 1, "High": 2},
    "Parental_Education_Level": {"High School": 0, "College": 1, "Postgraduate": 2},
    "Distance_from_Home": {"Near": 0, "Moderate": 1, "Far": 2},
    "Peer_Influence": {"Negative": 0, "Neutral": 1, "Positive": 2},
    "Extracurricular_Activities": {"No": 0, "Yes": 1},
    "Internet_Access": {"No": 0, "Yes": 1},
    "Learning_Disabilities": {"No": 0, "Yes": 1},
    "Gender": {"Female": 0, "Male": 1},
    "School_Type": {"Public": 0, "Private": 1},
}

# ---------- HEADER ----------
st.title("SkipSense")
st.caption("AI-powered student attendance prediction")

# ---------- SIDEBAR INPUT ----------
st.sidebar.header("Student Inputs")

hours_studied = st.sidebar.slider("Hours Studied", 0, 40, 10)
attendance = st.sidebar.slider("Attendance (%)", 0, 100, 60)
previous_scores = st.sidebar.slider("Previous Scores", 0, 100, 55)
sleep_hours = st.sidebar.slider("Sleep Hours", 3, 12, 6)

motivation_level = st.sidebar.selectbox(
    "Motivation", ["Low", "Medium", "High"])
parental_involvement = st.sidebar.selectbox(
    "Parental Involvement", ["Low", "Medium", "High"])
peer_influence = st.sidebar.selectbox(
    "Peer Influence", ["Negative", "Neutral", "Positive"])
family_income = st.sidebar.selectbox(
    "Family Income", ["Low", "Medium", "High"])

student = {
    "Hours_Studied": hours_studied,
    "Attendance": attendance,
    "Parental_Involvement": parental_involvement,
    "Access_to_Resources": "Medium",
    "Extracurricular_Activities": "Yes",
    "Sleep_Hours": sleep_hours,
    "Previous_Scores": previous_scores,
    "Motivation_Level": motivation_level,
    "Internet_Access": "Yes",
    "Tutoring_Sessions": 1,
    "Family_Income": family_income,
    "Teacher_Quality": "Medium",
    "School_Type": "Public",
    "Peer_Influence": peer_influence,
    "Physical_Activity": 2,
    "Learning_Disabilities": "No",
    "Parental_Education_Level": "College",
    "Distance_from_Home": "Near",
    "Gender": "Male",
}

# ---------- PREDICT BUTTON ----------
predict = st.button("Predict Risk")

if predict and model:

    for col, mapping in encode.items():
        student[col] = mapping[student[col]]

    student["study_efficiency"] = student["Hours_Studied"] / \
        max(student["Sleep_Hours"], 1)
    student["engagement_score"] = student["Attendance"] / \
        100*2 + student["Motivation_Level"]
    student["risk_score"] = sum([
        student["Motivation_Level"] == 0,
        student["Family_Income"] == 0,
        student["Peer_Influence"] == 0
    ])

    X = pd.DataFrame([student])[FEATURES]
    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0][1]

    st.balloons()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        if pred == 1:
            st.error("High Risk - Consider Skipping")
        else:
            st.success("Low Risk - Safe to Attend")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("Confidence", f"{prob*100:.1f}%")
        st.metric("Risk Score", student["risk_score"])
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("SkipSense AI System")
