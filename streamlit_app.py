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
    layout="centered"
)

# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load("student_model.pkl")

# ==========================================
# CSS
# ==========================================

st.markdown("""
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ---- Base ---- */
html, body, .stApp {
    background: #0a0f1e !important;
    color: #e2e8f0;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* ---- Hide default padding ---- */
.block-container {
    padding: 2rem 1.5rem 4rem !important;
    max-width: 860px !important;
}

/* ---- Hero ---- */
.hero {
    background: linear-gradient(135deg, #1e3a8a 0%, #4c1d95 100%);
    border-radius: 24px;
    padding: 40px 30px;
    text-align: center;
    margin-bottom: 32px;
    border: 1px solid rgba(99,102,241,0.3);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(99,102,241,0.15) 0%, transparent 60%);
    pointer-events: none;
}

.hero h1 {
    font-size: clamp(1.5rem, 5vw, 2.2rem);
    font-weight: 800;
    color: white;
    margin: 0 0 10px 0;
    letter-spacing: -0.5px;
}

.hero p {
    font-size: clamp(0.85rem, 2.5vw, 1rem);
    color: rgba(255,255,255,0.75);
    margin: 0;
}

.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    color: rgba(255,255,255,0.9);
    margin-bottom: 16px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ---- Section label ---- */
.section-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #6366f1;
    margin: 28px 0 12px 0;
}

/* ---- Input card ---- */
.input-card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
}

.input-card:hover {
    border-color: #374151;
}

/* ---- Predict button ---- */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 16px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.4) !important;
    margin: 8px 0 !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 30px rgba(99,102,241,0.5) !important;
}

/* ---- Result card ---- */
.result-card {
    background: linear-gradient(135deg, #0f172a, #1e1b4b);
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 24px;
    padding: 32px 24px;
    text-align: center;
    margin: 24px 0;
    box-shadow: 0 10px 40px rgba(99,102,241,0.15);
}

.result-grade {
    font-size: clamp(3rem, 12vw, 5rem);
    font-weight: 900;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: 0;
}

.result-label {
    font-size: 0.85rem;
    color: #6b7280;
    margin: 6px 0 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.result-badges {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
}

.badge {
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}

.badge-grade {
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.4);
    color: #a5b4fc;
}

.badge-low { background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.3); color: #4ade80; }
.badge-medium { background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.3); color: #fbbf24; }
.badge-high { background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.3); color: #f87171; }

/* ---- Summary card ---- */
.summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
    margin: 16px 0;
}

.summary-item {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 16px;
    padding: 16px 20px;
}

.summary-item-label {
    font-size: 0.72rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 4px;
}

.summary-item-value {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
}

/* ---- Feedback ---- */
.feedback-box {
    border-radius: 14px;
    padding: 16px 20px;
    font-size: 0.9rem;
    margin: 16px 0;
    line-height: 1.6;
}

.feedback-success {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.25);
    color: #86efac;
}

.feedback-warning {
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.25);
    color: #fde68a;
}

.feedback-error {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.25);
    color: #fca5a5;
}

/* ---- Model stats ---- */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 16px 0;
}

.stat-box {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 16px;
    padding: 18px 12px;
    text-align: center;
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 800;
    color: #818cf8;
}

.stat-label {
    font-size: 0.72rem;
    color: #6b7280;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ---- Slider & select overrides ---- */
.stSlider [data-baseweb="slider"] {
    padding: 8px 0;
}

div[data-baseweb="select"] > div {
    background: #1f2937 !important;
    border-color: #374151 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ---- Footer ---- */
.footer {
    text-align: center;
    padding: 32px 0 8px;
    color: #374151;
    font-size: 0.8rem;
}

.footer a {
    color: #6366f1;
    text-decoration: none;
}

/* ---- Divider ---- */
hr {
    border-color: #1f2937 !important;
    margin: 24px 0 !important;
}

/* ---- Slider label color ---- */
label, .stSlider label, .stSelectbox label {
    color: #9ca3af !important;
    font-size: 0.875rem !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HERO
# ==========================================

st.markdown("""
<div class="hero">
    <div class="hero-badge">🤖 Random Forest · R² 0.83</div>
    <h1>🎓 Student Performance Analytics</h1>
    <p>Enter student details below to predict the final grade using machine learning</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# MODEL STATS
# ==========================================

st.markdown("""
<div class="stats-row">
    <div class="stat-box">
        <div class="stat-value">0.83</div>
        <div class="stat-label">R² Score</div>
    </div>
    <div class="stat-box">
        <div class="stat-value">1.11</div>
        <div class="stat-label">MAE</div>
    </div>
    <div class="stat-box">
        <div class="stat-value">395</div>
        <div class="stat-label">Students</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# INPUT SECTION
# ==========================================

st.markdown('<div class="section-label">📝 Academic Grades</div>', unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        g1 = st.slider("G1 — First Period Grade", 0, 20, 10,
                       help="Student grade in first period (0–20)")
    with col2:
        g2 = st.slider("G2 — Second Period Grade", 0, 20, 10,
                       help="Student grade in second period (0–20)")

st.markdown('<div class="section-label">📚 Study Habits</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    studytime = st.selectbox(
        "Weekly Study Time",
        options=[1, 2, 3, 4],
        format_func=lambda x: {
            1: "1 — Less than 2 hrs/week",
            2: "2 — 2 to 5 hrs/week",
            3: "3 — 5 to 10 hrs/week",
            4: "4 — More than 10 hrs/week"
        }[x]
    )
with col4:
    failures = st.selectbox(
        "Number of Past Failures",
        options=[0, 1, 2, 3, 4],
        format_func=lambda x: f"{x} failure{'s' if x != 1 else ''}"
    )

st.markdown('<div class="section-label">👨‍👩‍👦 Family Background</div>', unsafe_allow_html=True)

col5, col6 = st.columns(2)

edu_labels = {
    0: "0 — No education",
    1: "1 — Primary school",
    2: "2 — Middle school",
    3: "3 — Secondary school",
    4: "4 — Higher education"
}

with col5:
    medu = st.selectbox("Mother's Education", options=[0,1,2,3,4],
                        format_func=lambda x: edu_labels[x])
with col6:
    fedu = st.selectbox("Father's Education", options=[0,1,2,3,4],
                        format_func=lambda x: edu_labels[x])

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# PREDICT BUTTON
# ==========================================

predict = st.button("🚀 Predict Final Grade")

# ==========================================
# RESULTS
# ==========================================

if predict:

    input_data = np.array([[g2, g1, failures, studytime, medu, fedu]])
    prediction = round(float(model.predict(input_data)[0]), 2)
    percentage = min(int((prediction / 20) * 100), 100)

    # Grade classification
    if prediction >= 16:
        grade_letter = "A"
        risk_label = "Low Risk"
        risk_class = "badge-low"
        feedback_class = "feedback-success"
        feedback_msg = "🎉 Excellent! This student is predicted to perform exceptionally well. Keep up the great work and maintain consistency heading into the final exam."
        show_balloons = True
    elif prediction >= 14:
        grade_letter = "B"
        risk_label = "Low Risk"
        risk_class = "badge-low"
        feedback_class = "feedback-success"
        feedback_msg = "✅ Good performance predicted. The student shows strong academic ability. A little extra revision could push this to an A."
        show_balloons = False
    elif prediction >= 10:
        grade_letter = "C"
        risk_label = "Medium Risk"
        risk_class = "badge-medium"
        feedback_class = "feedback-warning"
        feedback_msg = "⚠️ Average performance predicted. The student would benefit from increasing study time and addressing any gaps from G1 and G2."
        show_balloons = False
    else:
        grade_letter = "D"
        risk_label = "High Risk"
        risk_class = "badge-high"
        feedback_class = "feedback-error"
        feedback_msg = "🚨 Low performance predicted. Immediate academic support is recommended. Focus on reducing absences and addressing past failures."
        show_balloons = False

    # Result card
    st.markdown(f"""
    <div class="result-card">
        <p class="result-grade">{prediction}</p>
        <p class="result-label">Predicted Final Grade (G3) out of 20</p>
        <div class="result-badges">
            <span class="badge badge-grade">Grade {grade_letter}</span>
            <span class="badge {risk_class}">{risk_label}</span>
            <span class="badge badge-grade">{percentage}% Performance</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feedback
    st.markdown(f"""
    <div class="feedback-box {feedback_class}">
        {feedback_msg}
    </div>
    """, unsafe_allow_html=True)

    if show_balloons:
        st.balloons()

    # Charts
    st.markdown('<div class="section-label">📊 Visual Analysis</div>', unsafe_allow_html=True)

    chart_left, chart_right = st.columns([1, 1])

    with chart_left:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction,
            title={"text": "Grade Score", "font": {"color": "#9ca3af", "size": 14}},
            number={"font": {"color": "white", "size": 36}},
            gauge={
                "axis": {"range": [0, 20], "tickcolor": "#374151",
                         "tickfont": {"color": "#6b7280"}},
                "bar": {"color": "#6366f1", "thickness": 0.3},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 8],  "color": "#450a0a"},
                    {"range": [8, 12], "color": "#431407"},
                    {"range": [12, 16], "color": "#14532d"},
                    {"range": [16, 20], "color": "#166534"}
                ],
                "threshold": {
                    "line": {"color": "#818cf8", "width": 3},
                    "thickness": 0.8,
                    "value": prediction
                }
            }
        ))

        gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"},
            height=260,
            margin=dict(t=40, b=20, l=30, r=30)
        )

        st.plotly_chart(gauge, use_container_width=True)

    with chart_right:
        radar = go.Figure()
        radar.add_trace(go.Scatterpolar(
            r=[g1, g2, studytime * 5, max((4 - failures) * 5, 0), medu * 5, fedu * 5],
            theta=["G1", "G2", "Study Time", "No Failures", "Mother Edu", "Father Edu"],
            fill="toself",
            fillcolor="rgba(99,102,241,0.2)",
            line=dict(color="#818cf8", width=2),
        ))

        radar.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True, range=[0, 20],
                    tickcolor="#374151",
                    gridcolor="rgba(255,255,255,0.08)",
                    tickfont={"color": "#6b7280", "size": 9}
                ),
                angularaxis=dict(
                    tickcolor="#374151",
                    gridcolor="rgba(255,255,255,0.08)",
                    tickfont={"color": "#9ca3af", "size": 11}
                )
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"},
            showlegend=False,
            height=260,
            margin=dict(t=30, b=30, l=40, r=40)
        )

        st.plotly_chart(radar, use_container_width=True)

    # Input Summary
    st.markdown('<div class="section-label">📋 Input Summary</div>', unsafe_allow_html=True)

    study_map = {1: "<2 hrs/week", 2: "2–5 hrs/week", 3: "5–10 hrs/week", 4: ">10 hrs/week"}
    edu_map = {0: "None", 1: "Primary", 2: "Middle School", 3: "Secondary", 4: "Higher Education"}

    st.markdown(f"""
    <div class="summary-grid">
        <div class="summary-item">
            <div class="summary-item-label">First Period Grade</div>
            <div class="summary-item-value">{g1} / 20</div>
        </div>
        <div class="summary-item">
            <div class="summary-item-label">Second Period Grade</div>
            <div class="summary-item-value">{g2} / 20</div>
        </div>
        <div class="summary-item">
            <div class="summary-item-label">Study Time</div>
            <div class="summary-item-value">{study_map[studytime]}</div>
        </div>
        <div class="summary-item">
            <div class="summary-item-label">Past Failures</div>
            <div class="summary-item-value">{failures}</div>
        </div>
        <div class="summary-item">
            <div class="summary-item-label">Mother's Education</div>
            <div class="summary-item-value">{edu_map[medu]}</div>
        </div>
        <div class="summary-item">
            <div class="summary-item-label">Father's Education</div>
            <div class="summary-item-value">{edu_map[fedu]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")
st.markdown("""
<div class="footer">
    Built by <strong style="color:#818cf8">Risheek Shrestha</strong> &nbsp;·&nbsp;
    Streamlit &nbsp;·&nbsp; Scikit-Learn &nbsp;·&nbsp; Plotly &nbsp;·&nbsp;
    <a href="https://github.com/Risheek-Shrestha/student-price-predictor" target="_blank">
        GitHub ↗
    </a>
</div>
""", unsafe_allow_html=True)