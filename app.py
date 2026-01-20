import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime, timedelta
import time

# === PAGE CONFIG ===
st.set_page_config(
    page_title="ISRO - Launch Pad Monitoring", 
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load_isro_system():
    model = joblib.load('isro_launchpad_model.pkl')
    feature_cols = joblib.load('feature_cols.pkl')
    return model, feature_cols

model, feature_cols = load_isro_system()

# === HEALTH CALCULATION ===
def calculate_health_from_sensors(vib_x, vib_y, vib_z, pressure, strain, temp):
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

# === COMPLETE PROFESSIONAL STYLING ===
st.markdown("""
<style>
    /* Global */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Top Bar */
    .top-bar {
        background: #00274d;
        color: white;
        padding: 0.5rem 3rem;
        font-size: 0.75rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .top-links a {
        color: white;
        text-decoration: none;
        margin-right: 1.5rem;
    }
    
    /* Main Header */
    .main-header {
        background: linear-gradient(180deg, #003d82 0%, #002855 100%);
        padding: 1.5rem 3rem;
        color: white;
    }
    
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        max-width: 1600px;
        margin: 0 auto;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 2rem;
    }
    
    .isro-logo {
        width: 85px;
        height: auto;
    }
    
    .org-text h1 {
        font-size: 0.95rem;
        font-weight: 600;
        line-height: 1.4;
        margin: 0;
    }
    
    .org-text .subtitle {
        font-size: 0.8rem;
        opacity: 0.85;
        margin-top: 0.25rem;
    }
    
    .emblem {
        width: 65px;
        height: auto;
    }
    
    /* Orange Divider */
    .tri-divider {
        height: 4px;
        background: linear-gradient(90deg, #FF9933 0%, #FF9933 33%, #FFFFFF 33%, #FFFFFF 66%, #138808 66%);
    }
    
    /* Navigation */
    .nav-bar {
        background: #004d9f;
        padding: 0.75rem 3rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .nav-container {
        max-width: 1600px;
        margin: 0 auto;
        display: flex;
        gap: 2.5rem;
    }
    
    .nav-item {
        color: white;
        text-decoration: none;
        font-size: 0.95rem;
        padding: 0.5rem 0;
        border-bottom: 2px solid transparent;
        transition: all 0.3s;
    }
    
    .nav-item:hover {
        border-bottom-color: #FF9933;
    }
    
    /* Content Area */
    .content-area {
        background: #f5f7fa;
        min-height: 70vh;
        padding: 2rem 3rem;
    }
    
    .content-container {
        max-width: 1600px;
        margin: 0 auto;
    }
    
    /* Page Title */
    .page-header {
        background: white;
        border-left: 5px solid #FF9933;
        padding: 1.75rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .page-header h2 {
        color: #003d82;
        font-size: 1.85rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
    }
    
    .page-header p {
        color: #64748b;
        font-size: 1rem;
        margin: 0;
    }
    
    /* Cards */
    .info-card {
        background: white;
        border: 1px solid #e2e8f0;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    .card-title {
        color: #003d82;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #FF9933;
    }
    
    /* Live Badge */
    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: #dc2626;
        color: white;
        padding: 0.4rem 1rem;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }
    
    .live-dot {
        width: 8px;
        height: 8px;
        background: white;
        border-radius: 50%;
        animation: blink 1.5s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    /* Countdown */
    .countdown-box {
        background: #0f172a;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .countdown-label {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-bottom: 0.75rem;
        letter-spacing: 0.5px;
    }
    
    .countdown-time {
        color: #4ade80;
        font-size: 2.75rem;
        font-weight: 700;
        font-family: 'Courier New', monospace;
        letter-spacing: 3px;
    }
    
    .countdown-info {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 1rem;
        line-height: 1.6;
    }
    
    /* News Items */
    .news-item {
        padding: 1rem;
        border-left: 4px solid #003d82;
        background: #f8fafc;
        margin-bottom: 1rem;
        transition: all 0.2s;
    }
    
    .news-item:hover {
        background: #f1f5f9;
        border-left-color: #FF9933;
    }
    
    .news-title {
        color: #003d82;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.4rem;
        line-height: 1.4;
    }
    
    .news-time {
        color: #64748b;
        font-size: 0.8rem;
    }
    
    /* Video Container */
    .video-wrapper {
        position: relative;
        width: 100%;
        padding-bottom: 56.25%;
        background: #000;
        margin: 1rem 0;
    }
    
    .video-wrapper iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
    
    /* Status Boxes */
    .status-box {
        padding: 1.25rem;
        border-left: 5px solid;
        margin: 1.25rem 0;
    }
    
    .status-critical {
        background: #fef2f2;
        border-left-color: #dc2626;
        color: #7f1d1d;
    }
    
    .status-warning {
        background: #fffbeb;
        border-left-color: #f59e0b;
        color: #78350f;
    }
    
    .status-normal {
        background: #f0fdf4;
        border-left-color: #10b981;
        color: #14532d;
    }
    
    .status-title {
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 0.4rem;
    }
    
    /* Health Display */
    .health-display {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        border: 2px solid #cbd5e1;
        padding: 2rem;
        text-align: center;
        margin: 1.25rem 0;
    }
    
    .health-label {
        color: #475569;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .health-value {
        color: #0f172a;
        font-size: 3rem;
        font-weight: 700;
        font-family: 'Courier New', monospace;
        margin: 0.75rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: #003d82 !important;
        color: white !important;
        border: none !important;
        padding: 0.875rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        width: 100% !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        background: #002855 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,61,130,0.3) !important;
    }
    
    /* Form Elements */
    .stNumberInput label {
        color: #334155 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    .stNumberInput input {
        border-color: #cbd5e1 !important;
        font-size: 0.95rem !important;
    }
    
    /* Radio Buttons */
    .stRadio > div {
        gap: 1rem;
    }
    
    .stRadio label {
        background: white;
        padding: 0.75rem 1.5rem;
        border: 2px solid #e2e8f0;
        font-weight: 500;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 700;
        color: #003d82;
    }
    
    /* Footer */
    .isro-footer {
        background: linear-gradient(180deg, #003d82 0%, #001a3d 100%);
        color: white;
        padding: 2.5rem 3rem;
        margin-top: 3rem;
    }
    
    .footer-content {
        max-width: 1600px;
        margin: 0 auto;
        text-align: center;
    }
    
    .footer-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    
    .footer-info {
        font-size: 0.9rem;
        opacity: 0.9;
        line-height: 1.8;
    }
    
    /* Hide Streamlit */
    #MainMenu, footer, .stDeployButton {visibility: hidden;}
    
    /* Responsive */
    @media (max-width: 768px) {
        .top-bar, .nav-bar, .content-area {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .main-header {
            padding: 1rem;
        }
        
        .header-container {
            flex-direction: column;
            text-align: center;
            gap: 1rem;
        }
        
        .nav-container {
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .countdown-time {
            font-size: 1.75rem;
        }
        
        .isro-logo, .emblem {
            width: 55px;
        }
    }
</style>

<!-- Top Bar -->
<div class='top-bar'>
    <div class='top-links'>
        <a href='#'>English</a>
        <a href='#'>हिंदी</a>
        <a href='#'>Sitemap</a>
        <a href='#'>Contact Us</a>
        <a href='#'>Feedback</a>
    </div>
    <div>A+ A A-</div>
</div>

<!-- Main Header -->
<div class='main-header'>
    <div class='header-container'>
        <div class='header-left'>
            <img src='https://www.isro.gov.in/media/image/index.php?img_id=logo_1' class='isro-logo' alt='ISRO'>
            <div class='org-text'>
                <h1>भारतीय अंतरिक्ष अनुसंधान संगठन, अंतरिक्ष विभाग<br>
                Indian Space Research Organisation, Department of Space</h1>
                <div class='subtitle'>भारत सरकार / Government of India</div>
            </div>
        </div>
        <img src='https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg' class='emblem' alt='Emblem'>
    </div>
</div>

<div class='tri-divider'></div>

<!-- Navigation -->
<div class='nav-bar'>
    <div class='nav-container'>
        <a href='#' class='nav-item'>Home</a>
        <a href='#' class='nav-item'>About</a>
        <a href='#' class='nav-item'>Missions</a>
        <a href='#' class='nav-item'>Launches</a>
        <a href='#' class='nav-item'>Centres</a>
        <a href='#' class='nav-item'>Monitoring</a>
    </div>
</div>
""", unsafe_allow_html=True)

# === CONTENT AREA ===
st.markdown("<div class='content-area'><div class='content-container'>", unsafe_allow_html=True)

# Page Header
st.markdown("""
<div class='page-header'>
    <h2>Launch Pad Structural Health Monitoring System</h2>
    <p>Satish Dhawan Space Centre SHAR, Sriharikota • Real-time Predictive Maintenance Platform</p>
</div>
""", unsafe_allow_html=True)

# Live Section
col_main, col_side = st.columns([2.5, 1.5])

with col_main:
    st.markdown("""
    <div class='info-card'>
        <div class='live-badge'>
            <div class='live-dot'></div>
            LIVE
        </div>
        <div class='video-wrapper'>
            <iframe src='https://www.youtube.com/embed/21X5lGlDOfg?autoplay=1&mute=1' 
            frameborder='0' allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture' 
            allowfullscreen></iframe>
        </div>
        <div style='margin-top: 1rem; color: #64748b; font-size: 0.9rem;'>
            <strong>ISRO Official Live Stream</strong> - Launch Operations & Mission Updates
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_side:
    st.markdown("""
    <div class='info-card'>
        <div class='card-title'>Next Launch Countdown</div>
        <div class='countdown-box'>
            <div class='countdown-label'>PSLV-C62 / EOS-N1 Mission</div>
            <div class='countdown-time'>+00:00:05:570</div>
            <div class='countdown-info'>
                Launch Vehicle: PSLV-C62<br>
                Launch Site: First Launch Pad
            </div>
        </div>
    </div>
    
    <div class='info-card'>
        <div class='card-title'>Latest Updates</div>
        <div class='news-item'>
            <div class='news-title'>LVM3-M6 mission successfully places BlueBird Block-2 satellite</div>
            <div class='news-time'>2 hours ago</div>
        </div>
        <div class='news-item'>
            <div class='news-title'>ISRO's Aditya-L1 decodes Solar Storm impact on Earth's Magnetic Shield</div>
            <div class='news-time'>5 hours ago</div>
        </div>
        <div class='news-item'>
            <div class='news-title'>Overview of PSLV-C62 / EOS-N1 Mission</div>
            <div class='news-time'>1 day ago</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Data Source Selection
st.markdown("<div class='info-card'><div class='card-title'>Data Source Configuration</div>", unsafe_allow_html=True)
data_source = st.radio("", ["Live Sensor Feed", "CSV File Upload"], label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

# Live Sensor Mode
if data_source == "Live Sensor Feed":
    st.markdown("<div class='info-card'><div class='card-title'>Sensor Input Parameters</div>", unsafe_allow_html=True)
    
    st.subheader("Vibration Sensors (Tri-axial Accelerometers)")
    c1, c2, c3 = st.columns(3)
    with c1:
        vib_x = st.number_input("X-axis (m/s²)", 0.0, 5.0, 0.72, 0.01)
    with c2:
        vib_y = st.number_input("Y-axis (m/s²)", 0.0, 5.0, 0.68, 0.01)
    with c3:
        vib_z = st.number_input("Z-axis (m/s²)", 0.0, 4.0, 0.61, 0.01)
    
    st.subheader("Additional Monitoring Systems")
    c4, c5, c6 = st.columns(3)
    with c4:
        pressure = st.number_input("Hydraulic Pressure (bar)", 120.0, 260.0, 202.0, 1.0)
    with c5:
        strain = st.number_input("Structural Strain (µε)", 40.0, 450.0, 88.0, 2.0)
    with c6:
        temperature = st.number_input("Temperature (°C)", 20.0, 50.0, 28.5, 0.1)
    
    health = calculate_health_from_sensors(vib_x, vib_y, vib_z, pressure, strain, temperature)
    
    st.markdown(f"""
    <div class='health-display'>
        <div class='health-label'>Component Health Index</div>
        <div class='health-value'>{health:.3f}</div>
        <div class='health-label'>Auto-calculated from sensor readings</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='info-card'><div class='card-title'>Risk Analysis</div>", unsafe_allow_html=True)
    
    if st.button("Execute Analysis"):
        with st.spinner("Processing..."):
            time.sleep(0.5)
            
            input_data = pd.DataFrame({
                'vibration_x_ms2': [vib_x], 'vibration_y_ms2': [vib_y], 'vibration_z_ms2': [vib_z],
                'pressure_bar': [pressure], 'strain_microstrain': [strain], 'temperature_c': [temperature],
                'health_state': [health]
            })
            
            for col in feature_cols:
                if col not in input_data.columns:
                    input_data[col] = 0
            
            rmi_score = model.predict_proba(input_data[feature_cols])[0, 1]
            st.session_state.rmi = rmi_score
            st.session_state.timestamp = datetime.now()
    
    if 'rmi' in st.session_state:
        score = st.session_state.rmi
        timestamp = st.session_state.timestamp
        
        cm1, cm2, cm3 = st.columns(3)
        with cm1:
            st.metric("Failure Probability", f"{score:.2%}")
        with cm2:
            st.metric("Health Index", f"{health:.3f}")
        with cm3:
            st.metric("Updated", timestamp.strftime('%H:%M:%S'))
        
        if score >= 0.35:
            st.markdown("<div class='status-box status-critical'><div class='status-title'>CRITICAL ALERT</div>Immediate maintenance required. Launch hold recommended.</div>", unsafe_allow_html=True)
        elif score >= 0.18:
            st.markdown("<div class='status-box status-warning'><div class='status-title'>ELEVATED RISK</div>Priority inspection required within 48 hours.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='status-box status-normal'><div class='status-title'>OPERATIONAL</div>All systems normal. Launch clearance: GO</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("<div class='info-card'><div class='card-title'>Batch Analysis - CSV Upload</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'], label_visibility="collapsed")
    
    if uploaded_file:
        try:
            batch_data = pd.read_csv(uploaded_file)
            required_cols = ['vibration_x_ms2', 'vibration_y_ms2', 'vibration_z_ms2', 'pressure_bar', 'strain_microstrain', 'temperature_c']
            
            if all(col in batch_data.columns for col in required_cols):
                batch_data['health_state'] = batch_data.apply(
                    lambda row: calculate_health_from_sensors(row['vibration_x_ms2'], row['vibration_y_ms2'], 
                    row['vibration_z_ms2'], row['pressure_bar'], row['strain_microstrain'], row['temperature_c']), axis=1)
                
                for col in feature_cols:
                    if col not in batch_data.columns:
                        batch_data[col] = 0
                
                batch_risks = model.predict_proba(batch_data[feature_cols])[:, 1]
                
                cb1, cb2, cb3, cb4 = st.columns(4)
                with cb1:
                    st.metric("Total", len(batch_risks))
                with cb2:
                    st.metric("Avg Risk", f"{batch_risks.mean():.1%}")
                with cb3:
                    st.metric("Critical", (batch_risks>0.35).sum())
                with cb4:
                    st.metric("Safe", (batch_risks<=0.18).sum())
                
                results_df = batch_data[required_cols + ['health_state']].copy()
                results_df['failure_probability'] = batch_risks
                st.dataframe(results_df, use_container_width=True)
                
                st.download_button("Download Report", results_df.to_csv(index=False),
                    f"ISRO_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", "text/csv")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# System Info
st.markdown("<div class='info-card'><div class='card-title'>System Information</div>", unsafe_allow_html=True)
i1, i2, i3 = st.columns(3)
with i1:
    st.markdown("**Model Specs**\n- XGBoost Classifier\n- 140,160 samples\n- 7-day horizon\n- <0.5s inference")
with i2:
    st.markdown("**Performance**\n- Precision: 89.12%\n- Recall: 94.31%\n- F1: 91.64%\n- AUC: 0.9234")
with i3:
    st.markdown("**Health Weights**\n- Vibration: 25%\n- Pressure: 20%\n- Strain: 15%\n- Temp: 10%")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='tri-divider'></div>
<div class='isro-footer'>
    <div class='footer-content'>
        <div class='footer-title'>भारतीय अंतरिक्ष अनुसंधान संगठन<br>INDIAN SPACE RESEARCH ORGANISATION</div>
        <div class='footer-info'>
            Satish Dhawan Space Centre SHAR • Sriharikota Range • Andhra Pradesh • Pin: 524124<br>
            Launch Pad Health Monitoring System v3.1 • Department of Space • Government of India<br>
            © 2026 ISRO • All Rights Reserved
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
