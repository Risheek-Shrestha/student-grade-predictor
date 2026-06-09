import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load('student_model.pkl')

# Page Config
st.set_page_config(
    page_title="Student Grade Predictor",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Student Grade Predictor")
st.write("Predict the Final Grade (G3) using academic and student-related factors.")

st.divider()

# Inputs

g2 = st.slider(
    "G2 (Second Period Grade)",
    min_value=0,
    max_value=20,
    value=10
)

g1 = st.slider(
    "G1 (First Period Grade)",
    min_value=0,
    max_value=20,
    value=10
)

failures = st.selectbox(
    "Number of Past Failures",
    [0, 1, 2, 3, 4]
)

studytime = st.selectbox(
    "Study Time",
    [1, 2, 3, 4],
    help="""
1 = Less than 2 hours/week
2 = 2-5 hours/week
3 = 5-10 hours/week
4 = More than 10 hours/week
"""
)

medu = st.selectbox(
    "Mother's Education",
    [0, 1, 2, 3, 4],
    help="""
0 = None
1 = Primary Education
2 = 5th to 9th Grade
3 = Secondary Education
4 = Higher Education
"""
)

fedu = st.selectbox(
    "Father's Education",
    [0, 1, 2, 3, 4],
    help="""
0 = None
1 = Primary Education
2 = 5th to 9th Grade
3 = Secondary Education
4 = Higher Education
"""
)

st.divider()


if st.button("Predict Final Grade"):

    input_data = np.array([
        [
            g2,
            g1,
            failures,
            studytime,
            medu,
            fedu
        ]
    ])

    prediction = model.predict(input_data)[0]

    st.success(
        f"Predicted Final Grade (G3): {prediction:.2f}"
    )

    if prediction >= 16:
        st.balloons()
        st.info("Excellent predicted performance.")
    elif prediction >= 12:
        st.info("Good predicted performance.")
    elif prediction >= 8:
        st.warning("Average predicted performance.")
    else:
        st.error("Low predicted performance. Additional study effort may be required.")