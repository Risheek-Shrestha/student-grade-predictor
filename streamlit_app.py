import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Student Grade Predictor",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.main-title{
    text-align:center;
    font-size:3rem;
    font-weight:bold;
    color:#4CAF50;
}
.sub-title{
    text-align:center;
    font-size:1.1rem;
    color:gray;
    margin-bottom:30px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("student_model.pkl")

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="main-title">🎓 Student Grade Predictor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Predict the final student grade (G3) using Machine Learning</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("📋 Student Information")

g2 = st.sidebar.slider(
    "G2 (Second Period Grade)",
    0, 20, 10
)

g1 = st.sidebar.slider(
    "G1 (First Period Grade)",
    0, 20, 10
)

failures = st.sidebar.selectbox(
    "Number of Past Failures",
    [0, 1, 2, 3, 4]
)

studytime = st.sidebar.selectbox(
    "Study Time",
    [1, 2, 3, 4],
    help="""
1 = Less than 2 hrs/week
2 = 2–5 hrs/week
3 = 5–10 hrs/week
4 = More than 10 hrs/week
"""
)

medu = st.sidebar.selectbox(
    "Mother's Education",
    [0, 1, 2, 3, 4]
)

fedu = st.sidebar.selectbox(
    "Father's Education",
    [0, 1, 2, 3, 4]
)

predict_btn = st.sidebar.button("🚀 Predict Grade")

# -----------------------------
# Main Area
# -----------------------------
if predict_btn:

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

    # Grade Category
    if prediction >= 16:
        grade = "A"
        remark = "Excellent Performance"
    elif prediction >= 14:
        grade = "B"
        remark = "Very Good Performance"
    elif prediction >= 10:
        grade = "C"
        remark = "Average Performance"
    else:
        grade = "D"
        remark = "Needs Improvement"

    # -----------------------------
    # Top Metrics
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Predicted Grade",
            f"{prediction:.2f}/20"
        )

    with col2:
        st.metric(
            "Grade Category",
            grade
        )

    with col3:
        st.metric(
            "Performance",
            remark
        )

    st.divider()

    # -----------------------------
    # Gauge Chart
    # -----------------------------
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(prediction),
        title={'text': "Predicted Final Grade"},
        gauge={
            'axis': {'range': [0, 20]},
            'bar': {'color': "green"},
            'steps': [
                {'range': [0, 8], 'color': "#ffcccc"},
                {'range': [8, 12], 'color': "#fff3cd"},
                {'range': [12, 16], 'color': "#d4edda"},
                {'range': [16, 20], 'color': "#a8e6a3"}
            ]
        }
    ))

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

    if prediction >= 16:
        st.balloons()

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3 = st.tabs(
    ["📊 Features Used", "🤖 About Model", "ℹ️ About Project"]
)

with tab1:

    feature_df = pd.DataFrame({
        "Feature": [
            "G2",
            "G1",
            "Failures",
            "Study Time",
            "Mother Education",
            "Father Education"
        ]
    })

    st.dataframe(
        feature_df,
        use_container_width=True
    )

with tab2:

    st.markdown("""
### Random Forest Regressor

This project uses a Random Forest Regression model to predict
the final grade (G3).

**Features Used**
- G2
- G1
- Failures
- Study Time
- Mother's Education
- Father's Education

**Evaluation Metrics**
- Mean Absolute Error (MAE)
- R² Score

Random Forest was selected because it produced the best prediction performance among the tested models.
""")

with tab3:

    st.markdown("""
### Student Grade Predictor

This machine learning project predicts a student's final academic grade (G3).

### Technologies Used
- Python
- Streamlit
- Scikit-Learn
- Pandas
- NumPy
- Plotly

### Models Tested
- Linear Regression
- K-Nearest Neighbors
- Random Forest Regressor

### Developed By
Risheek Shrestha
""")
