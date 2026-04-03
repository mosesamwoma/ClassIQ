import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(
    page_title="SkipSense - Student Attendance Predictor",
    layout="wide"
)

MODEL = "models/best_model.pkl"


@st.cache_resource
def load_model():
    if os.path.exists(MODEL):
        return joblib.load(MODEL)
    else:
        st.error(f"Model not found at {MODEL}")
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

st.title("SkipSense")
st.subheader("Student Attendance Prediction System")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Academic Information")
    hours_studied = st.slider("Hours Studied per Week", 0, 40, 10)
    attendance = st.slider("Attendance (%)", 0, 100, 60)
    previous_scores = st.slider("Previous Exam Scores", 0, 100, 55)
    tutoring_sessions = st.number_input("Tutoring Sessions per Week", 0, 10, 0)
    sleep_hours = st.slider("Sleep Hours per Day", 3, 12, 5)
    physical_activity = st.slider("Physical Activity (hours/week)", 0, 20, 1)

with col2:
    st.markdown("Student Profile")
    parental_involvement = st.selectbox(
        "Parental Involvement", ["Low", "Medium", "High"])
    access_to_resources = st.selectbox(
        "Access to Resources", ["Low", "Medium", "High"])
    motivation_level = st.selectbox(
        "Motivation Level", ["Low", "Medium", "High"])
    family_income = st.selectbox("Family Income", ["Low", "Medium", "High"])
    teacher_quality = st.selectbox(
        "Teacher Quality", ["Low", "Medium", "High"])
    parental_education = st.selectbox("Parental Education Level", [
                                      "High School", "College", "Postgraduate"])

col3, col4 = st.columns(2)

with col3:
    st.markdown("School & Environment")
    school_type = st.selectbox("School Type", ["Public", "Private"])
    peer_influence = st.selectbox(
        "Peer Influence", ["Negative", "Neutral", "Positive"])
    distance_from_home = st.selectbox(
        "Distance from Home", ["Near", "Moderate", "Far"])

with col4:
    st.markdown("Additional Factors")
    extracurricular = st.selectbox("Extracurricular Activities", ["No", "Yes"])
    internet_access = st.selectbox("Internet Access", ["No", "Yes"])
    learning_disabilities = st.selectbox(
        "Learning Disabilities", ["No", "Yes"])
    gender = st.selectbox("Gender", ["Female", "Male"])

student = {
    "Hours_Studied": hours_studied,
    "Attendance": attendance,
    "Parental_Involvement": parental_involvement,
    "Access_to_Resources": access_to_resources,
    "Extracurricular_Activities": extracurricular,
    "Sleep_Hours": sleep_hours,
    "Previous_Scores": previous_scores,
    "Motivation_Level": motivation_level,
    "Internet_Access": internet_access,
    "Tutoring_Sessions": tutoring_sessions,
    "Family_Income": family_income,
    "Teacher_Quality": teacher_quality,
    "School_Type": school_type,
    "Peer_Influence": peer_influence,
    "Physical_Activity": physical_activity,
    "Learning_Disabilities": learning_disabilities,
    "Parental_Education_Level": parental_education,
    "Distance_from_Home": distance_from_home,
    "Gender": gender,
}

st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    predict_btn = st.button("PREDICT ATTENDANCE RISK",
                            use_container_width=True)

if predict_btn and model:
    for col, mapping in encode.items():
        student[col] = mapping[student[col]]

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

    X = pd.DataFrame([student])[FEATURES]
    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0][1]

    st.balloons()

    st.markdown("---")
    st.markdown("PREDICTION RESULT")

    col_res1, col_res2 = st.columns(2)

    with col_res1:
        if pred == 1:
            st.error("RECOMMENDATION: SKIP")
            st.warning(
                "High risk of poor performance. Intervention recommended.")
        else:
            st.success("RECOMMENDATION: ATTEND")
            st.info("Likely to perform well. Maintain support.")

    with col_res2:
        st.metric("Confidence", f"{prob * 100:.1f}%")
        st.metric("Risk Score", f"{student['risk_score']} / 8")

    st.markdown("---")
    st.markdown("Risk Factors Breakdown")

    risk_factors = []
    if student["Motivation_Level"] == 0:
        risk_factors.append("Low Motivation")
    if student["Family_Income"] == 0:
        risk_factors.append("Low Family Income")
    if student["Learning_Disabilities"] == 1:
        risk_factors.append("Learning Disabilities")
    if student["Access_to_Resources"] == 0:
        risk_factors.append("Poor Resource Access")
    if student["Peer_Influence"] == 0:
        risk_factors.append("Negative Peer Influence")
    if student["Parental_Involvement"] == 0:
        risk_factors.append("Low Parental Involvement")
    if student["Internet_Access"] == 0:
        risk_factors.append("No Internet Access")
    if student["Distance_from_Home"] == 2:
        risk_factors.append("Far Distance from Home")

    if risk_factors:
        for factor in risk_factors:
            st.write(factor)
    else:
        st.success("No major risk factors detected")

    if student["risk_score"] >= 5:
        st.warning("High Risk Alert: Immediate intervention recommended.")

st.markdown("---")
st.caption("SkipSense - AI-Powered Student Attendance Prediction System")
