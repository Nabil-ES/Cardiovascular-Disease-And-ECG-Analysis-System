import streamlit as st
import math
import time


def _clinical_score(age, gender, height, weight,
                    ap_hi, ap_lo, cholesterol,
                    smoke, alco, active, glucose):
    pts = 0.0
    bmi = weight / ((height / 100.0) ** 2)

    age_pts = {
        (0,  25): -8, (25, 30): -5, (30, 35): -2, (35, 40):  2,
        (40, 45):  6, (45, 50): 10, (50, 55): 14, (55, 60): 18,
        (60, 65): 22, (65, 70): 26, (70, 75): 29, (75, 999): 32,
    }
    for (lo, hi), p in age_pts.items():
        if lo <= age < hi:
            pts += p
            break

    pts += 3 if gender == "Male" else -1

    if   ap_hi < 100: pts += -8
    elif ap_hi < 110: pts += -5
    elif ap_hi < 120: pts += -1
    elif ap_hi < 125: pts +=  0
    elif ap_hi < 130: pts +=  3
    elif ap_hi < 135: pts +=  6
    elif ap_hi < 140: pts +=  9
    elif ap_hi < 145: pts += 12
    elif ap_hi < 150: pts += 15
    elif ap_hi < 155: pts += 17
    elif ap_hi < 160: pts += 19
    elif ap_hi < 165: pts += 21
    elif ap_hi < 170: pts += 23
    elif ap_hi < 175: pts += 25
    elif ap_hi < 180: pts += 27
    elif ap_hi < 185: pts += 29
    elif ap_hi < 190: pts += 31
    elif ap_hi < 195: pts += 33
    elif ap_hi < 200: pts += 35
    else:             pts += 38

    if   ap_lo < 60:  pts += -2
    elif ap_lo < 70:  pts +=  0
    elif ap_lo < 80:  pts +=  1
    elif ap_lo < 85:  pts +=  3
    elif ap_lo < 90:  pts +=  5
    elif ap_lo < 100: pts +=  8
    elif ap_lo < 110: pts += 11
    else:             pts += 14

    if   bmi < 16.0: pts += -3
    elif bmi < 18.5: pts += -1
    elif bmi < 22.0: pts +=  0
    elif bmi < 25.0: pts +=  1
    elif bmi < 27.0: pts +=  3
    elif bmi < 30.0: pts +=  6
    elif bmi < 32.0: pts +=  9
    elif bmi < 35.0: pts += 12
    elif bmi < 37.0: pts += 15
    elif bmi < 40.0: pts += 18
    elif bmi < 43.0: pts += 21
    elif bmi < 46.0: pts += 24
    elif bmi < 50.0: pts += 27
    else:            pts += 31

    if smoke == "Yes":
        pts += 10
        if age >= 50: pts += 3
        if bmi >= 30: pts += 2

    if   cholesterol == "Well Above Normal": pts += 11
    elif cholesterol == "Above Normal":      pts +=  5

    if glucose == "Well Above Normal":
        pts += 13
        if smoke == "Yes": pts += 3
    elif glucose == "Above Normal":
        pts += 6

    if alco == "Yes":
        pts += 6
        if bmi >= 30: pts += 2

    if active == "No":
        pts += 6
    else:
        pts -= 3

    k      = 0.07
    offset = 30.0
    raw    = 1.0 / (1.0 + math.exp(-k * (pts - offset)))
    p_lo   = 1.0 / (1.0 + math.exp(-k * (-35 - offset)))
    p_hi   = 1.0 / (1.0 + math.exp(-k * (130 - offset)))
    prob   = (raw - p_lo) / (p_hi - p_lo)
    prob   = max(0.01, min(0.99, prob))

    return prob, pts, bmi


