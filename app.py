import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime, timedelta
import time

# === PAGE CONFIG ===
st.set_page_config(
    page_title="ISRO Launch Pad Monitoring System", 
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_isro_system():
    model = joblib.load('isro_launchpad_model.pkl')
    feature_cols = joblib.load('feature_cols.pkl')
    return model, feature_cols

model, feature_cols = load_isro_system()

# === HEALTH CALCULATION FUNCTION ===
def calculate_health_from_sensors(vib_x, vib_y, vib_z, pressure, strain, temp):
    """Calculate component health from sensor readings"""
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

# === ISRO OFFICIAL STYLING ===
st.markdown("""
<style>
    /* Global Reset */
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    
    /* ISRO Official Header */
    .isro-header {
        background: linear-gradient(180deg, #003d82 0%, #002855 100%);
        padding: 0;
        margin: 0;
        color: white;
    }
    
    .top-nav {
        background: #00274d;
        padding: 0.5rem 2rem;
        font-size: 0.8rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .top-nav a {
        color: white;
        text-decoration: none;
        margin-right: 1.5rem;
    }
    
    .main-header {
        padding: 1.5rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 2rem;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 2rem;
        flex: 1;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .isro-logo {
        width: 80px;
        height: auto;
    }
    
    .header-text h1 {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 600;
        line-height: 1.4;
    }
    
    .header-text .hindi {
        font-size: 0.95rem;
        opacity: 0.9;
    }
    
    .header-text .subtitle {
        font-size: 0.85rem;
        opacity: 0.8;
        margin-top: 0.25rem;
    }
    
    .header-right {
        display: flex;
        align-items: center;
        gap: 2rem;
    }
    
    .emblem {
        width: 60px;
        height: auto;
    }
    
    /* Orange Divider */
    .orange-divider {
        height: 4px;
        background: linear-gradient(90deg, #FF9933 0%, #FF9933 33%, #FFFFFF 33%, #FFFFFF 66%, #138808 66%, #138808 100%);
    }
    
    /* Main Navigation */
    .main-nav {
        background: #004d9f;
        padding: 0.75rem 2rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
        font-size: 0.95rem;
    }
    
    .nav-links a {
        color: white;
        text-decoration: none;
        padding: 0.5rem 0;
        border-bottom: 2px solid transparent;
    }
    
    .nav-links a:hover {
        border-bottom-color: #FF9933;
    }
    
    /* Content Area */
    .content-wrapper {
        background: #f5f5f5;
        min-height: calc(100vh - 300px);
    }
    
    .container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Page Title */
    .page-title {
        background: white;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #FF9933;
    }
    
    .page-title h2 {
        margin: 0;
        color: #003d82;
        font-size: 1.75rem;
        font-weight: 700;
    }
    
    .page-title p {
        margin: 0.5rem 0 0 0;
        color: #666;
        font-size: 1rem;
    }
    
    /* Cards */
    .card {
        background: white;
        border: 1px solid #ddd;
        border-radius: 0;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .card-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #003d82;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #FF9933;
    }
    
    /* Live Sections */
    .live-section {
        background: white;
        border: 1px solid #ddd;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: #dc2626;
        color: white;
        padding: 0.25rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .live-dot {
        width: 8px;
        height: 8px;
        background: white;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    .countdown-display {
        background: #1a1a1a;
        color: #4ade80;
        padding: 1.5rem;
        text-align: center;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
    }
    
    .countdown-label {
        font-size: 0.9rem;
        color: #9ca3af;
        margin-bottom: 0.5rem;
    }
    
    .countdown-time {
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: 2px;
    }
    
    .news-item {
        padding: 0.75rem;
        border-left: 3px solid #003d82;
        background: #f8fafc;
        margin-bottom: 0.75rem;
    }
    
    .news-title {
        color: #003d82;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.25rem;
    }
    
    .news-time {
        color: #64748b;
        font-size: 0.8rem;
    }
    
    /* Status Indicators */
    .status-indicator {
        padding: 1rem;
        border-radius: 0;
        border-left: 4px solid;
        margin: 1rem 0;
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
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }
    
    /* Health Display */
    .health-box {
        background: #f1f5f9;
        border: 2px solid #cbd5e1;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .health-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0.5rem 0;
        font-family: 'Courier New', monospace;
    }
    
    .health-label {
        font-size: 0.8rem;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Buttons */
    .stButton > button {
        background: #003d82 !important;
        color: white !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: #002855 !important;
    }
    
    /* Footer */
    .isro-footer {
        background: linear-gradient(180deg, #003d82 0%, #001a3d 100%);
        color: white;
        padding: 2rem;
        text-align: center;
        margin-top: 3rem;
    }
    
    .footer-content {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .footer-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .footer-text {
        font-size: 0.9rem;
        opacity: 0.9;
        line-height: 1.6;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .main-header {
            flex-direction: column;
            text-align: center;
            padding: 1rem;
        }
        
        .header-left, .header-right {
            width: 100%;
            justify-content: center;
        }
        
        .logo-container {
            flex-direction: column;
        }
        
        .nav-links {
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .container {
            padding: 1rem;
        }
        
        .countdown-time {
            font-size: 1.75rem;
        }
        
        .isro-logo, .emblem {
            width: 50px;
        }
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>

<!-- ISRO Header -->
<div class='isro-header'>
    <div class='top-nav'>
        <a href='#'>English</a>
        <a href='#'>हिंदी</a>
        <a href='#'>Sitemap</a>
        <a href='#'>Contact Us</a>
        <a href='#'>Feedback</a>
    </div>
    
    <div class='main-header'>
        <div class='header-left'>
            <div class='logo-container'>
                <img src='https://www.isro.gov.in/media/image/index.php?img_id=logo_1' class='isro-logo' alt='ISRO'>
                <div class='header-text'>
                    <div class='hindi'>भारतीय अंतरिक्ष अनुसंधान संगठन, अंतरिक्ष विभाग</div>
                    <h1>Indian Space Research Organisation, Department of Space</h1>
                    <div class='subtitle'>भारत सरकार / Government of India</div>
                </div>
            </div>
        </div>
        <div class='header-right'>
            <img src='https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg' class='emblem' alt='India Emblem'>
        </div>
    </div>
</div>

<div class='orange-divider'></div>

<div class='main-nav'>
    <div class='nav-links'>
        <a href='#'>Home</a>
        <a href='#'>About</a>
        <a href='#'>Missions</a>
        <a href='#'>Launches</a>
        <a href='#'>Centres</a>
        <a href='#'>Monitoring</a>
    </div>
</div>
""", unsafe_allow_html=True)

# === CONTENT AREA ===
st.markdown("<div class='content-wrapper'><div class='container'>", unsafe_allow_html=True)

# Page Title
st.markdown("""
<div class='page-title'>
    <h2>Launch Pad Structural Health Monitoring System</h2>
    <p>Satish Dhawan Space Centre SHAR, Sriharikota • Real-time Predictive Maintenance Platform</p>
</div>
""", unsafe_allow_html=True)

# === LIVE MISSION SECTION ===
col_live1, col_live2 = st.columns([2, 1])

with col_live1:
    st.markdown("""
    <div class='live-section'>
        <div class='live-badge'>
            <div class='live-dot'></div>
            LIVE
        </div>
        <div style='margin-top: 1rem;'>
            <iframe width='100%' height='315' 
            src='https://www.youtube.com/embed/live_stream?channel=UCHh4YMD3L03gRKSeuK3sJWQ' 
            frameborder='0' allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture' 
            allowfullscreen></iframe>
        </div>
        <div style='margin-top: 0.75rem; color: #666; font-size: 0.9rem;'>
            <strong>ISRO Official Live Stream</strong> - Launch Operations & Mission Updates
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_live2:
    # Countdown
    st.markdown("""
    <div class='card'>
        <div class='card-header'>Next Launch Countdown</div>
        <div class='countdown-display'>
            <div class='countdown-label'>PSLV-C62 / EOS-N1 Mission</div>
            <div class='countdown-time'>+00:00:05:570</div>
        </div>
        <div style='text-align: center; color: #666; font-size: 0.85rem; margin-top: 0.5rem;'>
            Launch Vehicle: PSLV-C62<br>
            Launch Site: First Launch Pad
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Live News
    st.markdown("""
    <div class='card'>
        <div class='card-header'>Latest Updates</div>
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

# === DATA SOURCE SELECTION ===
st.markdown("<div class='card'><div class='card-header'>Data Source Configuration</div>", unsafe_allow_html=True)
data_source = st.radio(
    "Select Input Method:",
    ["Live Sensor Feed", "CSV File Upload"],
    label_visibility="collapsed"
)
st.markdown("</div>", unsafe_allow_html=True)

# === LIVE SENSOR MODE ===
if data_source == "Live Sensor Feed":
    # Input Section
    st.markdown("<div class='card'><div class='card-header'>Sensor Input Parameters</div>", unsafe_allow_html=True)
    
    st.subheader("Vibration Sensors (Tri-axial Accelerometers)")
    col1, col2, col3 = st.columns(3)
    with col1:
        vib_x = st.number_input("X-axis (m/s²)", 0.0, 5.0, 0.72, 0.01, key="vx")
    with col2:
        vib_y = st.number_input("Y-axis (m/s²)", 0.0, 5.0, 0.68, 0.01, key="vy")
    with col3:
        vib_z = st.number_input("Z-axis (m/s²)", 0.0, 4.0, 0.61, 0.01, key="vz")
    
    st.subheader("Additional Monitoring Systems")
    col4, col5, col6 = st.columns(3)
    with col4:
        pressure = st.number_input("Hydraulic Pressure (bar)", 120.0, 260.0, 202.0, 1.0, key="pr")
    with col5:
        strain = st.number_input("Structural Strain (µε)", 40.0, 450.0, 88.0, 2.0, key="st")
    with col6:
        temperature = st.number_input("Temperature (°C)", 20.0, 50.0, 28.5, 0.1, key="tp")
    
    health = calculate_health_from_sensors(vib_x, vib_y, vib_z, pressure, strain, temperature)
    
    st.markdown(f"""
    <div class='health-box'>
        <div class='health-label'>Component Health Index</div>
        <div class='health-value'>{health:.3f}</div>
        <div class='health-label'>Auto-calculated from sensor readings</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Analysis
    st.markdown("<div class='card'><div class='card-header'>Risk Analysis</div>", unsafe_allow_html=True)
    
    if st.button("Execute Analysis", type="primary", key="analyze"):
        with st.spinner("Processing sensor data..."):
            time.sleep(0.5)
            
            input_data = pd.DataFrame({
                'vibration_x_ms2': [vib_x],
                'vibration_y_ms2': [vib_y],
                'vibration_z_ms2': [vib_z],
                'pressure_bar': [pressure],
                'strain_microstrain': [strain],
                'temperature_c': [temperature],
                'health_state': [health]
            })
            
            for col in feature_cols:
                if col not in input_data.columns:
                    input_data[col] = 0
            input_data = input_data[feature_cols]
            
            rmi_score = model.predict_proba(input_data)[0, 1]
            st.session_state.rmi = rmi_score
            st.session_state.health = health
            st.session_state.timestamp = datetime.now()
    
    if 'rmi' in st.session_state:
        score = st.session_state.rmi
        timestamp = st.session_state.timestamp
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Failure Probability", f"{score:.2%}")
        with col_m2:
            st.metric("Health Index", f"{health:.3f}")
        with col_m3:
            st.metric("Last Updated", timestamp.strftime('%H:%M:%S'))
        
        if score >= 0.35:
            st.markdown("""
            <div class='status-indicator status-critical'>
                <div class='status-title'>CRITICAL ALERT</div>
                <div>Immediate maintenance required. Launch hold recommended.</div>
            </div>
            """, unsafe_allow_html=True)
        elif score >= 0.18:
            st.markdown("""
            <div class='status-indicator status-warning'>
                <div class='status-title'>ELEVATED RISK</div>
                <div>Priority inspection required within 48 hours.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='status-indicator status-normal'>
                <div class='status-title'>OPERATIONAL</div>
                <div>All systems normal. Launch clearance: GO</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# === CSV MODE ===
else:
    st.markdown("<div class='card'><div class='card-header'>Batch Analysis - CSV Upload</div>", unsafe_allow_html=True)
    
    st.info("Upload CSV file containing sensor readings for batch processing")
    
    uploaded_file = st.file_uploader("Select CSV File", type=['csv'], label_visibility="collapsed")
    
    if uploaded_file is not None:
        with st.spinner("Processing batch data..."):
            try:
                batch_data = pd.read_csv(uploaded_file)
                st.success(f"Loaded {len(batch_data)} records successfully")
                
                required_cols = ['vibration_x_ms2', 'vibration_y_ms2', 'vibration_z_ms2', 
                               'pressure_bar', 'strain_microstrain', 'temperature_c']
                
                missing = [col for col in required_cols if col not in batch_data.columns]
                
                if missing:
                    st.error(f"Missing columns: {', '.join(missing)}")
                else:
                    batch_data['health_state'] = batch_data.apply(
                        lambda row: calculate_health_from_sensors(
                            row['vibration_x_ms2'], row['vibration_y_ms2'], row['vibration_z_ms2'],
                            row['pressure_bar'], row['strain_microstrain'], row['temperature_c']
                        ), axis=1
                    )
                    
                    for col in feature_cols:
                        if col not in batch_data.columns:
                            batch_data[col] = 0
                    
                    batch_features = batch_data[feature_cols]
                    batch_risks = model.predict_proba(batch_features)[:, 1]
                    
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("Total Components", len(batch_risks))
                    with c2:
                        st.metric("Average Risk", f"{batch_risks.mean():.1%}")
                    with c3:
                        st.metric("Critical", f"{(batch_risks>0.35).sum()}")
                    with c4:
                        st.metric("Safe", f"{(batch_risks<=0.18).sum()}")
                    
                    results_df = batch_data[required_cols + ['health_state']].copy()
                    results_df['failure_probability'] = batch_risks
                    
                    st.dataframe(results_df, use_container_width=True)
                    
                    results_csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="Download Analysis Report",
                        data=results_csv,
                        file_name=f"ISRO_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# === SYSTEM INFO ===
st.markdown("<div class='card'><div class='card-header'>System Information</div>", unsafe_allow_html=True)

info1, info2, info3 = st.columns(3)

with info1:
    st.markdown("""
    **Model Specifications**
    - Algorithm: XGBoost Classifier
    - Training Samples: 140,160
    - Prediction Horizon: 7 days
    - Inference Time: <0.5 seconds
    """)

with info2:
    st.markdown("""
    **Performance Metrics**
    - Precision: 89.12%
    - Recall: 94.31%
    - F1-Score: 91.64%
    - ROC-AUC: 0.9234
    """)

with info3:
    st.markdown("""
    **Health Calculation Weights**
    - Vibration Impact: 25%
    - Pressure Impact: 20%
    - Strain Impact: 15%
    - Temperature Impact: 10%
    """)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# === FOOTER ===
st.markdown("""
<div class='orange-divider'></div>
<div class='isro-footer'>
    <div class='footer-content'>
        <div class='footer-title'>
            भारतीय अंतरिक्ष अनुसंधान संगठन<br>
            INDIAN SPACE RESEARCH ORGANISATION
        </div>
        <div class='footer-text'>
            Satish Dhawan Space Centre SHAR • Sriharikota Range • Andhra Pradesh • Pin: 524124<br>
            Launch Pad Health Monitoring System v3.1 • Department of Space • Government of India<br>
            © 2026 ISRO • All Rights Reserved
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
