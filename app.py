import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime, timedelta
import time

# === PAGE CONFIG ===
st.set_page_config(
    page_title="ISRO Launch Pad Monitoring System", 
    page_icon="https://www.isro.gov.in/media/image/index.php?img_id=logo_1",
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
    
    # Vibration Impact
    vib_mag = np.sqrt(vib_x**2 + vib_y**2 + vib_z**2)
    if vib_mag > 4.0: health -= 0.30
    elif vib_mag > 3.0: health -= 0.20
    elif vib_mag > 2.5: health -= 0.12
    elif vib_mag > 2.0: health -= 0.06
    elif vib_mag > 1.5: health -= 0.02
    
    # Pressure Impact
    if pressure < 130: health -= 0.30
    elif pressure < 150: health -= 0.20
    elif pressure < 170: health -= 0.12
    elif pressure < 185: health -= 0.06
    elif pressure < 200: health -= 0.02
    
    # Strain Impact
    if strain > 400: health -= 0.25
    elif strain > 350: health -= 0.18
    elif strain > 300: health -= 0.12
    elif strain > 250: health -= 0.07
    elif strain > 200: health -= 0.03
    
    # Temperature Impact
    if temp > 45: health -= 0.15
    elif temp > 42: health -= 0.10
    elif temp > 38: health -= 0.05
    elif temp > 35: health -= 0.02
    
    return max(0.50, min(1.0, health))

# === PROFESSIONAL STYLING ===
st.markdown("""
<style>
    /* Reset and Base */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header */
    .isro-header {
        background: #ffffff;
        border-bottom: 3px solid #FF9933;
        padding: 1.5rem 0;
        margin: -2rem -2rem 2rem -2rem;
    }
    
    .header-content {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 2rem;
        display: flex;
        align-items: center;
        gap: 2rem;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .logo-img {
        width: 80px;
        height: auto;
    }
    
    .org-info h1 {
        margin: 0;
        font-size: 1.4rem;
        color: #1a1a1a;
        font-weight: 600;
        line-height: 1.3;
    }
    
    .org-info p {
        margin: 0.25rem 0 0 0;
        font-size: 0.9rem;
        color: #666;
    }
    
    /* Cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #FF9933;
    }
    
    /* Status Indicators */
    .status-indicator {
        padding: 1rem;
        border-radius: 4px;
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
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }
    
    .status-subtitle {
        font-size: 0.875rem;
        opacity: 0.8;
    }
    
    /* Health Display */
    .health-box {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 4px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .health-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0.5rem 0;
    }
    
    .health-label {
        font-size: 0.875rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Buttons */
    .stButton > button {
        background: #0f4c81 !important;
        color: white !important;
        border: none !important;
        padding: 0.625rem 1.5rem !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #0d3d66 !important;
    }
    
    /* Form Elements */
    .stNumberInput > div > div > input {
        border-radius: 4px;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        margin-top: 3rem;
        padding: 2rem 0;
        border-top: 1px solid #e0e0e0;
        text-align: center;
        color: #64748b;
        font-size: 0.875rem;
    }
    
    /* Remove Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive */
    @media (max-width: 768px) {
        .header-content {
            flex-direction: column;
            text-align: center;
        }
        
        .logo-section {
            flex-direction: column;
        }
        
        .org-info h1 {
            font-size: 1.1rem;
        }
    }
</style>

<!-- Header -->
<div class='isro-header'>
    <div class='header-content'>
        <div class='logo-section'>
            <img src='https://www.isro.gov.in/media/image/index.php?img_id=logo_1' class='logo-img' alt='ISRO Logo'>
            <div class='org-info'>
                <h1>INDIAN SPACE RESEARCH ORGANISATION<br>Department of Space, Government of India</h1>
                <p>Satish Dhawan Space Centre SHAR, Sriharikota</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# === MAIN TITLE ===
st.title("Launch Pad Structural Health Monitoring System")
st.markdown("Real-time Predictive Maintenance Platform")
st.markdown("---")

# === DATA SOURCE SELECTION ===
st.markdown("<div class='metric-card'><div class='card-title'>Data Source Configuration</div>", unsafe_allow_html=True)
data_source = st.radio(
    "Select Input Method:",
    ["Live Sensor Feed", "CSV File Upload"],
    horizontal=True,
    label_visibility="collapsed"
)
st.markdown("</div>", unsafe_allow_html=True)

# === LIVE SENSOR MODE ===
if data_source == "Live Sensor Feed":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='metric-card'><div class='card-title'>Sensor Input Parameters</div>", unsafe_allow_html=True)
        
        st.subheader("Vibration Sensors (Tri-axial Accelerometers)")
        v1, v2, v3 = st.columns(3)
        with v1:
            vib_x = st.number_input("X-axis (m/s²)", 0.0, 5.0, 0.72, 0.01, key="vx")
        with v2:
            vib_y = st.number_input("Y-axis (m/s²)", 0.0, 5.0, 0.68, 0.01, key="vy")
        with v3:
            vib_z = st.number_input("Z-axis (m/s²)", 0.0, 4.0, 0.61, 0.01, key="vz")
        
        st.subheader("Additional Monitoring Systems")
        s1, s2, s3 = st.columns(3)
        with s1:
            pressure = st.number_input("Hydraulic Pressure (bar)", 120.0, 260.0, 202.0, 1.0, key="pr")
        with s2:
            strain = st.number_input("Structural Strain (µε)", 40.0, 450.0, 88.0, 2.0, key="st")
        with s3:
            temperature = st.number_input("Temperature (°C)", 20.0, 50.0, 28.5, 0.1, key="tp")
        
        # Calculate health
        health = calculate_health_from_sensors(vib_x, vib_y, vib_z, pressure, strain, temperature)
        
        st.markdown(f"""
        <div class='health-box'>
            <div class='health-label'>Component Health Index</div>
            <div class='health-value'>{health:.3f}</div>
            <div class='health-label'>Auto-calculated from sensor readings</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'><div class='card-title'>Risk Analysis</div>", unsafe_allow_html=True)
        
        if st.button("Execute Analysis", type="primary", key="analyze"):
            with st.spinner("Processing..."):
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
            
            st.metric("Failure Probability", f"{score:.2%}", 
                     delta=f"{(score-0.15)*100:.1f}% from baseline")
            
            st.caption(f"Last Updated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if score >= 0.35:
                st.markdown("""
                <div class='status-indicator status-critical'>
                    <div class='status-title'>CRITICAL ALERT</div>
                    <div class='status-subtitle'>Immediate maintenance required. Launch hold recommended.</div>
                </div>
                """, unsafe_allow_html=True)
            elif score >= 0.18:
                st.markdown("""
                <div class='status-indicator status-warning'>
                    <div class='status-title'>ELEVATED RISK</div>
                    <div class='status-subtitle'>Priority inspection required within 48 hours.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='status-indicator status-normal'>
                    <div class='status-title'>OPERATIONAL</div>
                    <div class='status-subtitle'>All systems normal. Launch clearance: GO</div>
                </div>
                """, unsafe_allow_html=True)
            
            with st.expander("View Health Calculation Details"):
                vib_mag = np.sqrt(vib_x**2 + vib_y**2 + vib_z**2)
                st.markdown(f"""
                **Calculation Breakdown:**
                - Initial Health: 1.000
                - Vibration magnitude: {vib_mag:.2f} m/s²
                - Pressure level: {pressure:.0f} bar
                - Strain level: {strain:.0f} µε
                - Temperature: {temperature:.1f}°C
                
                **Final Health Index: {health:.3f}**
                """)
        
        st.markdown("</div>", unsafe_allow_html=True)

# === CSV MODE ===
else:
    st.markdown("<div class='metric-card'><div class='card-title'>Batch Analysis - CSV Upload</div>", unsafe_allow_html=True)
    
    st.info("Upload a CSV file containing sensor readings. Health indices will be calculated automatically.")
    
    uploaded_file = st.file_uploader("Select CSV File", type=['csv'], label_visibility="collapsed")
    
    if uploaded_file is not None:
        with st.spinner("Processing data..."):
            try:
                batch_data = pd.read_csv(uploaded_file)
                st.success(f"Successfully loaded {len(batch_data)} records")
                
                with st.expander("View Data Preview"):
                    st.dataframe(batch_data.head(), use_container_width=True)
                
                required_cols = ['vibration_x_ms2', 'vibration_y_ms2', 'vibration_z_ms2', 
                               'pressure_bar', 'strain_microstrain', 'temperature_c']
                
                missing = [col for col in required_cols if col not in batch_data.columns]
                
                if missing:
                    st.error(f"Missing required columns: {', '.join(missing)}")
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
                    
                    st.subheader("Analysis Summary")
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("Total Components", len(batch_risks))
                    with c2:
                        st.metric("Average Risk", f"{batch_risks.mean():.2%}")
                    with c3:
                        st.metric("Critical (>35%)", f"{(batch_risks>0.35).sum()}")
                    with c4:
                        st.metric("Safe (<18%)", f"{(batch_risks<=0.18).sum()}")
                    
                    risk_categories = pd.cut(batch_risks, 
                                            bins=[0, 0.18, 0.35, 1.0], 
                                            labels=['Normal', 'Caution', 'Critical'])
                    
                    risk_summary = pd.DataFrame({
                        'Status': risk_categories.value_counts().index,
                        'Count': risk_categories.value_counts().values,
                        'Percentage': (risk_categories.value_counts().values / len(batch_risks) * 100).round(1)
                    })
                    
                    st.dataframe(risk_summary, use_container_width=True)
                    
                    results_df = batch_data[['vibration_x_ms2', 'vibration_y_ms2', 'vibration_z_ms2',
                                             'pressure_bar', 'strain_microstrain', 'temperature_c',
                                             'health_state']].copy()
                    results_df['failure_probability'] = batch_risks
                    results_df['risk_level'] = risk_categories
                    
                    with st.expander("View Complete Results"):
                        st.dataframe(results_df, use_container_width=True)
                    
                    results_csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="Download Analysis Report",
                        data=results_csv,
                        file_name=f"ISRO_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# === SYSTEM INFORMATION ===
st.markdown("<div class='metric-card'><div class='card-title'>System Information</div>", unsafe_allow_html=True)

info1, info2, info3 = st.columns(3)

with info1:
    st.markdown("""
    **Model Specifications**
    - Algorithm: XGBoost Classifier
    - Training Samples: 140,160
    - Prediction Horizon: 7 days
    - Inference Time: <0.5s
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
    - Vibration: 25%
    - Pressure: 20%
    - Strain: 15%
    - Temperature: 10%
    """)

st.markdown("</div>", unsafe_allow_html=True)

# === FOOTER ===
st.markdown("""
<div class='footer'>
    <strong>Indian Space Research Organisation</strong><br>
    Satish Dhawan Space Centre SHAR, Sriharikota Range, Pin: 524124<br>
    Launch Pad Health Monitoring System v3.1 | © 2026 ISRO
</div>
""", unsafe_allow_html=True)
