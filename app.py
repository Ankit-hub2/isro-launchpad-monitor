import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime
import time

# Page Config
st.set_page_config(
    page_title="ISRO - Launch Pad Monitoring System", 
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

# Complete Styling
st.markdown("""
<style>
    /* Global Reset */
    * {margin: 0; padding: 0; box-sizing: border-box;}
    .main .block-container {padding: 0 !important; max-width: 100% !important;}
    
    /* Top Navigation Bar */
    .top-nav {
        background: #00274d;
        color: white;
        padding: 0.6rem 2rem;
        font-size: 0.75rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .top-links a {
        color: white;
        text-decoration: none;
        margin-right: 1.2rem;
    }
    
    /* Main Header */
    .main-header {
        background: linear-gradient(180deg, #003d82 0%, #00274d 100%);
        padding: 1.8rem 2rem;
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    
    .header-content {
        max-width: 1400px;
        margin: 0 auto;
        text-align: center;
    }
    
    .org-name-hindi {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
        opacity: 0.95;
    }
    
    .org-name-english {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        letter-spacing: 0.3px;
    }
    
    .org-subtitle {
        font-size: 0.85rem;
        opacity: 0.85;
    }
    
    /* Tricolor Bar */
    .tricolor {
        height: 4px;
        background: linear-gradient(90deg, 
            #FF9933 0%, #FF9933 33.33%, 
            #FFFFFF 33.33%, #FFFFFF 66.66%, 
            #138808 66.66%, #138808 100%);
    }
    
    /* Navigation Menu */
    .nav-menu {
        background: #004d9f;
        padding: 0.8rem 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .nav-container {
        max-width: 1400px;
        margin: 0 auto;
        display: flex;
        gap: 2rem;
        flex-wrap: wrap;
    }
    
    .nav-link {
        color: white;
        font-size: 0.9rem;
        padding: 0.4rem 0;
        border-bottom: 2px solid transparent;
        transition: border-color 0.3s;
    }
    
    .nav-link:hover {
        border-bottom-color: #FF9933;
    }
    
    /* Content Area */
    .content-wrapper {
        background: #f5f7fa;
        min-height: 70vh;
        padding: 2rem;
    }
    
    .container {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Page Title */
    .page-title {
        background: white;
        border-left: 5px solid #FF9933;
        padding: 1.8rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .page-title h2 {
        color: #003d82;
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .page-title p {
        color: #64748b;
        font-size: 0.95rem;
    }
    
    /* Cards */
    .card {
        background: white;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    .card-header {
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
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 1rem;
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
    
    /* Video Container */
    .video-box {
        position: relative;
        width: 100%;
        padding-bottom: 56.25%;
        background: #000;
        margin: 1rem 0;
    }
    
    .video-box iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
    
    /* Countdown */
    .countdown {
        background: #0f172a;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .countdown-label {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-bottom: 0.75rem;
        letter-spacing: 0.5px;
    }
    
    .countdown-time {
        color: #4ade80;
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'Courier New', monospace;
        letter-spacing: 2px;
    }
    
    .countdown-info {
        color: #94a3b8;
        font-size: 0.8rem;
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
        font-size: 0.9rem;
        margin-bottom: 0.4rem;
        line-height: 1.4;
    }
    
    .news-time {
        color: #64748b;
        font-size: 0.75rem;
    }
    
    /* Health Display */
    .health-box {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        border: 2px solid #cbd5e1;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .health-label {
        color: #475569;
        font-size: 0.75rem;
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
    
    /* Status Boxes */
    .status-box {
        padding: 1.25rem;
        border-left: 5px solid;
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
        margin-bottom: 0.4rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: #003d82 !important;
        color: white !important;
        border: none !important;
        padding: 0.875rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        width: 100% !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        background: #00274d !important;
        box-shadow: 0 4px 12px rgba(0,61,130,0.3) !important;
    }
    
    /* Form Elements */
    .stNumberInput label {
        color: #334155 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }
    
    .stRadio label {
        background: white;
        padding: 0.75rem 1.25rem;
        border: 2px solid #e2e8f0;
        font-weight: 500;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.4rem;
        font-weight: 700;
        color: #003d82;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(180deg, #003d82 0%, #001a3d 100%);
        color: white;
        padding: 2.5rem 2rem;
        text-align: center;
        margin-top: 3rem;
    }
    
    .footer-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    
    .footer-text {
        font-size: 0.85rem;
        opacity: 0.9;
        line-height: 1.8;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu, footer, .stDeployButton {visibility: hidden;}
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .top-nav, .nav-menu, .content-wrapper {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .main-header {
            padding: 1.2rem 1rem;
        }
        
        .org-name-hindi {
            font-size: 0.85rem;
        }
        
        .org-name-english {
            font-size: 1.1rem;
        }
        
        .org-subtitle {
            font-size: 0.75rem;
        }
        
        .nav-container {
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .page-title h2 {
            font-size: 1.35rem;
        }
        
        .countdown-time {
            font-size: 1.75rem;
        }
        
        .health-value {
            font-size: 2rem;
        }
        
        .card {
            padding: 1.25rem;
        }
    }
    
    @media (max-width: 480px) {
        .page-title {
            padding: 1.2rem 1rem;
        }
        
        .card {
            padding: 1rem;
        }
        
        .countdown-time {
            font-size: 1.5rem;
        }
    }
</style>

<!-- Top Navigation -->
<div class='top-nav'>
    <div class='top-links'>
        <a href='#'>English</a>
        <a href='#'>हिंदी</a>
        <a href='#'>Sitemap</a>
        <a href='#'>Contact Us</a>
    </div>
    <div>A+ A A-</div>
</div>

<!-- Main Header -->
<div class='main-header'>
    <div class='header-content'>
        <div class='org-name-hindi'>भारतीय अंतरिक्ष अनुसंधान संगठन, अंतरिक्ष विभाग</div>
        <div class='org-name-english'>INDIAN SPACE RESEARCH ORGANISATION</div>
        <div class='org-name-english' style='font-size: 1.1rem; margin-top: 0.2rem;'>Department of Space</div>
        <div class='org-subtitle'>भारत सरकार / Government of India</div>
    </div>
</div>

<!-- Tricolor Bar -->
<div class='tricolor'></div>

<!-- Navigation Menu -->
<div class='nav-menu'>
    <div class='nav-container'>
        <div class='nav-link'>Home</div>
        <div class='nav-link'>About</div>
        <div class='nav-link'>Missions</div>
        <div class='nav-link'>Launches</div>
        <div class='nav-link'>Centres</div>
        <div class='nav-link'>Monitoring</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Content Area
st.markdown("<div class='content-wrapper'><div class='container'>", unsafe_allow_html=True)

# Page Title
st.markdown("""
<div class='page-title'>
    <h2>Launch Pad Structural Health Monitoring System</h2>
    <p>Satish Dhawan Space Centre SHAR, Sriharikota • Real-time Predictive Maintenance Platform</p>
</div>
""", unsafe_allow_html=True)

# Main Layout
col_left, col_right = st.columns([2.5, 1.5])

with col_left:
    st.markdown("""
    <div class='card'>
        <div class='live-badge'><div class='live-dot'></div>LIVE</div>
        <div class='video-box'>
            <iframe src='https://www.youtube.com/embed/21X5lGlDOfg?autoplay=1&mute=1' 
            frameborder='0' allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture' 
            allowfullscreen></iframe>
        </div>
        <div style='margin-top: 1rem; color: #64748b; font-size: 0.85rem;'>
            <strong>ISRO Official Live Stream</strong> - Launch Operations & Mission Updates
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class='card'>
        <div class='card-header'>Next Launch Countdown</div>
        <div class='countdown'>
            <div class='countdown-label'>PSLV-C62 / EOS-N1 Mission</div>
            <div class='countdown-time'>+00:00:05:570</div>
            <div class='countdown-info'>
                Launch Vehicle: PSLV-C62<br>
                Launch Site: First Launch Pad
            </div>
        </div>
    </div>
    
    <div class='card'>
        <div class='card-header'>Latest Updates</div>
        <div class='news-item'>
            <div class='news-title'>LVM3-M6 mission successfully places BlueBird Block-2 satellite</div>
            <div class='news-time'>2 hours ago</div>
        </div>
        <div class='news-item'>
            <div class='news-title'>ISRO's Aditya-L1 decodes Solar Storm impact on Earth's Shield</div>
            <div class='news-time'>5 hours ago</div>
        </div>
        <div class='news-item'>
            <div class='news-title'>Overview of PSLV-C62 / EOS-N1 Mission</div>
            <div class='news-time'>1 day ago</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Data Source Selection
st.markdown("<div class='card'><div class='card-header'>Data Source Configuration</div>", unsafe_allow_html=True)
data_source = st.radio("", ["Live Sensor Feed", "CSV File Upload"], label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

# Live Sensor Mode
if data_source == "Live Sensor Feed":
    st.markdown("<div class='card'><div class='card-header'>Sensor Input Parameters</div>", unsafe_allow_html=True)
    
    st.subheader("Vibration Sensors (Tri-axial Accelerometers)")
    v1, v2, v3 = st.columns(3)
    with v1:
        vib_x = st.number_input("X-axis (m/s²)", 0.0, 5.0, 0.72, 0.01, key="live_vib_x")
    with v2:
        vib_y = st.number_input("Y-axis (m/s²)", 0.0, 5.0, 0.68, 0.01, key="live_vib_y")
    with v3:
        vib_z = st.number_input("Z-axis (m/s²)", 0.0, 4.0, 0.61, 0.01, key="live_vib_z")
    
    st.subheader("Secondary Monitoring Systems")
    s1, s2, s3 = st.columns(3)
    with s1:
        pressure = st.number_input("Hydraulic Pressure (bar)", 120.0, 260.0, 202.0, 1.0, key="live_pressure")
    with s2:
        strain = st.number_input("Structural Strain (µε)", 40.0, 450.0, 88.0, 2.0, key="live_strain")
    with s3:
        temperature = st.number_input("Temperature (°C)", 20.0, 50.0, 28.5, 0.1, key="live_temp")
    
    health = calculate_health_from_sensors(vib_x, vib_y, vib_z, pressure, strain, temperature)
    
    st.markdown(f"""
    <div class='health-box'>
        <div class='health-label'>Component Health Index</div>
        <div class='health-value'>{health:.3f}</div>
        <div class='health-label'>Auto-calculated from sensor readings</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Analysis Section
    st.markdown("<div class='card'><div class='card-header'>Risk Analysis</div>", unsafe_allow_html=True)
    
    if st.button("Execute Analysis", type="primary", key="live_analyze"):
        with st.spinner("Computing risk indices..."):
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
            st.session_state.live_rmi_score = rmi_score
            st.session_state.live_health = health
            st.session_state.live_timestamp = datetime.now()
    
    if 'live_rmi_score' in st.session_state:
        score = st.session_state.live_rmi_score
        health_calc = st.session_state.live_health
        timestamp = st.session_state.live_timestamp
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Failure Probability", f"{score:.2%}")
        with m2:
            st.metric("Health Index", f"{health_calc:.3f}")
        with m3:
            st.metric("Last Update", timestamp.strftime('%H:%M:%S'))
        
        if score >= 0.35:
            st.markdown("""
            <div class='status-box status-critical'>
                <div class='status-title'>CRITICAL ALERT</div>
                <div>Immediate maintenance required. Launch hold recommended.</div>
            </div>
            """, unsafe_allow_html=True)
        elif score >= 0.18:
            st.markdown("""
            <div class='status-box status-warning'>
                <div class='status-title'>ELEVATED RISK</div>
                <div>Priority inspection required within 48 hours.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='status-box status-normal'>
                <div class='status-title'>OPERATIONAL</div>
                <div>All systems normal. Launch clearance: GO</div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("Health Calculation Breakdown"):
            vib_mag = np.sqrt(vib_x**2 + vib_y**2 + vib_z**2)
            st.markdown(f"""
            **Health Index Calculation:**
            - Started at: 1.000 (perfect)
            - Vibration impact ({vib_mag:.2f} m/s²): {'High' if vib_mag > 2.5 else 'Normal'}
            - Pressure impact ({pressure:.0f} bar): {'Low' if pressure < 175 else 'Normal'}
            - Strain impact ({strain:.0f} µε): {'High' if strain > 250 else 'Normal'}
            - Temperature impact ({temperature:.1f}°C): {'High' if temperature > 35 else 'Normal'}
            
            **Final Health: {health_calc:.3f}**
            """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# CSV File Mode
else:
    st.markdown("<div class='card'><div class='card-header'>Batch CSV File Analysis</div>", unsafe_allow_html=True)
    
    st.info("Upload a CSV file with sensor readings. Health index will be calculated automatically for each row.")
    
    uploaded_file = st.file_uploader("Select CSV File", type=['csv'])
    
    if uploaded_file is not None:
        with st.spinner("Processing sensor data batch..."):
            try:
                batch_data = pd.read_csv(uploaded_file)
                st.success(f"Loaded {len(batch_data)} records")
                
                with st.expander("Data Preview (first 5 rows)"):
                    st.dataframe(batch_data.head())
                
                required_cols = ['vibration_x_ms2', 'vibration_y_ms2', 'vibration_z_ms2', 
                               'pressure_bar', 'strain_microstrain', 'temperature_c']
                
                missing = [col for col in required_cols if col not in batch_data.columns]
                
                if missing:
                    st.error(f"Missing required columns: {', '.join(missing)}")
                    st.info("Required columns: vibration_x_ms2, vibration_y_ms2, vibration_z_ms2, pressure_bar, strain_microstrain, temperature_c")
                else:
                    batch_data['health_state'] = batch_data.apply(
                        lambda row: calculate_health_from_sensors(
                            row['vibration_x_ms2'],
                            row['vibration_y_ms2'],
                            row['vibration_z_ms2'],
                            row['pressure_bar'],
                            row['strain_microstrain'],
                            row['temperature_c']
                        ), axis=1
                    )
                    
                    for col in feature_cols:
                        if col not in batch_data.columns:
                            batch_data[col] = 0
                    
                    batch_features = batch_data[feature_cols]
                    batch_risks = model.predict_proba(batch_features)[:, 1]
                    
                    st.markdown("### Analysis Summary")
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("Total Components", len(batch_risks))
                    with c2:
                        st.metric("Average Risk", f"{batch_risks.mean():.2%}")
                    with c3:
                        st.metric("Critical (>35%)", f"{(batch_risks>0.35).sum()}")
                    with c4:
                        st.metric("Safe (<18%)", f"{(batch_risks<=0.18).sum()}")
                    
                    st.markdown("### Risk Distribution")
                    risk_categories = pd.cut(batch_risks, 
                                            bins=[0, 0.18, 0.35, 1.0], 
                                            labels=['Normal (GO)', 'Caution', 'Critical'])
                    
                    risk_summary = pd.DataFrame({
                        'Status': risk_categories.value_counts().index,
                        'Count': risk_categories.value_counts().values,
                        'Percentage': (risk_categories.value_counts().values / len(batch_risks) * 100).round(1)
                    })
                    
                    st.dataframe(risk_summary, use_container_width=True)
                    
                    with st.expander("Detailed Results (All Components)"):
                        results_df = batch_data[['vibration_x_ms2', 'vibration_y_ms2', 'vibration_z_ms2',
                                                 'pressure_bar', 'strain_microstrain', 'temperature_c',
                                                 'health_state']].copy()
                        results_df['Failure_Probability'] = batch_risks
                        results_df['Risk_Level'] = risk_categories
                        st.dataframe(results_df)
                    
                    results_csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="Download Full Analysis Report",
                        data=results_csv,
                        file_name=f"ISRO_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure your CSV has these columns: vibration_x_ms2, vibration_y_ms2, vibration_z_ms2, pressure_bar, strain_microstrain, temperature_c")
    
    st.markdown("</div>", unsafe_allow_html=True)

# System Information
st.markdown("<div class='card'><div class='card-header'>System Information</div>", unsafe_allow_html=True)

info1, info2, info3 = st.columns(3)

with info1:
    st.markdown("""
    **Model Specifications**
    - Algorithm: XGBoost Classifier
    - Training: 140,160 samples
    - Horizon: 7-day prediction
    - Inference: <0.5 seconds
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
    **Health Calculation**