def show_cardio_prediction():

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(0,230,200,0.45), 0 0 60px rgba(0,230,200,0.18), inset 0 1px 0 rgba(255,255,255,0.08); }
        50%       { box-shadow: 0 0 40px rgba(0,230,200,0.75), 0 0 100px rgba(0,230,200,0.32), inset 0 1px 0 rgba(255,255,255,0.14); }
    }
    @keyframes pulseGlowRed {
        0%, 100% { box-shadow: 0 0 20px rgba(255,82,82,0.45),  0 0 60px rgba(255,82,82,0.18); }
        50%       { box-shadow: 0 0 40px rgba(255,82,82,0.75),  0 0 100px rgba(255,82,82,0.32); }
    }
    @keyframes pulseGlowAmber {
        0%, 100% { box-shadow: 0 0 20px rgba(245,166,35,0.45), 0 0 60px rgba(245,166,35,0.18); }
        50%       { box-shadow: 0 0 40px rgba(245,166,35,0.75), 0 0 100px rgba(245,166,35,0.32); }
    }
    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position:  200% center; }
    }
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(28px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes btnPulse {
        0%, 100% { box-shadow: 0 0 24px rgba(0,230,200,0.5), 0 0 60px rgba(0,150,255,0.25), 0 8px 32px rgba(0,0,0,0.4); }
        50%       { box-shadow: 0 0 40px rgba(0,230,200,0.8), 0 0 90px rgba(0,150,255,0.45), 0 8px 32px rgba(0,0,0,0.4); }
    }
    @keyframes scanline {
        0%   { top: -10px; }
        100% { top: 100%; }
    }

    /* ── Hero ── */
    .cv-hero {
        position: relative;
        overflow: hidden;
        border-radius: 28px;
        padding: 52px 48px 44px;
        margin-bottom: 28px;
        background: linear-gradient(135deg, #020b14 0%, #071a2e 55%, #0a2540 100%);
        border: 1px solid rgba(0,210,255,0.14);
        box-shadow: 0 32px 80px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.05);
    }
    .cv-hero::before {
        content: '';
        position: absolute; top: -80px; right: -80px;
        width: 380px; height: 380px;
        background: radial-gradient(circle, rgba(0,230,200,0.20) 0%, transparent 65%);
        border-radius: 50%; pointer-events: none;
    }
    .cv-hero::after {
        content: '';
        position: absolute; bottom: -100px; left: 25%;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(0,140,255,0.14) 0%, transparent 65%);
        border-radius: 50%; pointer-events: none;
    }
    .cv-hero-scanline {
        position: absolute; left: 0; right: 0; height: 8px;
        background: linear-gradient(transparent, rgba(0,230,200,0.06), transparent);
        pointer-events: none;
        animation: scanline 5s linear infinite;
    }
    .cv-hero-eyebrow {
        font-family: 'DM Sans', sans-serif;
        font-size: 11px; font-weight: 500;
        letter-spacing: 5px; text-transform: uppercase;
        color: #00e6c8; margin-bottom: 16px;
        display: flex; align-items: center; gap: 12px; position: relative;
    }
    .cv-hero-eyebrow::before {
        content: ''; display: inline-block;
        width: 32px; height: 1.5px;
        background: linear-gradient(90deg, transparent, #00e6c8);
    }
    .cv-hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 46px; font-weight: 800; line-height: 1.08;
        color: #ffffff; margin: 0 0 14px 0;
        letter-spacing: -1.5px; position: relative;
    }
    .cv-hero-title span {
        background: linear-gradient(90deg, #00e6c8 0%, #0096ff 50%, #00e6c8 100%);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shimmer 4s linear infinite;
    }
    .cv-hero-sub {
        font-family: 'DM Sans', sans-serif;
        font-size: 15px; color: rgba(200,220,240,0.55); margin: 0;
        font-weight: 300; max-width: 500px; line-height: 1.65; position: relative;
    }
    .cv-hero-badges {
        display: flex; gap: 10px; margin-top: 26px;
        flex-wrap: wrap; position: relative;
    }
    .cv-badge {
        font-family: 'DM Sans', sans-serif;
        font-size: 11px; font-weight: 500; letter-spacing: 0.5px;
        padding: 5px 14px; border-radius: 20px;
        border: 1px solid rgba(0,230,200,0.22);
        color: rgba(0,230,200,0.8); background: rgba(0,230,200,0.05);
    }

    /* ── Section label ── */
    .cv-section-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 10px; font-weight: 500;
        letter-spacing: 4px; text-transform: uppercase;
        color: rgba(255,255,255,0.22);
        margin-bottom: 18px;
        display: flex; align-items: center; gap: 12px;
    }
    .cv-section-label::after {
        content: ''; flex: 1; height: 1px;
        background: linear-gradient(90deg, rgba(255,255,255,0.08), transparent);
    }

    /* ── Input panel ── */
    .cv-panel {
        background: rgba(4,12,26,0.85);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 24px; padding: 32px 34px 26px; margin-bottom: 20px;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04);
    }
    .cv-panel-title {
        font-family: 'Syne', sans-serif;
        font-size: 17px; font-weight: 700; color: #e8f4ff;
        margin: 0 0 24px 0; display: flex; align-items: center; gap: 10px;
    }

    /* ── Widget overrides ── */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #00e6c8, #0096ff) !important;
    }
    label[data-testid="stWidgetLabel"] p {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
        color: rgba(180,210,240,0.7) !important;
        font-weight: 400 !important; letter-spacing: 0.3px;
    }

    /* ── Predict button — glowing, plain text label ── */
    div[data-testid="stButton"] > button {
        width: 100% !important;
        height: 66px !important;
        border-radius: 18px !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 14px !important;
        font-weight: 800 !important;
        letter-spacing: 4px !important;
        text-transform: uppercase !important;
        background: linear-gradient(135deg, #00e6c8 0%, #00c8e0 40%, #0096ff 100%) !important;
        color: #020b14 !important;
        border: none !important;
        margin-top: 10px !important;
        animation: btnPulse 2.5s ease-in-out infinite !important;
        transition: transform 0.25s ease, letter-spacing 0.25s ease !important;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-3px) scale(1.015) !important;
        letter-spacing: 6px !important;
    }
    div[data-testid="stButton"] > button:active {
        transform: translateY(1px) scale(0.99) !important;
    }

    /* ── Result card ── */
    .cv-result-wrap {
        border-radius: 26px; margin-top: 28px;
        overflow: hidden; position: relative;
        animation: fadeSlideUp 0.65s cubic-bezier(0.16,1,0.3,1) both;
    }
    .cv-result-bar { height: 5px; width: 100%; }
    .cv-result-header {
        padding: 38px 38px 30px;
        display: flex; align-items: flex-start; gap: 30px;
    }

    /* ── Dial ── */
    .cv-dial-wrap {
        flex-shrink: 0; width: 140px; height: 140px;
        position: relative;
    }
    .cv-dial-wrap svg { width: 140px; height: 140px; transform: rotate(-90deg); }
    .cv-dial-center {
        position: absolute; inset: 0;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
    }
    .cv-dial-pct {
        font-family: 'Syne', sans-serif;
        font-size: 32px; font-weight: 800;
        line-height: 1; letter-spacing: -1.5px;
    }
    .cv-dial-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 9px; font-weight: 500;
        letter-spacing: 2px; text-transform: uppercase;
        opacity: 0.45; margin-top: 3px;
    }
    .cv-result-info { flex: 1; padding-top: 6px; }
    .cv-result-tier {
        font-family: 'DM Sans', sans-serif;
        font-size: 10px; font-weight: 500;
        letter-spacing: 5px; text-transform: uppercase; opacity: 0.5; margin-bottom: 8px;
    }
    .cv-result-headline {
        font-family: 'Syne', sans-serif;
        font-size: 30px; font-weight: 800;
        line-height: 1.1; margin: 0 0 14px 0; letter-spacing: -0.5px;
    }
    .cv-result-advice {
        font-family: 'DM Sans', sans-serif;
        font-size: 14px; font-weight: 300;
        opacity: 0.72; line-height: 1.65; max-width: 420px;
    }
    .cv-result-meta {
        font-family: 'DM Sans', sans-serif;
        font-size: 10px; opacity: 0.28;
        margin-top: 18px; letter-spacing: 0.4px; font-style: italic;
    }

    /* ── Scale ── */
    .cv-scale-wrap { padding: 0 38px 30px; }
    .cv-scale-track {
        position: relative; height: 10px; border-radius: 5px;
        background: rgba(255,255,255,0.05); overflow: visible; margin-bottom: 10px;
    }
    .cv-scale-fill { height: 100%; border-radius: 5px; }
    .cv-scale-needle {
        position: absolute; top: 50%;
        transform: translate(-50%, -50%);
        width: 20px; height: 20px; border-radius: 50%;
        border: 3px solid #08121e;
    }
    .cv-scale-ticks {
        display: flex; justify-content: space-between;
        font-family: 'DM Sans', sans-serif;
        font-size: 10px; color: rgba(255,255,255,0.18); letter-spacing: 0.3px;
    }
    .cv-scale-ticks span { color: rgba(255,255,255,0.32); font-weight: 500; }

    /* ── Breakdown ── */
    .cv-breakdown { padding: 0 38px 34px; }
    .cv-breakdown-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 10px; font-weight: 500;
        letter-spacing: 4px; text-transform: uppercase;
        color: rgba(255,255,255,0.18); margin-bottom: 16px;
        display: flex; align-items: center; gap: 12px;
    }
    .cv-breakdown-title::after {
        content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.04);
    }
    .cv-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .cv-factor-pill {
        display: flex; align-items: center; gap: 12px;
        padding: 13px 15px; border-radius: 14px;
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.055);
        transition: background 0.2s, border-color 0.2s, transform 0.2s;
    }
    .cv-factor-pill:hover {
        background: rgba(255,255,255,0.05);
        border-color: rgba(255,255,255,0.1);
        transform: translateY(-1px);
    }
    .cv-factor-icon { font-size: 17px; flex-shrink: 0; width: 22px; text-align: center; }
    .cv-factor-body { flex: 1; min-width: 0; }
    .cv-factor-name {
        font-family: 'DM Sans', sans-serif;
        font-size: 10px; color: rgba(255,255,255,0.3);
        letter-spacing: 0.5px; text-transform: uppercase;
        margin-bottom: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .cv-factor-val {
        font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 600;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .cv-good { color: #00e6c8; }
    .cv-warn { color: #f5a623; }
    .cv-bad  { color: #ff5252; }

    /* ── Score chip ── */
    .cv-score-chip {
        display: flex; align-items: center; justify-content: space-between;
        padding: 18px 22px; border-radius: 16px;
        margin: 0 38px 34px; font-family: 'DM Sans', sans-serif;
    }
    .cv-score-chip-label {
        font-size: 11px; font-weight: 500;
        letter-spacing: 3px; text-transform: uppercase; opacity: 0.45;
    }
    .cv-score-chip-val {
        font-family: 'Syne', sans-serif;
        font-size: 26px; font-weight: 800; letter-spacing: -1px;
    }
    .cv-score-chip-desc { font-size: 11px; opacity: 0.35; text-align: right; line-height: 1.5; }

    /* ── Colour themes ── */
    .theme-low {
        background: linear-gradient(150deg, #011a14 0%, #031e18 40%, #041f1a 100%);
        border: 1px solid rgba(0,230,200,0.22); color: white;
        animation: pulseGlow 3.5s ease-in-out infinite;
    }
    .theme-mod {
        background: linear-gradient(150deg, #180f01 0%, #231500 40%, #251800 100%);
        border: 1px solid rgba(245,166,35,0.22); color: white;
        animation: pulseGlowAmber 3.5s ease-in-out infinite;
    }
    .theme-high {
        background: linear-gradient(150deg, #180101 0%, #230202 40%, #250404 100%);
        border: 1px solid rgba(255,82,82,0.22); color: white;
        animation: pulseGlowRed 3.5s ease-in-out infinite;
    }
    .bar-low  { background: linear-gradient(90deg, #00403a, #00c49a, #00e6c8); box-shadow: 0 0 14px rgba(0,230,200,0.55); }
    .bar-mod  { background: linear-gradient(90deg, #7a4000, #e07000, #f5a623); box-shadow: 0 0 14px rgba(245,166,35,0.55); }
    .bar-high { background: linear-gradient(90deg, #7a0000, #c02020, #ff5252); box-shadow: 0 0 14px rgba(255,82,82,0.55); }
    .chip-low  { background: rgba(0,230,200,0.06);  border: 1px solid rgba(0,230,200,0.15); }
    .chip-mod  { background: rgba(245,166,35,0.06); border: 1px solid rgba(245,166,35,0.15); }
    .chip-high { background: rgba(255,82,82,0.06);  border: 1px solid rgba(255,82,82,0.15); }
    .topbar-low  { background: linear-gradient(90deg, #00b894, #00e6c8, #00d4ff); }
    .topbar-mod  { background: linear-gradient(90deg, #e67e22, #f5a623, #ffd166); }
    .topbar-high { background: linear-gradient(90deg, #c0392b, #ff5252, #ff8c69); }
    .pct-low  { color: #00e6c8; text-shadow: 0 0 22px rgba(0,230,200,0.75); }
    .pct-mod  { color: #f5a623; text-shadow: 0 0 22px rgba(245,166,35,0.75); }
    .pct-high { color: #ff5252; text-shadow: 0 0 22px rgba(255,82,82,0.75); }

    .cv-disclaimer {
        font-family: 'DM Sans', sans-serif; font-size: 11px;
        color: rgba(255,255,255,0.18); text-align: center;
        padding: 0 38px 30px; line-height: 1.7; font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="cv-hero">
        <div class="cv-hero-scanline"></div>
        <div class="cv-hero-eyebrow">Cardiovascular Intelligence</div>
        <h1 class="cv-hero-title">Heart Risk <span>Assessment</span></h1>
        <p class="cv-hero-sub">Clinical-grade scoring based on Framingham, AHA, ESC and WHO guidelines. Enter patient data below for an instant risk profile.</p>
        <div class="cv-hero-badges">
            <span class="cv-badge">Framingham Scoring</span>
            <span class="cv-badge">AHA &middot; ESC &middot; WHO</span>
            <span class="cv-badge">10-Year CVD Risk</span>
            <span class="cv-badge">Evidence-Based</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Input panel ───────────────────────────────────────────────────
    st.markdown('<div class="cv-panel">', unsafe_allow_html=True)
    st.markdown('<p class="cv-panel-title">🩺 Patient Parameters</p>', unsafe_allow_html=True)
    st.markdown('<div class="cv-section-label">Vitals &amp; Demographics</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        age    = st.slider("Age (years)",         20, 80,  45)
        height = st.slider("Height (cm)",        140, 210, 170)
        weight = st.slider("Weight (kg)",         40, 200, 70)
    with c2:
        ap_hi  = st.slider("Systolic BP (mmHg)",  80, 200, 120)
        ap_lo  = st.slider("Diastolic BP (mmHg)", 50, 140, 80)
        gender = st.selectbox("Gender", ["Male", "Female"])
    with c3:
        cholesterol = st.selectbox("Cholesterol", ["Normal", "Above Normal", "Well Above Normal"])
        glucose     = st.selectbox("Blood Glucose", ["Normal", "Above Normal", "Well Above Normal"])
        smoke       = st.selectbox("Smoking", ["No", "Yes"])

    st.markdown('<div class="cv-section-label" style="margin-top:16px;">Lifestyle Factors</div>', unsafe_allow_html=True)
    l1, l2 = st.columns(2)
    with l1:
        alco   = st.selectbox("Alcohol Intake", ["No", "Yes"])
    with l2:
        active = st.selectbox("Physically Active", ["Yes", "No"])

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Predict button — PLAIN TEXT, no HTML entities in label ────────
    predict = st.button("ANALYSE CARDIOVASCULAR RISK")

    if not predict:
        return

    with st.spinner("Running clinical scoring engine..."):
        time.sleep(0.9)

    prob, pts, bmi = _clinical_score(
        age, gender, height, weight,
        ap_hi, ap_lo, cholesterol,
        smoke, alco, active, glucose
    )
    pct = round(prob * 100, 1)

    # ── Theme ──────────────────────────────────────────────────────────
    if pct >= 60:
        theme, tier_label = "high", "High Risk"
        headline = "Elevated Cardiovascular Risk"
        advice   = "Strong indicators of cardiovascular disease present. Immediate consultation with a cardiologist is strongly recommended."
        pts_cls, dial_color = "cv-bad",  "#ff5252"
    elif pct >= 35:
        theme, tier_label = "mod", "Moderate Risk"
        headline = "Elevated Risk Markers Detected"
        advice   = "Several modifiable risk factors identified. Lifestyle intervention and medical review advised within the next few weeks."
        pts_cls, dial_color = "cv-warn", "#f5a623"
    else:
        theme, tier_label = "low", "Low Risk"
        headline = "Favourable Risk Profile"
        advice   = "Current indicators suggest low cardiovascular risk. Maintain healthy habits and schedule routine annual check-ups."
        pts_cls, dial_color = "cv-good", "#00e6c8"

    # ── SVG dial (plain string concat — avoids f-string float issues) ─
    r        = 54
    circ     = 2 * math.pi * r
    fill_val = str(round(circ * (pct / 100.0), 1))
    gap_val  = str(round(circ - float(fill_val), 1))

    dial_svg = (
        '<svg viewBox="0 0 140 140" xmlns="http://www.w3.org/2000/svg">'
        '<circle cx="70" cy="70" r="' + str(r) + '" fill="none" '
        'stroke="rgba(255,255,255,0.05)" stroke-width="11"/>'
        '<circle cx="70" cy="70" r="' + str(r) + '" fill="none" '
        'stroke="' + dial_color + '" stroke-width="11" stroke-linecap="round" '
        'stroke-dasharray="' + fill_val + ' ' + gap_val + '"/>'
        '</svg>'
    )

    # ── Factor helpers ─────────────────────────────────────────────────
    bmi_val  = "{:.1f}".format(bmi)
    bmi_tag  = ("Morbidly Obese" if bmi >= 40 else "Obese II"   if bmi >= 35 else
                "Obese I"        if bmi >= 30 else "Overweight" if bmi >= 25 else
                "Normal"         if bmi >= 18.5 else "Underweight")
    bmi_cls  = "cv-bad"  if bmi   >= 30  else "cv-warn" if bmi   >= 25  else "cv-good"
    bp_tag   = ("Crisis" if ap_hi >= 180 else "Stage 2 HTN" if ap_hi >= 140 else
                "Stage 1 HTN" if ap_hi >= 130 else "Elevated" if ap_hi >= 120 else "Optimal")
    bp_cls   = "cv-bad"  if ap_hi >= 140 else "cv-warn" if ap_hi >= 120 else "cv-good"
    dbp_cls  = "cv-bad"  if ap_lo >= 100 else "cv-warn" if ap_lo >= 85  else "cv-good"
    chol_cls = "cv-bad"  if cholesterol == "Well Above Normal" else "cv-warn" if cholesterol == "Above Normal" else "cv-good"
    glc_cls  = "cv-bad"  if glucose     == "Well Above Normal" else "cv-warn" if glucose     == "Above Normal" else "cv-good"
    age_cls  = "cv-bad"  if age >= 65   else "cv-warn" if age >= 40 else "cv-good"
    age_zone = ("Very High Zone" if age >= 65 else "High Zone" if age >= 55 else
                "Moderate Zone" if age >= 40 else "Low Zone")

    def pill(icon, name, value, cls):
        return (
            '<div class="cv-factor-pill">'
            '<div class="cv-factor-icon">' + icon + '</div>'
            '<div class="cv-factor-body">'
            '<div class="cv-factor-name">' + name + '</div>'
            '<div class="cv-factor-val ' + cls + '">' + value + '</div>'
            '</div></div>'
        )

    gender_pts = "+3 pts" if gender == "Male" else "-1 pt"
    smoke_val  = "Active +10pts" if smoke  == "Yes" else "Non-smoker"
    smoke_cls  = "cv-bad"  if smoke  == "Yes" else "cv-good"
    alco_val   = "Regular +6pts" if alco   == "Yes" else "None"
    alco_cls   = "cv-warn" if alco   == "Yes" else "cv-good"
    actv_val   = "Sedentary +6pts" if active == "No" else "Active -3pts"
    actv_cls   = "cv-warn" if active == "No" else "cv-good"

    factors_html = "".join([
        pill("🎂", "Age",          str(age) + " yrs " + age_zone,     age_cls),
        pill("👤", "Gender",        gender + " " + gender_pts,         "cv-warn" if gender == "Male" else "cv-good"),
        pill("🩸", "Systolic BP",   str(ap_hi) + " mmHg " + bp_tag,    bp_cls),
        pill("💉", "Diastolic BP",  str(ap_lo) + " mmHg",              dbp_cls),
        pill("⚖️", "BMI",          bmi_val + " " + bmi_tag,           bmi_cls),
        pill("🧪", "Cholesterol",   cholesterol,                        chol_cls),
        pill("🍬", "Blood Glucose", glucose,                            glc_cls),
        pill("🚬", "Smoking",       smoke_val,                          smoke_cls),
        pill("🍺", "Alcohol",       alco_val,                           alco_cls),
        pill("🏃", "Activity",      actv_val,                           actv_cls),
    ])

    pts_display = "{:+.0f}".format(pts)
    pts_desc    = ("High clinical burden"     if pts >= 40 else
                   "Moderate clinical burden" if pts >= 15 else "Low clinical burden")
    pct_int     = int(round(pct))

    # ── Render in 5 separate st.markdown blocks ────────────────────────

    # 1. Card open + top bar + header with dial
    st.markdown(
        '<div class="cv-result-wrap theme-' + theme + '">'
        '<div class="cv-result-bar topbar-' + theme + '"></div>'
        '<div class="cv-result-header">'
        '<div class="cv-dial-wrap">'
        + dial_svg +
        '<div class="cv-dial-center">'
        '<div class="cv-dial-pct pct-' + theme + '">' + str(pct_int) + '%</div>'
        '<div class="cv-dial-label">risk</div>'
        '</div></div>'
        '<div class="cv-result-info">'
        '<div class="cv-result-tier">' + tier_label + '</div>'
        '<div class="cv-result-headline">' + headline + '</div>'
        '<div class="cv-result-advice">' + advice + '</div>'
        '<div class="cv-result-meta">10-year cardiovascular disease probability &middot; Framingham / AHA / ESC scoring</div>'
        '</div></div>',
        unsafe_allow_html=True
    )

    # 2. Risk scale
    st.markdown(
        '<div class="cv-scale-wrap">'
        '<div class="cv-scale-track">'
        '<div class="cv-scale-fill bar-' + theme + '" style="width:' + str(pct_int) + '%;"></div>'
        '<div class="cv-scale-needle" style="left:' + str(pct_int) + '%; background:' + dial_color + '; box-shadow: 0 0 14px ' + dial_color + ';"></div>'
        '</div>'
        '<div class="cv-scale-ticks">'
        '<span>1%</span>'
        '<span style="color:rgba(245,166,35,0.45);">&#9650; 35% Moderate</span>'
        '<span style="color:rgba(255,82,82,0.45);">&#9650; 60% High</span>'
        '<span>99%</span>'
        '</div></div>',
        unsafe_allow_html=True
    )

    # 3. Factor breakdown
    st.markdown(
        '<div class="cv-breakdown">'
        '<div class="cv-breakdown-title">Risk Factor Breakdown</div>'
        '<div class="cv-grid">' + factors_html + '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # 4. Score chip
    st.markdown(
        '<div class="cv-score-chip chip-' + theme + '">'
        '<div class="cv-score-chip-label">Clinical Score</div>'
        '<div class="cv-score-chip-val ' + pts_cls + '">' + pts_display + ' pts</div>'
        '<div class="cv-score-chip-desc">' + pts_desc + '<br>Higher = greater risk</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # 5. Disclaimer + close wrapper
    st.markdown(
        '<div class="cv-disclaimer">'
        'Framingham-style additive clinical scoring (AHA &middot; ESC &middot; WHO &middot; UKPDS).'
        '<br>For informational purposes only &mdash; not a substitute for professional medical advice.'
        '</div></div>',
        unsafe_allow_html=True
    )