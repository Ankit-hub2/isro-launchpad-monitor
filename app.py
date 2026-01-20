import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime
import time

# Page Config
st.set_page_config(page_title="ISRO Launch Pad Monitoring", page_icon="🛰️", layout="wide")

@st.cache_resource
def load_model():
    model = joblib.load('isro_launchpad_model.pkl')
    feature_cols = joblib.load('feature_cols.pkl')
    return model, feature_cols

model, feature_cols = load_model()

def calculate_health(vib_x, vib_y, vib_z, pressure, strain, temp):
    health = 1.0
    vib_mag = np.sqrt(vib_x**2 + vib_y**2 + vib_z**2)
    
    if vib_mag > 4.0: health -= 0.30
    elif vib_mag > 3.0: health -= 0.20
    elif vib_mag > 2.5: health -= 0.12
    elif vib_mag > 2.0: health -= 0.06
    elif vib_mag > 1.5: health -= 0.02
    
    if pressure < 130: health -= 0.30
    elif pressure < 150: health -= 0.20
    elif pressure < 170: health -= 0.12
    elif pressure < 185: health -= 0.06
    elif pressure < 200: health -= 0.02
    
    if strain > 400: health -= 0.25
    elif strain > 350: health -= 0.18
    elif strain > 300: health -= 0.12
    elif strain > 250: health -= 0.07
    elif strain > 200: health -= 0.03
    
    if temp > 45: health -= 0.15
    elif temp > 42: health -= 0.10
    elif temp > 38: health -= 0.05
    elif temp > 35: health -= 0.02
    
    return max(0.50, min(1.0, health))

# CSS Styling
st.markdown("""
<style>
    .main .block-container {padding: 0 !important; max-width: 100% !important;}
    
    .top-bar {
        background: #00274d;
        color: white;
        padding: 8px 40px;
        font-size: 13px;
        display: flex;
        justify-content: space-between;
    }
    
    .main-header {
        background: linear-gradient(180deg, #003d82 0%, #002855 100%);
        padding: 20px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: white;
    }
    
    .header-left {display: flex; align-items: center; gap: 25px;}
    .isro-logo {width: 75px;}
    .emblem {width: 60px;}
    
    .org-text h1 {
        font-size: 14px;
        font-weight: 600;
        margin: 0;
        line-height: 1.4;
    }
    
    .org-text .sub {
        font-size: 12px;
        opacity: 0.85;
        margin-top: 4px;
    }
    
    .tri-bar {
        height: 4px;
        background: linear-gradient(90deg, #FF9933 0%, #FF9933 33.33%, #FFFFFF 33.33%, #FFFFFF 66.66%, #138808 66.66%);
    }
    
    .nav-bar {
        background: #004d9f;
        padding: 12px 40px;
        display: flex;
        gap: 30px;
    }
    
    .nav-item {
        color: white;
        font-size: 15px;
        padding: 8px 0;
        border-bottom: 2px solid transparent;
    }
    
    .content-area {
        background: #f5f7fa;
        padding: 30px 40px;
        min-height: 70vh;
    }
    
    .page-title {
        background: white;
        border-left: 5px solid #FF9933;
        padding: 25px 30px;
        margin-bottom: 25px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .page-title h2 {
        color: #003d82;
        font-size: 28px;
        font-weight: 700;
        margin: 0 0 8px 0;
    }
    
    .page-title p {
        color: #64748b;
        font-size: 15px;
        margin: 0;
    }
    
    .card {
        background: white;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    .card-header {
        color: #003d82;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 3px solid #FF9933;
    }
    
    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #dc2626;
        color: white;
        padding: 6px 16px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 15px;
    }
    
    .live-dot {
        width: 8px;
        height: 8px;
        background: white;
        border-radius: 50%;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% {opacity: 1;}
        50% {opacity: 0.3;}
    }
    
    .video-container {
        position: relative;
        padding-bottom: 56.25%;
        background: #000;
        margin: 15px 0;
    }
    
    .video-container iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
    
    .countdown {
        background: #0f172a;
        padding: 30px;
        text-align: center;
        margin: 15px 0;
    }
    
    .countdown-label {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 12px;
    }
    
    .countdown-time {
        color: #4ade80;
        font-size: 42px;
        font-weight: 700;
        font-family: monospace;
        letter-spacing: 3px;
    }
    
    .countdown-info {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 15px;
        line-height: 1.6;
    }
    
    .news-item {
        padding: 15px;
        border-left: 4px solid #003d82;
        background: #f8fafc;
        margin-bottom: 12px;
    }
    
    .news-title {
        color: #003d82;
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 6px;
    }
    
    .news-time {
        color: #64748b;
        font-size: 12px;
    }
    
    .health-box {
        background: #f1f5f9;
        border: 2px solid #cbd5e1;
        padding: 30px;
        text-align: center;
        margin: 15px 0;
    }
    
    .health-value {
        font-size: 48px;
        font-weight: 700;
        color: #0f172a;
        font-family: monospace;
        margin: 12px 0;
    }
    
    .health-label {
        font-size: 12px;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .status-box {
        padding: 18px;
        border-left: 5px solid;
        margin: 15px 0;
    }
    
    .status-critical {background: #fef2f2; border-left-color: #dc2626; color: #7f1d1d;}
    .status-warning {background: #fffbeb; border-left-color: #f59e0b; color: #78350f;}
    .status-normal {background: #f0fdf4; border-left-color: #10b981; color: #14532d;}
    
    .status-title {
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 6px;
    }
    
    .stButton > button {
        background: #003d82 !important;
        color: white !important;
        padding: 12px 35px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        width: 100% !important;
    }
    
    .footer {
        background: linear-gradient(180deg, #003d82 0%, #001a3d 100%);
        color: white;
        padding: 35px 40px;
        text-align: center;
        margin-top: 40px;
    }
    
    .footer-title {
        font-size: 19px;
        font-weight: 700;
        margin-bottom: 15px;
        line-height: 1.6;
    }
    
    .footer-text {
        font-size: 14px;
        opacity: 0.9;
        line-height: 1.8;
    }
    
    #MainMenu, footer, .stDeployButton {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class='top-bar'>
    <div>English | हिंदी | Sitemap | Contact Us | Feedback</div>
    <div>A+ A A-</div>
</div>

<div class='main-header'>
    <div class='header-left'>
        <img src='https://www.isro.gov.in/media/image/index.php?img_id=logo_1' class='isro-logo'>
        <div class='org-text'>
            <h1>भारतीय अंतरिक्ष अनुसंधान संगठन, अंतरिक्ष विभाग<br>
            Indian Space Research Organisation, Department of Space</h1>
            <div class='sub'>भारत सरकार / Government of India</div>
        </div>
    </div>
    <img src='https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg' class='emblem'>
</div>

<div class='tri-bar'></div>

<div class='nav-bar'>
    <div class='nav-item'>Home</div>
    <div class='nav-item'>About</div>
    <div class='nav-item'>Missions</div>
    <div class='nav-item'>Launches</div>
    <div class='nav-item'>Centres</div>
    <div class='nav-item'>Monitoring</div>
</div>
""", unsafe_allow_html=True)

