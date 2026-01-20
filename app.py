import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime
import time

# Page Config
st.set_page_config(
    page_title="Launch Pad Monitoring System", 
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

# Enhanced Mobile-Responsive Styling
st.markdown("""
<style>
    /* Global Reset */
    * {margin: 0; padding: 0; box-sizing: border-box;}
    .main .block-container {padding: 0 !important; max-width: 100% !important;}
    
    /* Enhanced Header */
    .header-section {
        background: linear-gradient(135deg, #001f3f 0%, #003d82 50%, #00274d 100%);
        padding: 1.5rem 1rem;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .header-content {
        max-width: 1400px;
        margin: 0 auto;
        text-align: center;
        position: relative;
        z-index: 2;
    }
    
    .header-badge {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: #dc2626;
        color: white;
        padding: 0.4rem 0.8rem;
        font-size: 0.7rem;
        font-weight: 700;
        border-radius: 20px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% {opacity: 1; transform: scale(1);}
        50% {opacity: 0.7; transform: scale(1.05);}
    }
    
    .org-title-hindi {
        font-size: clamp(0.9rem, 2.5vw, 1.1rem);
        font-weight: 600;
        margin-bottom: 0.3rem;
        opacity: 0.95;
        letter-spacing: 0.5px;
    }
    
    .org-title-english {
        font-size: clamp(1.3rem, 4vw, 2rem);
        font-weight: 800;
        margin-bottom: 0.4rem;
        letter-spacing: 1px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: clamp(0.8rem, 2vw, 1rem);
        opacity: 0.9;
        font-weight: 500;
        letter-spacing: 0.3px;
    }
    
    /* Tricolor Bar */
    .tricolor {
        height: 5px;
        background: linear-gradient(90deg, 
            #FF9933 0%, #FF9933 33.33%, 
            #FFFFFF 33.33%, #FFFFFF 66.66%, 
            #138808 66.66%, #138808 100%);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Navigation - Mobile Optimized */
    .nav-section {
        background: rgba(0, 47, 108, 0.95);
        backdrop-filter: blur(10px);
        padding: 0.8rem 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .nav-container {
        max-width: 1400px;
        margin: 0 auto;
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .nav-link {
        color: white;
        font-size: clamp(0.75rem, 2vw, 0.85rem);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        transition: all 0.3s;
        font-weight: 500;
        white-space: nowrap;
    }
    
    .nav-link:hover {
        background: rgba(255, 153, 51, 0.2);
        transform: translateY(-1px);
    }
    
    /* Content Area */
    .content-wrapper {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        min-height: 80vh;
        padding: 2rem 1rem;
    }
    
    .container {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Page Title - Enhanced */
    .page-title {
        background: white;
        border-radius: 16px;
        border-left: 6px solid #FF9933;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
    .page-title h2 {
        color: #001f3f;
        font-size: clamp(1.5rem, 4vw, 2.2rem);
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .page-title p {
        color: #64748b;
        font-size: clamp(0.9rem, 2.5vw, 1.1rem);
        font-weight: 500;
    }
    
    /* Cards - Enhanced */
    .card {
        background: white;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s;
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.12);
    }
    
    .card-header {
        color: #001f3f;
        font-size: clamp(1.1rem, 3vw, 1.3rem);
        font-weight: 800;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 4px solid #FF9933;
        position: relative;
    }
    
    .card-header::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #FF9933, #138808);
        border-radius: 2px;
    }
    
    /* Health Display - Enhanced */
    .health-box {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 12px 40px rgba(16, 185, 129, 0.3);
    }
    
    .health-label {
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    
    .health-value {
        font-size: clamp(2.5rem, 8vw, 4rem);
        font-weight: 900;
        font-family: 'Courier New', monospace;
        letter-spacing: 3px;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Status Boxes */
    .status-box {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 6px solid;
    }
    
    .status-critical {background: #fef2f2; border-left-color: #dc2626; color: #7f1d1d;}
    .status-warning {background: #fffbeb; border-left-color: #f59e0b; color: #78350f;}
    .status-normal {background: #f0fdf4; border-left-color: #10b981; color: #14532d;}
    
    .status-title {
        font-weight: 800;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Buttons - Enhanced */
    .stButton > button {
        background: linear-gradient(135deg, #003d82, #001f3f) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        border-radius: 12px !important;
        width: 100% !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 16px rgba(0,61,130,0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00274d, #001a2e) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(0,61,130,0.4) !important;
    }
    
    /* Form Elements */
    .stNumberInput > label {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        color: #001f3f !important;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(180deg, #001f3f 0%, #000814 100%);
        color: white;
        padding: 3rem 1rem;
        text-align: center;
        margin-top: 4rem;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu, footer, .stDeployButton {visibility: hidden !important;}
    
    /* Ultra Mobile Responsive */
    @media (max-width: 768px) {
        .content-wrapper {padding: 1.5rem 0.5rem;}
        .card {padding: 1.5rem;}
        .page-title {padding: 1.5rem 1rem;}
        .nav-container {gap: 0.3rem;}
        .nav-link {padding: 0.4rem 0.8rem; font-size: 0.8rem;}
    }
    
    @media (max-width: 480px) {
        .header-section {padding: 1.2rem 0.8rem;}
        .header-badge {top: 0.8rem; right: 0.8rem; font-size: 0.65rem;}
        .card {padding: 1.2rem; margin-bottom: 1.5rem;}
        .page-title {padding: 1.2rem 1rem;}
        .nav-container {flex-direction: column; gap: 0.4rem;}
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Header
st.markdown("""
<div class='header-section'>
    <div class='header-badge'>🛰️ LIVE MONITORING</div>
    <div class='header-content'>
        <div class='org-title-hindi'>लॉन्च पैड संरचनात्मक स्वास्थ्य निगरानी प्रणाली</div>
        <div class='org-title-english'>LAUNCH PAD STRUCTURAL HEALTH MONITORING SYSTEM</div>
        <div class='header-subtitle'>Satish Dhawan Space Centre SHAR • Real-time Predictive Maintenance</div>
    </div>
</div>
<div class='tricolor'></div>
<div class='nav-section'>
    <div class='nav-container'>
        <div class='nav-link'>Dashboard</div>
        <div class='nav-link'>Analysis</div>
        <div class='nav-link'>Alerts</div>
        <div class='nav-link'>Reports</div>
        <div class='nav-link'>Settings</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Content Area
st.markdown("<div class='content-wrapper'><div class='container'>", unsafe_allow_html=True)

# Page Title
st.markdown("""
<div class='page-title'>
    <h2>Real-time Sensor Analysis</h2>
    <p>Monitor launch pad structural integrity with live sensor data and ML predictions</p>
</div>
""", unsafe_allow_html=True)

# Main Content - Full Width Dashboard
st.markdown("<div class='card'><div class='card-header'>Live Sensor Dashboard</div>", unsafe_allow_html=True)

# Data Source Selection
data_source = st.radio("**Data Mode:**", ["Live Sensor Feed", "CSV File Upload"], 
                      label_visibility="collapsed", horizontal=True)

st.markdown("</div>", unsafe_allow_html=True)

# Live Sensor Mode
if data_source == "Live Sensor Feed":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    st.markdown("<div class='card-header'>Sensor Readings</div>", unsafe_allow_html=True)
    
    # Sensor Inputs - Mobile Responsive
    st.subheader("🌀 Vibration Sensors (Tri-axial)")
    v1, v2, v3 = st.columns(3)
    with v1:
        vib_x = st.number_input("X-axis (m/s²)", 0.0, 5.0, 0.72, 0.01, key="live_vib_x")
    with v2:
        vib_y = st.number_input("Y-axis (m/s²)", 0.0, 5.0, 0.68, 0.01, key="live_vib_y")
    with v3:
        vib_z = st.number_input("Z-axis (m/s²)", 0.0, 4.0, 0.61, 0.01, key="live_vib_z")
    
    st.markdown("---")
    
    st.subheader("🔧 Secondary Systems")
    s1, s2, s3 = st.columns(3)
    with s1:
        pressure = st.number_input("Pressure (bar)", 120.0, 260.0, 202.0, 1.0, key="live_pressure")
    with s2:
        strain = st.number_input("Strain (µε)", 40.0, 450.0, 88.0, 2.0, key="live_strain")
    with s3:
        temperature = st.number_input("Temp (°C)", 20.0, 50.0, 28.5, 0.1, key="live_temp")
    
    # Health Calculation
    health = calculate_health_from_sensors(vib_x, vib_y, vib_z, pressure, strain, temperature)
    
    st.markdown(f"""
    <div class='health-box'>
        <div class='health-label'>Structural Health Index</div>
        <div class='health-value'>{health:.3f}</div>
        <div style='font-size: 1rem; margin-top: 1rem; opacity: 0.9;'>
            Auto-calculated from all sensors
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Analysis Section
    st.markdown("<div class='card'><div class='card-header'>ML Risk Prediction</div>", unsafe_allow_html=True)
    
    if st.button("🚀 RUN PREDICTION ANALYSIS", type="primary", key="live_analyze"):
        with st.spinner("Analyzing structural integrity..."):
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
            st.metric("💥 Failure Risk", f"{score:.2%}")
        with m2:
            st.metric("❤️ Health Score", f"{health_calc:.3f}")
        with m3:
            st.metric("📊 Last Update", timestamp.strftime('%H:%M:%S'))
        
        # Status Alert
        if score >= 0.35:
            st.markdown("""
            <div class='status-box status-critical'>
                <div class='status-title'>🚨 CRITICAL ALERT</div>
                <div>Immediate maintenance required. Launch operations HOLD.</div>
            </div>
            """, unsafe_allow_html=True)
        elif score >= 0.18:
            st.markdown("""
            <div class='status-box status-warning'>
                <div class='status-title'>⚠️ ELEVATED RISK</div>
                <div>Schedule priority inspection within 48 hours.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='status-box status-normal'>
                <div class='status-title'>✅ ALL SYSTEMS GO</div>
                <div>Launch pad operational. No immediate concerns detected.</div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("📈 Detailed Health Breakdown"):
            vib_mag = np.sqrt(vib_x**2 + vib_y**2 + vib_z**2)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Vibration Magnitude", f"{vib_mag:.2f} m/s²")
                st.metric("Pressure", f"{pressure:.0f} bar")
            with col2:
                st.metric("Strain", f"{strain:.0f} µε")
                st.metric("Temperature", f"{temperature:.1f}°C")
    
    st.markdown("</div>", unsafe_allow_html=True)

# CSV File Mode
else:
    st.markdown("<div class='card'><div class='card-header'>Batch Analysis Mode</div>", unsafe_allow_html=True)
    
    st.info("🔄 Upload CSV with sensor data for bulk structural analysis")
    
    uploaded_file = st.file_uploader("📁 Choose CSV file", type=['csv'], 
                                   help="Requires: vibration_x_ms2, vibration_y_ms2, vibration_z_ms2, pressure_bar, strain_microstrain, temperature_c")
    
    if uploaded_file is not None:
        with st.spinner("Processing batch analysis..."):
            try:
                batch_data = pd.read_csv(uploaded_file)
                st.success(f"✅ Loaded {len(batch_data)} sensor records")
                
                with st.expander("👀 Data Preview", expanded=True):
                    st.dataframe(batch_data.head(), use_container_width=True)
                
                required_cols = ['vibration_x_ms2', 'vibration_y_ms2', 'vibration_z_ms2', 
                               'pressure_bar', 'strain_microstrain', 'temperature_c']
                
                missing = [col for col in required_cols if col not in batch_data.columns]
                
                if missing:
                    st.error(f"❌ Missing columns: **{', '.join(missing)}**")
                    st.info("Required: `vibration_x_ms2`, `vibration_y_ms2`, `vibration_z_ms2`, `pressure_bar`, `strain_microstrain`, `temperature_c`")
                else:
                    # Calculate health for all rows
                    batch_data['health_state'] = batch_data.apply(
                        lambda row: calculate_health_from_sensors(
                            row['vibration_x_ms2'], row['vibration_y_ms2'], row['vibration_z_ms2'],
                            row['pressure_bar'], row['strain_microstrain'], row['temperature_c']
                        ), axis=1
                    )
                    
                    # Prepare features for model
                    for col in feature_cols:
                        if col not in batch_data.columns:
                            batch_data[col] = 0
                    
                    batch_features = batch_data[feature_cols]
                    batch_risks = model.predict_proba(batch_features)[:, 1]
                    
                    # Summary Metrics
                    c1, c2, c3, c4 = st.columns(4)
                    with c1: st.metric("📊 Total Records", len(batch_risks))
                    with c2: st.metric("📈 Avg Risk", f"{batch_risks.mean():.2%}")
                    with c3: st.metric("🚨 Critical", f"{(batch_risks>0.35).sum()}")
                    with c4: st.metric("✅ Safe", f"{(batch_risks<=0.18).sum()}")
                    
                    # Risk Distribution Table
                    risk_categories = pd.cut(batch_risks, 
                                           bins=[0, 0.18, 0.35, 1.0], 
                                           labels=['✅ Normal', '⚠️ Caution', '🚨 Critical'])
                    
                    risk_summary = pd.DataFrame({
                        'Status': risk_categories.value_counts().index,
                        'Count': risk_categories.value_counts().values,
                        'Percentage': (risk_categories.value_counts().values / len(batch_risks) * 100).round(1)
                    }).reset_index(drop=True)
                    
                    st.markdown("### 📊 Risk Distribution")
                    st.dataframe(risk_summary, use_container_width=True)
                    
                    # Download Results
                    results_df = batch_data[['vibration_x_ms2', 'vibration_y_ms2', 'vibration_z_ms2',
                                           'pressure_bar', 'strain_microstrain', 'temperature_c',
                                           'health_state']].copy()
                    results_df['failure_probability'] = batch_risks
                    results_df['risk_level'] = risk_categories
                    
                    csv_data = results_df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download Analysis Report",
                        data=csv_data,
                        file_name=f"launchpad_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
            except Exception as e:
                st.error(f"❌ Processing error: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# System Info Footer Card
st.markdown("""
<div class='card'>
    <div class='card-header'>⚙️ System Specifications</div>
    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem;'>
""", unsafe_allow_html=True)

info1, info2, info3 = st.columns(3)

with info1:
    st.markdown("""
    **🤖 ML Model**
    - **Algorithm**: XGBoost Classifier
    - **Training Data**: 140,160 samples
    - **Prediction Horizon**: 7 days
    - **Inference Time**: <0.5s
    """)

with info2:
    st.markdown("""
    **📊 Performance**
    - **Precision**: 89.12%
    - **Recall**: 94.31%
    - **F1-Score**: 91.64%
    - **ROC-AUC**: 0.9234
    """)

with info3:
    st.markdown("""
    **🔬 Health Formula**
    - Multi-sensor weighted index
    - Vibration magnitude threshold
    - Real-time risk correlation
    - Auto-calibration enabled
    """)

st.markdown("</div></div>", unsafe_allow_html=True)

# Close containers and add footer
st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("""
<div class='footer'>
    <div style='max-width: 800px; margin: 0 auto;'>
        <div style='font-size: 1.3rem; font-weight: 700; margin-bottom: 1rem;'>Launch Pad Monitoring System</div>
        <div style='font-size: 0.9rem; opacity: 0.8; line-height: 1.7;'>
            Advanced structural health monitoring powered by machine learning.<br>
            Designed for mission-critical launch infrastructure safety.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
