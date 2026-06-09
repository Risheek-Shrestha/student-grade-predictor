import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load("student_model.pkl")

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #111827 40%,
        #1f2937 100%
    );
}

.hero-card {
    background: linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );
    padding: 35px;
    border-radius: 25px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
}

.metric-card {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
}

.metric-title {
    font-size: 14px;
    color: #9ca3af;
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div class="hero-card">
    <h1>🎓 Student Performance Analytics</h1>
    <p>
        AI-Powered Final Grade Prediction using Random Forest Regression
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("📋 Student Profile")

g2 = st.sidebar.slider("G2 Grade", 0, 20, 10)
g1 = st.sidebar.slider("G1 Grade", 0, 20, 10)

failures = st.sidebar.selectbox(
    "Previous Failures",
    [0, 1, 2, 3, 4]
)

studytime = st.sidebar.selectbox(
    "Study Time",
    [1, 2, 3, 4]
)

medu = st.sidebar.selectbox(
    "Mother Education",
    [0, 1, 2, 3, 4]
)

fedu = st.sidebar.selectbox(
    "Father Education",
    [0, 1, 2, 3, 4]
)

predict = st.sidebar.button(
    "🚀 Predict Performance",
    use_container_width=True
)

# ==========================================
# PREDICTION
# ==========================================

if predict:

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

    if prediction >= 16:
        grade = "A"
        risk = "LOW 🟢"
        color = "#22c55e"

    elif prediction >= 14:
        grade = "B"
        risk = "LOW 🟢"
        color = "#84cc16"

    elif prediction >= 10:
        grade = "C"
        risk = "MEDIUM 🟡"
        color = "#f59e0b"

    else:
        grade = "D"
        risk = "HIGH 🔴"
        color = "#ef4444"

    # ======================================
    # KPI CARDS
    # ======================================

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
            "Risk Level",
            risk
        )

    st.divider()

    # ======================================
    # CHARTS
    # ======================================

    left, right = st.columns(2)

    with left:

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=float(prediction),
            title={"text": "Predicted Grade"},
            gauge={
                "axis": {"range": [0, 20]},
                "bar": {"color": "#3b82f6"},
                "steps": [
                    {"range": [0, 8], "color": "#7f1d1d"},
                    {"range": [8, 12], "color": "#92400e"},
                    {"range": [12, 16], "color": "#365314"},
                    {"range": [16, 20], "color": "#166534"}
                ]
            }
        ))

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

    with right:

        radar = go.Figure()

        radar.add_trace(
            go.Scatterpolar(
                r=[
                    g1,
                    g2,
                    studytime * 5,
                    (4 - failures) * 5,
                    medu * 5,
                    fedu * 5
                ],
                theta=[
                    "G1",
                    "G2",
                    "Study Time",
                    "Failures",
                    "Mother Edu",
                    "Father Edu"
                ],
                fill="toself"
            )
        )

        radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 20]
                )
            ),
            showlegend=False
        )

        st.plotly_chart(
            radar,
            use_container_width=True
        )

    # ======================================
    # PERFORMANCE BAR
    # ======================================

    st.subheader("📈 Performance Index")

    percentage = min(
        int((prediction / 20) * 100),
        100
    )

    st.progress(percentage)

    st.write(
        f"Estimated Performance: **{percentage}%**"
    )

    # ======================================
    # AI ANALYSIS
    # ======================================

    st.subheader("🧠 AI Analysis")

    if prediction >= 16:

        st.success(
            "The student is predicted to perform exceptionally well in the final examination."
        )

        st.balloons()

    elif prediction >= 10:

        st.warning(
            "The student is expected to achieve average to good academic performance."
        )

    else:

        st.error(
            "The student may require additional academic support and study effort."
        )

# ==========================================
# INFORMATION SECTION
# ==========================================

st.markdown("---")

colA, colB = st.columns(2)

with colA:

    st.subheader("📊 Features Used")

    st.info("""
G2 Grade

G1 Grade

Previous Failures

Study Time

Mother's Education

Father's Education
""")

with colB:

    st.subheader("🤖 Model Information")

    st.info("""
Random Forest Regressor

Target Variable: G3

Features: 6

Evaluation Metrics:
• MAE
• R² Score
""")

st.markdown("---")

st.markdown(
"""
<div style='text-align:center;color:gray'>
Built with Streamlit • Scikit-Learn • Plotly
</div>
""",
unsafe_allow_html=True
)