# Content
st.markdown("<div class='content-area'>", unsafe_allow_html=True)

st.markdown("""
<div class='page-title'>
    <h2>Launch Pad Structural Health Monitoring System</h2>
    <p>Satish Dhawan Space Centre SHAR, Sriharikota • Real-time Predictive Maintenance Platform</p>
</div>
""", unsafe_allow_html=True)

# Main Layout
col1, col2 = st.columns([2.5, 1.5])

with col1:
    st.markdown("""
    <div class='card'>
        <div class='live-badge'><div class='live-dot'></div>LIVE</div>
        <div class='video-container'>
            <iframe src='https://www.youtube.com/embed/21X5lGlDOfg?autoplay=1&mute=1' frameborder='0' allowfullscreen></iframe>
        </div>
        <div style='margin-top: 12px; color: #64748b; font-size: 14px;'>
            <strong>ISRO Official Live Stream</strong> - Launch Operations & Mission Updates
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='card'>
        <div class='card-header'>Next Launch Countdown</div>
        <div class='countdown'>
            <div class='countdown-label'>PSLV-C62 / EOS-N1 Mission</div>
            <div class='countdown-time'>+00:00:05:570</div>
            <div class='countdown-info'>Launch Vehicle: PSLV-C62<br>Launch Site: First Launch Pad</div>
        </div>
    </div>
    
    <div class='card'>
        <div class='card-header'>Latest Updates</div>
        <div class='news-item'>
            <div class='news-title'>LVM3-M6 mission successfully places BlueBird Block-2 satellite</div>
            <div class='news-time'>2 hours ago</div>
        </div>
        <div class='news-item'>
            <div class='news-title'>ISRO's Aditya-L1 decodes Solar Storm impact</div>
            <div class='news-time'>5 hours ago</div>
        </div>
        <div class='news-item'>
            <div class='news-title'>Overview of PSLV-C62 / EOS-N1 Mission</div>
            <div class='news-time'>1 day ago</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Data Source
st.markdown("<div class='card'><div class='card-header'>Data Source Configuration</div>", unsafe_allow_html=True)
source = st.radio("", ["Live Sensor Feed", "CSV File Upload"], label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

if source == "Live Sensor Feed":
    st.markdown("<div class='card'><div class='card-header'>Sensor Input Parameters</div>", unsafe_allow_html=True)
    
    st.subheader("Vibration Sensors")
    c1, c2, c3 = st.columns(3)
    with c1:
        vx = st.number_input("X-axis (m/s²)", 0.0, 5.0, 0.72, 0.01)
    with c2:
        vy = st.number_input("Y-axis (m/s²)", 0.0, 5.0, 0.68, 0.01)
    with c3:
        vz = st.number_input("Z-axis (m/s²)", 0.0, 4.0, 0.61, 0.01)
    
    st.subheader("Additional Sensors")
    c4, c5, c6 = st.columns(3)
    with c4:
        pr = st.number_input("Pressure (bar)", 120.0, 260.0, 202.0, 1.0)
    with c5:
        st_val = st.number_input("Strain (µε)", 40.0, 450.0, 88.0, 2.0)
    with c6:
        temp = st.number_input("Temp (°C)", 20.0, 50.0, 28.5, 0.1)
    
    health = calculate_health(vx, vy, vz, pr, st_val, temp)
    
    st.markdown(f"""
    <div class='health-box'>
        <div class='health-label'>Component Health Index</div>
        <div class='health-value'>{health:.3f}</div>
        <div class='health-label'>Auto-calculated from sensor data</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'><div class='card-header'>Risk Analysis</div>", unsafe_allow_html=True)
    
    if st.button("Execute Analysis"):
        with st.spinner("Processing..."):
            time.sleep(0.5)
            df = pd.DataFrame({
                'vibration_x_ms2': [vx], 'vibration_y_ms2': [vy], 'vibration_z_ms2': [vz],
                'pressure_bar': [pr], 'strain_microstrain': [st_val], 'temperature_c': [temp],
                'health_state': [health]
            })
            for col in feature_cols:
                if col not in df.columns:
                    df[col] = 0
            
            risk = model.predict_proba(df[feature_cols])[0, 1]
            st.session_state.risk = risk
            st.session_state.time = datetime.now()
    
    if 'risk' in st.session_state:
        risk = st.session_state.risk
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Failure Probability", f"{risk:.2%}")
        with m2:
            st.metric("Health Index", f"{health:.3f}")
        with m3:
            st.metric("Updated", st.session_state.time.strftime('%H:%M:%S'))
        
        if risk >= 0.35:
            st.markdown("<div class='status-box status-critical'><div class='status-title'>CRITICAL ALERT</div>Immediate maintenance required. Launch hold recommended.</div>", unsafe_allow_html=True)
        elif risk >= 0.18:
            st.markdown("<div class='status-box status-warning'><div class='status-title'>ELEVATED RISK</div>Priority inspection within 48 hours.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='status-box status-normal'><div class='status-title'>OPERATIONAL</div>All systems normal. Launch: GO</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("<div class='card'><div class='card-header'>CSV Batch Analysis</div>", unsafe_allow_html=True)
    file = st.file_uploader("Upload CSV", type=['csv'], label_visibility="collapsed")
    
    if file:
        try:
            data = pd.read_csv(file)
            req = ['vibration_x_ms2', 'vibration_y_ms2', 'vibration_z_ms2', 'pressure_bar', 'strain_microstrain', 'temperature_c']
            
            if all(c in data.columns for c in req):
                data['health_state'] = data.apply(
                    lambda r: calculate_health(r['vibration_x_ms2'], r['vibration_y_ms2'], r['vibration_z_ms2'],
                                               r['pressure_bar'], r['strain_microstrain'], r['temperature_c']), axis=1)
                
                for col in feature_cols:
                    if col not in data.columns:
                        data[col] = 0
                
                risks = model.predict_proba(data[feature_cols])[:, 1]
                
                b1, b2, b3, b4 = st.columns(4)
                with b1:
                    st.metric("Total", len(risks))
                with b2:
                    st.metric("Avg Risk", f"{risks.mean():.1%}")
                with b3:
                    st.metric("Critical", (risks > 0.35).sum())
                with b4:
                    st.metric("Safe", (risks <= 0.18).sum())
                
                result = data[req + ['health_state']].copy()
                result['failure_probability'] = risks
                st.dataframe(result, use_container_width=True)
                
                st.download_button("Download Report", result.to_csv(index=False),
                                  f"Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", "text/csv")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# System Info
st.markdown("<div class='card'><div class='card-header'>System Information</div>", unsafe_allow_html=True)
i1, i2, i3 = st.columns(3)
with i1:
    st.markdown("**Model**\n- XGBoost\n- 140K samples\n- 7-day horizon")
with i2:
    st.markdown("**Performance**\n- Precision: 89%\n- Recall: 94%\n- AUC: 0.92")
with i3:
    st.markdown("**Weights**\n- Vibration: 25%\n- Pressure: 20%\n- Strain: 15%")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='tri-bar'></div>
<div class='footer'>
    <div class='footer-title'>भारतीय अंतरिक्ष अनुसंधान संगठन<br>INDIAN SPACE RESEARCH ORGANISATION</div>
    <div class='footer-text'>
        Satish Dhawan Space Centre SHAR • Sriharikota • Andhra Pradesh • 524124<br>
        Launch Pad Health Monitoring System v3.1 • Department of Space • Government of India<br>
        © 2026 ISRO • All Rights Reserved
    </div>
</div>
""", unsafe_allow_html=True)
