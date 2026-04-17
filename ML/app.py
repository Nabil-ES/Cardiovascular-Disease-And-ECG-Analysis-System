import streamlit as st
import time
import glob
import os

from cardio_prediction import show_cardio_prediction

st.set_page_config(
    page_title="Cardio & ECG Predictor",
    page_icon="❤️",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = "Welcome"

st.markdown("""
<style>
[data-testid="stHeader"] { display: none; }
[data-testid="stFooter"] { display: none; }
.block-container { padding: 2rem 4rem; max-width: 100%; }

.stApp {
    background: radial-gradient(circle at top left, #0f2027, #203a43, #141e30);
    color: white;
}

[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.08);
    z-index: 1;
}
[data-testid="collapsedControl"] { z-index: 9999 !important; }

[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    border-radius: 40px;
    background: linear-gradient(45deg, #00f5a0, #00d9f5);
    color: black;
    font-weight: 600;
    padding: 12px;
    margin-bottom: 12px;
    transition: 0.3s ease;
    white-space: normal;
    text-align: center;
    line-height: 1.2em;
}
[data-testid="stSidebar"] .stButton > button:hover {
    box-shadow: 0 0 25px #00f5a0;
    transform: scale(1.05);
}

.custom-navbar {
    padding: 20px 40px;
    background: rgba(255,255,255,0.05);
    border-bottom: 1px solid rgba(255,255,255,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}
.brand {
    font-size: 24px;
    font-weight: 700;
    background: linear-gradient(90deg, #00f5a0, #00d9f5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.footer {
    text-align: center;
    padding: 20px;
    opacity: 0.6;
    font-size: 14px;
}

.glass-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 25px;
    transition: 0.3s ease;
    height: 100%;
}
.glass-card:hover { transform: translateY(-6px); box-shadow: 0 0 25px rgba(0,245,160,0.4); }
.card-title { font-size: 20px; font-weight: 800; margin-bottom: 15px; color: #00f5a0; }

.title-card {
    background: linear-gradient(135deg, #0f2027, #203a43);
    border-radius: 25px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 0 35px rgba(0,245,160,0.3);
    margin-bottom: 20px;
}
.title-card h2 { margin:0; font-size:30px; color:#00f5a0; }
.title-card p  { margin-top:8px; font-size:18px; opacity:0.85; }

.cardio-card {
    background: rgba(0,0,0,0.35);
    backdrop-filter: blur(12px);
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.1);
    padding: 25px;
    margin-top: 20px;
    box-shadow: 0 0 25px rgba(0,245,160,0.2);
    color: white;
}

.result-success, .result-danger {
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    margin-top: 20px;
    font-size: 20px;
    font-weight: 700;
}
.result-success { border:1px solid #00f5a0; color:#00f5a0; box-shadow:0 0 25px rgba(0,245,160,0.6); }
.result-danger  { border:1px solid #ff4b4b; color:#ff4b4b; box-shadow:0 0 25px rgba(255,75,75,0.6); }

.glow-success { border:1px solid #00f5a0; color:#00f5a0; animation: glowGreen 1.5s infinite alternate; }
.glow-danger  { border:1px solid #ff4b4b; color:#ff4b4b; animation: glowRed 1.5s infinite alternate; }

@keyframes glowGreen { from { box-shadow: 0 0 10px #00f5a0; } to { box-shadow: 0 0 30px #00f5a0; } }
@keyframes glowRed   { from { box-shadow: 0 0 10px #ff4b4b; } to { box-shadow: 0 0 30px #ff4b4b; } }

.stButton > button {
    background: linear-gradient(45deg, #00f5a0, #00d9f5);
    border: none;
    padding: 12px 25px;
    border-radius: 40px;
    font-weight: 600;
    color: black;
    transition: 0.3s ease;
    margin: 5px;
}
.stButton > button:hover { box-shadow: 0 0 20px #00f5a0; transform: scale(1.05); }

.glow-circle {
    position: fixed;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(0,245,160,0.4), transparent 70%);
    border-radius: 50%;
    filter: blur(80px);
    z-index: 0;
}
.circle1 { top:10%; left:5%; }
.circle2 { bottom:10%; right:10%; }

.section-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 25px;
    transition: 0.3s ease;
}
.section-card:hover { box-shadow: 0 0 20px rgba(0,217,245,0.3); transform: translateY(-4px); }
.section-title { font-size:22px; font-weight:700; margin-bottom:15px; color:#00f5a0; }

.thank-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 25px;
    padding: 40px;
    text-align: center;
    margin-bottom: 30px;
    transition: 0.4s ease;
}
.thank-card:hover { box-shadow: 0 0 30px rgba(0,245,160,0.4); transform: translateY(-6px); }
.thank-title {
    font-size:34px; font-weight:800;
    background: linear-gradient(90deg, #00f5a0, #00d9f5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="custom-navbar">
    <div class="brand">❤️ Cardio AI Dashboard</div>
    <div style="opacity:0.7;">AI-Powered Healthcare Intelligence</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🚀 Navigation")
    if st.button("🏠 Home",              key="nav_home"):   st.session_state.page = "Welcome";           st.rerun()
    if st.button("❤️ Cardio Prediction", key="nav_cardio"): st.session_state.page = "Cardio Prediction"; st.rerun()
    if st.button("🫀 ECG Prediction",    key="nav_ecg"):    st.session_state.page = "ECG Prediction";    st.rerun()
    if st.button("🚪 Exit",              key="nav_exit"):   st.session_state.page = "Exit";              st.rerun()


def show_welcome():
    st.markdown('<div class="glow-circle circle1"></div>', unsafe_allow_html=True)
    st.markdown('<div class="glow-circle circle2"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="hero" style="text-align:center; padding:40px 20px 20px 20px;">
        <h1 style="font-size:52px; font-weight:900; background:linear-gradient(90deg,#00f5a0,#00d9f5);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;">❤️ Cardio AI System</h1>
        <div style="font-size:24px; font-weight:700; background:linear-gradient(90deg,#00d9f5,#00f5a0);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            Next-Generation Cardiovascular &amp; ECG Risk Intelligence<br>
            Powered by Advanced Machine Learning
        </div>
    </div>
    """, unsafe_allow_html=True)

    sp1, col1, col2, sp2 = st.columns([2, 2, 2, 2])
    with col1:
        if st.button("❤️ Cardio Prediction", key="welcome_cardio"):
            st.session_state.page = "Cardio Prediction"
            st.rerun()
    with col2:
        if st.button("🧠 ECG Prediction", key="welcome_ecg"):
            st.session_state.page = "ECG Prediction"
            st.rerun()

    st.markdown('<div style="text-align:center; font-size:30px; font-weight:800; margin:50px 0 30px 0;">🚀 AI Engines Powering The Platform</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="glass-card">
            <div class="card-title">🌲 Random Forest</div>
            <ul><li>Ensemble-based prediction model</li><li>High stability on medical datasets</li>
            <li>Reduces overfitting effectively</li><li>Identifies critical health indicators</li></ul>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="glass-card">
            <div class="card-title">⚡ XGBoost</div>
            <ul><li>Gradient boosting optimization</li><li>Sequential error minimization</li>
            <li>Built-in regularization</li><li>High-performance structured data model</li></ul>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="glass-card">
            <div class="card-title">🧠 ResNet50</div>
            <ul><li>50-layer deep convolutional network</li><li>ECG image feature extraction</li>
            <li>Residual learning architecture</li><li>Advanced medical image classification</li></ul>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="text-align:center; margin-top:40px; opacity:0.6; font-size:15px;">Built as a futuristic AI healthcare platform ✨</div>', unsafe_allow_html=True)


def show_ecg_prediction():
    try:
        from ECG import ECG
    except ImportError:
        st.error("ECG module not found. Make sure Ecg.py is in the same directory.")
        return

    st.markdown("""
    <div class="title-card">
        <h2>🫀 ECG Report Analyzer</h2>
        <p>AI Powered ECG Signal Processing &amp; Heart Condition Detection</p>
    </div>
    """, unsafe_allow_html=True)

    ecg = ECG()
    uploaded_file = st.file_uploader("Upload an ECG Image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:

        def show_section(title, content_func, use_columns=True):
            st.markdown(f'''<div class="glass-card" style="margin-bottom:20px;">
                <h4 style="color:#00f5a0; margin-bottom:15px;">{title}</h4>''',
                unsafe_allow_html=True)
            if use_columns:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    content_func()
            else:
                content_func()
            st.markdown('</div>', unsafe_allow_html=True)

        ecg_user_image_read = ecg.getImage(uploaded_file)
        show_section("Uploaded ECG Image",
                     lambda: st.image(ecg_user_image_read, width=500))

        ecg_user_gray_image_read = ecg.GrayImgae(ecg_user_image_read)
        show_section("Gray Scale Conversion",
                     lambda: st.image(ecg_user_gray_image_read, width=500))

        dividing_leads = ecg.DividingLeads(ecg_user_image_read)
        show_section("Dividing Leads", lambda: [
            st.image('Leads_1-12_figure.png', width=500),
            st.image('Long_Lead_13_figure.png', width=500)
        ])

        ecg_preprocessed_leads = ecg.PreprocessingLeads(dividing_leads)
        show_section("Preprocessed Leads", lambda: [
            st.image('Preprossed_Leads_1-12_figure.png', width=500),
            st.image('Preprossed_Leads_13_figure.png', width=500)
        ])

        ecg.SignalExtraction_Scaling(dividing_leads)
        show_section("Contour Leads",
                     lambda: st.image('Contour_Leads_1-12_figure.png', width=500))

        for old_csv in glob.glob('Scaled_1DLead_*.csv'):
            os.remove(old_csv)
        ecg.SignalExtraction_Scaling(dividing_leads)

        ecg_1dsignal = ecg.CombineConvert1Dsignal()
        ecg_final = ecg.DimensionalReduciton(ecg_1dsignal)

        st.markdown('<div class="glass-card" style="margin-bottom:20px;"><h4 style="color:#00f5a0; margin-bottom:5px;">1D Signal</h4>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:rgba(255,255,255,0.5); font-size:13px; margin-bottom:12px;">📊 {ecg_1dsignal.shape[1]} signal points across 12 leads</p>', unsafe_allow_html=True)
        st.dataframe(ecg_1dsignal)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card" style="margin-bottom:20px;"><h4 style="color:#00f5a0; margin-bottom:5px;">Dimensional Reduction</h4>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:rgba(255,255,255,0.5); font-size:13px; margin-bottom:12px;">📉 Reduced to {ecg_final.shape[1]} principal components via PCA</p>', unsafe_allow_html=True)
        st.dataframe(ecg_final)
        st.markdown('</div>', unsafe_allow_html=True)

        ecg_model = ecg.ModelLoad_predict(ecg_final)

        if isinstance(ecg_model, str) and "Normal" in ecg_model:
            st.markdown(f"""<div class="result-success">
                <h3>ECG Analysis Result</h3><p>{ecg_model}</p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="result-danger">
                <h3>ECG Analysis Result</h3><p>{ecg_model}</p>
            </div>""", unsafe_allow_html=True)


def show_exit():
    st.markdown("""
    <div class="thank-card">
        <div class="thank-title">❤️ Thank You for Using Cardio AI</div>
        <p style="margin-top:15px; font-size:18px; opacity:0.8;">
            You've successfully exited the system.
            Taking action today leads to a healthier tomorrow.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card">
        <div class="section-title">💡 Heart-Healthy Tips</div>
        <ul>
            <li>🥦 Maintain a balanced diet rich in nutrients</li>
            <li>🚶 Exercise at least 30 minutes daily</li>
            <li>💧 Stay hydrated consistently</li>
            <li>😴 Ensure 7–9 hours of quality sleep</li>
            <li>🏥 Schedule regular medical check-ups</li>
        </ul>
    </div>
    <div class="section-card">
        <div class="section-title">📢 Stay Connected</div>
        <p style="opacity:0.8;">🔗 Website: www.hearthealthcare.com<br>📩 Email: support@hearthealthcare.com</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Back to Home", key="exit_home"):
            st.session_state.page = "Welcome"; st.rerun()
    with col2:
        if st.button("❤️ Cardio Prediction", key="exit_cardio"):
            st.session_state.page = "Cardio Prediction"; st.rerun()
    with col3:
        if st.button("🫀 ECG Prediction", key="exit_ecg"):
            st.session_state.page = "ECG Prediction"; st.rerun()

    st.markdown('<div style="text-align:center; margin-top:30px; font-size:18px; opacity:0.8;">💖 Stay Healthy • Stay Safe • Protect Your Heart</div>', unsafe_allow_html=True)


# ── Router ─────────────────────────────────────────────────────────
page = st.session_state.page

if   page == "Welcome":           show_welcome()
elif page == "Cardio Prediction": show_cardio_prediction()
elif page == "ECG Prediction":    show_ECG()
elif page == "Exit":              show_exit()

st.markdown("""
<div class="footer">
© 2026 Cardio AI | Next-Generation AI Healthcare System ✨
</div>
""", unsafe_allow_html=True)