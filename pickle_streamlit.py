import streamlit as st
import plotly.graph_objects as go
import joblib
import pandas as pd



st.set_page_config(page_title="Placement & Salary Prediction", layout="wide")

classifier = joblib.load('classifier.pkl')
regressor = joblib.load('regressor.pkl')



def make_prediction(features):
    df = pd.DataFrame([features])
    placement = classifier.predict(df)[0]
    
    if placement == 0:
        return {"placement_prediction": 0, "salary_prediction": None}
    salary = regressor.predict(df)[0]

    return {"placement_prediction": 1, "salary_prediction": float(salary)}



st.sidebar.title("Student Input")

with st.sidebar.expander("📊 Academic & Profile", expanded=True):
    gender = st.selectbox("Gender", ["Male", "Female"], index=0)
    cgpa = st.number_input("CGPA", 0.0, 10.0, 8.0)
    backlogs = st.number_input("Backlogs", 0, None, 0)
    degree_percentage = st.number_input("Degree Percentage", 0, 100, 80)
    hsc_percentage = st.number_input("HSC Percentage", 0, 100, 80)
    ssc_percentage = st.number_input("SSC Percentage", 0, 100, 80)
    entrance_exam_score = st.number_input("Entrance Exam Score", 0, 100, 80)
    attendance_percentage = st.number_input("Attendance Percentage", 0, 100, 80)

with st.sidebar.expander("💼 Skills & Experience", expanded=True):
    extracurricular_activities = st.selectbox("Extracurricular Activities", ["Yes", "No"], index=0)
    work_experience_months = st.number_input("Work Experience (Months)", 0, None, 0)
    soft_skill_score = st.number_input("Soft Skill Score", 0, 100, 80)
    technical_skill_score = st.number_input("Technical Skill Score", 0, 100, 80)
    internship_count = st.number_input("Internship Count", 0, None, 0)
    live_projects = st.number_input("Live Projects", 0, None, 0)
    certifications = st.number_input("Certifications", 0, None, 0)

predict_clicked = st.sidebar.button("🔮 Predict Placement & Salary", width = 'stretch')

st.title("Placement & Salary Prediction Dashboard")
st.divider()



col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

with col1:
    st.caption("CGPA")
    st.markdown(f"## {cgpa:.2f}")

with col2:
    st.caption("Gender")
    icon = "♂️" if gender == "Male" else "♀️"
    st.markdown(f"## {icon} {gender}")

with col3:
    st.caption("Extracurricular")
    icon = "✅" if extracurricular_activities == "Yes" else "❌"
    st.markdown(f"## {icon} {extracurricular_activities}")

with col4:
    st.caption("Work Experience")
    st.markdown(f"## {work_experience_months} months")

with col5:
    st.caption("Backlogs")
    if backlogs > 0:
        st.markdown(f"## :red[⚠️ {backlogs}]")
    else:
        st.markdown(f"## ✅ {backlogs}")

st.divider()



left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown("**Academic Profile**")
    web = go.Figure(
        data = go.Scatterpolar(
            r = [ssc_percentage, hsc_percentage, degree_percentage, entrance_exam_score, attendance_percentage],
            theta = ["SSC %", "HSC %", "Degree %", "Entrance", "Attendance %"],
            fill = "toself",
            name = "Student",
            line = dict(color="#4C9AFF")
        ),
        layout = dict(
            polar = dict(radialaxis=dict(visible = True, range = [0, 100])),
            showlegend = False,
            height = 300,
            margin = dict(l = 20, r = 20, t = 20, b = 20)
        )
    )
    st.plotly_chart(web, width = 'stretch')

with right_col:
    st.markdown("**Skill Scores**")
    skills = go.Figure(
        data = go.Bar(                          
            x = [technical_skill_score, soft_skill_score],
            y = ["Technical Skill", "Soft Skill"],
            orientation = "h",
            marker = dict(color = ["#4C9AFF", "#F6AD55"]),
            text = [technical_skill_score, soft_skill_score],
            textposition = "outside"
        ),
        layout = dict(                          
            xaxis = dict(range = [0, 100], title="Score"),
            height = 150,
            margin = dict(l=20, r=20, t=20, b=20)
        )
    )
    st.plotly_chart(skills, width = 'stretch')

    st.markdown("**Experience Counts**")
    experience1 = go.Figure(
        data = go.Bar(
            x = ["Internships", "Projects", "Certifications"],
            y = [internship_count, live_projects, certifications],
            name = "Count",
            marker = dict(color="#38B2AC")
        ),
        layout = dict(
            yaxis = dict(title = "Count"),
            height = 150,
            margin = dict(l=20, r=20, t=20, b=20),
        )
    )
    st.plotly_chart(experience1, width = 'stretch')

st.divider()

st.subheader("Prediction Result")



if predict_clicked:
    features = {
        "backlogs": int(backlogs),
        "cgpa": float(cgpa),
        "technical_skill_score": int(technical_skill_score),
        "soft_skill_score": int(soft_skill_score),
        "ssc_percentage": int(ssc_percentage),
        "hsc_percentage": int(hsc_percentage),
        "degree_percentage": int(degree_percentage),
        "entrance_exam_score": int(entrance_exam_score),
        "internship_count": int(internship_count),
        "live_projects": int(live_projects),
        "work_experience_months": int(work_experience_months),
        "certifications": int(certifications),
        "attendance_percentage": int(attendance_percentage),
        "gender": gender,
        "extracurricular_activities": extracurricular_activities
    }

    result = make_prediction(features)

    if result is not None:
        placement = result.get("placement_prediction")
        salary = result.get("salary_prediction")

        # p1_col, p2_col = st.columns(2)
        # with p1_col:
        if placement == 1:
            st.success(f"### ✅ This student is predicted to get placed\n### 💵 Estimated Salary = {salary:,.2f} LPA")
            # st.success(f"### 💵 Estimated Salary\n### {salary:,.2f} LPA")
        else:
            st.error("### ❌ This student is predicted not to get placed\n### 👛 There is no salary estimation (Student predicted as not to get placed)")
                # st.error("### There is no salary estimation\n### Student predicted as not to get placed")
        # with p2_col:
        #     if placement == 1:
        #         st.success(f"### 💵 Estimated Salary\n### {salary:,.2f} LPA")
        #     else:
        #         st.error("### There is no salary estimation\n### Student predicted as not to get placed")
else:
    st.info("Fill in the student data in the sidebar and click predict to see the result.")