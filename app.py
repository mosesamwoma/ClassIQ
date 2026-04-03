import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(
    page_title="ClassIQ - Student Attendance Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Title styling */
    h1 {
        color: white;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        letter-spacing: -1px;
    }
    
    /* Subtitle styling */
    h3 {
        color: rgba(255,255,255,0.9);
        text-align: center;
        font-weight: 400 !important;
        font-size: 1.3rem !important;
        margin-top: 0.5rem !important;
    }
    
    /* Section headers */
    .stMarkdown h4 {
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(255,255,255,0.3);
    }
    
    /* Input containers */
    .stSlider, .stSelectbox, .stNumberInput {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        margin-bottom: 0.5rem;
    }
    
    /* Labels */
    label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        border: none;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
        transition: all 0.3s ease;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6);
    }
    
    /* Result cards */
    .stAlert {
        border-radius: 12px;
        backdrop-filter: blur(10px);
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: white;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255,255,255,0.8);
        font-size: 1rem;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.3), transparent);
    }
    
    /* Caption */
    .stCaption {
        text-align: center;
        color: rgba(255,255,255,0.6);
        font-size: 0.9rem;
    }
    
    /* Card styling */
    div[data-testid="column"] {
        background: rgba(255,255,255,0.05);
        padding: 1.5rem;
        border-radius: 16px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Risk factor bullets */
    .risk-factor {
        background: rgba(255,255,255,0.1);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.3rem 0;
        color: white;
        border-left: 3px solid #f5576c;
    }
</style>
""", unsafe_allow_html=True)

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

# Header
st.markdown("<h1>ClassIQ</h1>", unsafe_allow_html=True)
st.markdown("<h3>AI-Powered Student Attendance Prediction System</h3>",
            unsafe_allow_html=True)
st.markdown("---")

# Input Section
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Academic Information")
    hours_studied = st.slider("Hours Studied per Week", 0, 40, 10, key="hours")
    attendance = st.slider("Attendance (%)", 0, 100, 60, key="att")
    previous_scores = st.slider(
        "Previous Exam Scores", 0, 100, 55, key="scores")
    tutoring_sessions = st.number_input(
        "Tutoring Sessions per Week", 0, 10, 0, key="tutor")
    sleep_hours = st.slider("Sleep Hours per Day", 3, 12, 5, key="sleep")
    physical_activity = st.slider(
        "Physical Activity (hours/week)", 0, 20, 1, key="activity")

with col2:
    st.markdown("#### Student Profile")
    parental_involvement = st.selectbox(
        "Parental Involvement", ["Low", "Medium", "High"], key="parent")
    access_to_resources = st.selectbox(
        "Access to Resources", ["Low", "Medium", "High"], key="resources")
    motivation_level = st.selectbox(
        "Motivation Level", ["Low", "Medium", "High"], key="motivation")
    family_income = st.selectbox(
        "Family Income", ["Low", "Medium", "High"], key="income")
    teacher_quality = st.selectbox(
        "Teacher Quality", ["Low", "Medium", "High"], key="teacher")
    parental_education = st.selectbox("Parental Education Level", [
                                      "High School", "College", "Postgraduate"], key="education")

col3, col4 = st.columns(2)

with col3:
    st.markdown("#### School & Environment")
    school_type = st.selectbox(
        "School Type", ["Public", "Private"], key="school")
    peer_influence = st.selectbox(
        "Peer Influence", ["Negative", "Neutral", "Positive"], key="peer")
    distance_from_home = st.selectbox(
        "Distance from Home", ["Near", "Moderate", "Far"], key="distance")

with col4:
    st.markdown("#### Additional Factors")
    extracurricular = st.selectbox("Extracurricular Activities", [
                                   "No", "Yes"], key="extra")
    internet_access = st.selectbox(
        "Internet Access", ["No", "Yes"], key="internet")
    learning_disabilities = st.selectbox(
        "Learning Disabilities", ["No", "Yes"], key="learning")
    gender = st.selectbox("Gender", ["Female", "Male"], key="gender")

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

    # Results Section
    st.markdown("### PREDICTION RESULT")
    st.markdown("")

    col_res1, col_res2, col_res3 = st.columns([2, 1, 1])

    with col_res1:
        if pred == 1:
            st.error("**RECOMMENDATION: SKIP**")
            st.warning(
                "High risk of poor performance. Intervention recommended.")
        else:
            st.success("**RECOMMENDATION: ATTEND**")
            st.info("Likely to perform well. Maintain support.")

    with col_res2:
        st.metric("Confidence", f"{prob * 100:.1f}%")

    with col_res3:
        st.metric("Risk Score", f"{student['risk_score']} / 8")

    st.markdown("---")
    st.markdown("### Risk Factors Breakdown")

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
            st.markdown(
                f'<div class="risk-factor">{factor}</div>', unsafe_allow_html=True)
    else:
        st.success("No major risk factors detected")

    if student["risk_score"] >= 5:
        st.error("**High Risk Alert**: Immediate intervention recommended.")

st.markdown("---")
st.caption("ClassIQ - AI-Powered Student Attendance Prediction System")
