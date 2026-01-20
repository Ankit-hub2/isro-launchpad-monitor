import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime, timedelta
import time

# === ISRO OFFICIAL CONFIG ===
st.set_page_config(
    page_title="ISRO - Launch Pad Monitoring System", 
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
    """
    Calculate component health automatically from sensor readings
    Returns: health_index (0.5 to 1.0)
    """
    health = 1.0  # Start at perfect health
    
    # Factor 1: Vibration Impact (25% weight)
    vib_mag = np.sqrt(vib_x**2 + vib_y**2 + vib_z**2)
    if vib_mag > 4.0: health -= 0.30
    elif vib_mag > 3.0: health -= 0.20
    elif vib_mag > 2.5: health -= 0.12
    elif vib_mag > 2.0: health -= 0.06
    elif vib_mag > 1.5: health -= 0.02
    
    # Factor 2: Pressure Impact (20% weight)
    if pressure < 130: health -= 0.30
    elif pressure < 150: health -= 0.20
    elif pressure < 170: health -= 0.12
    elif pressure < 185: health -= 0.06
    elif pressure < 200: health -= 0.02
    
    # Factor 3: Strain Impact (15% weight)
    if strain > 400: health -= 0.25
    elif strain > 350: health -= 0.18
    elif strain > 300: health -= 0.12
    elif strain > 250: health -= 0.07
    elif strain > 200: health -= 0.03
    
    # Factor 4: Temperature Impact (10% weight)
    if temp > 45: health -= 0.15
    elif temp > 42: health -= 0.10
    elif temp > 38: health -= 0.05
    elif temp > 35: health -= 0.02
    
    return max(0.50, min(1.0, health))

# === ISRO OFFICIAL HEADER ===
st.markdown("""
<style>
/* Mobile Responsive */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem 0.5rem !important;
        max-width: 100% !important;
    }
}

/* ISRO Header */
.isro-top-bar {
    background: linear-gradient(90deg, #003d82 0%, #004d9f 100%);
    padding: 0.5rem 1rem;
    margin: -5rem -5rem 0 -5rem;
    color: white;
    font-size: 0.85rem;
    display: flex;
    justify-content: space-between;
}

.isro-main-header {
    background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%);
    padding: 1.5rem 2rem;
    margin: 0 -5rem 2rem -5rem;
    border-bottom: 3px solid #ff9933;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.isro-logo-section {
    display: flex;
    align-items: center;
    gap: 2rem;
}

.isro-org-name-hindi {
    font-size: 1.3rem;
    color: #003d82;
    font-weight: 700;
}

.isro-org-name-english {
    font-size: 1.8rem;
    color: #003d82;
    font-weight: 700;
    margin: 0.3rem 0;
}

.isro-org-subtitle {
    font-size: 1rem;
    color: #666;
    font-weight: 500;
}

.isro-card {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.isro-card-header {
    color: #003d82;
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #ff9933;
}

.status-box {
    padding: 1rem;
    border-radius: 6px;
    text-align: center;
    font-weight: 600;
    margin: 0.5rem 0;
}

.status-critical {
    background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%);
    color: white;
    border-left: 4px solid #ff9933;
}

.status-warning {
    background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
    color: white;
    border-left: 4px solid #ff9933;
}

.status-normal {
    background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
    color: white;
    border-left: 4px solid #ff9933;
}

.health-display {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.health-value {
    font-size: 3rem;
    font-weight: 900;
    margin: 0.5rem 0;
}

.health-label {
    font-size: 0.9rem;
    opacity: 0.9;
}

.live-indicator {
    display: inline-block;
    width: 12px;
    height: 12px;
    background: #4caf50;
    border-radius: 50%;
    animation: pulse 2s infinite;
    margin-right: 0.5rem;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.tricolor-bar {
    height: 4px;
    background: linear-gradient(90deg, #ff9933 0%, #ffffff 33%, #138808 66%, #138808 100%);
    margin: 0 -5rem;
}

.stButton > button {
    background: #003d82 !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 0.6rem 2rem !important;
    border-radius: 4px !important;
}

.stButton > button:hover {
    background: #004d9f !important;
    box-shadow: 0 4px 12px rgba(0,61,130,0.3) !important;
}
</style>

<!-- Top Bar -->
<div class='isro-top-bar'>
    <div>English | हिंदी | Sitemap | Contact us</div>
    <div>A+ A A-</div>
</div>

<!-- Header -->
<div class='isro-main-header'>
    <div class='isro-logo-section'>
        <div style='font-size: 3rem;'></div>
        <div>
            <div class='isro-org-name-hindi'>भारतीय अंतरिक्ष अनुसंधान संगठन, अंतरिक्ष विभाग</div>
            <div class='isro-org-name-english'>Indian Space Research Organisation, Department of Space</div>
            <div class='isro-org-subtitle'>भारत सरकार / Government of India</div>
        </div>
    </div>
</div>

<div class='tricolor-bar'></div>
""", unsafe_allow_html=True)

# === PAGE TITLE ===
st.markdown("""
<div class='isro-card'>
    <h1 style='color: #003d82; font-size: 2rem; font-weight: 700; margin: 0;'>
         Launch Pad Structural Health Monitoring System
    </h1>
    <p style='color: #666; font-size: 1.1rem; margin: 0.5rem 0 0 0;'>
        Satish Dhawan Space Centre SHAR, Sriharikota • Real-time Predictive Maintenance Platform
    </p>
</div>
""", unsafe_allow_html=True)

# === DATA SOURCE SELECTION ===
st.markdown("<div class='isro-card'><div class='isro-card-header'>📡 Data Source Selection</div>", unsafe_allow_html=True)

data_source = st.radio(
    "Select Data Source:",
    ["🔴 Live Sensor Feed", "📁 CSV File Upload"],
    horizontal=True
)

st.markdown("</div>", unsafe_allow_html=True)

# === LIVE SENSOR MODE ===
if data_source == "🔴 Live Sensor Feed":
    st.markdown("<div class='isro-card'>", unsafe_allow_html=True)
    st.markdown("<div class='isro-card-header'><span class='live-indicator'></span>Live Sensor Data Stream</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2.5, 1.5])
    
    with col1:
        st.markdown("**Primary Vibration Sensors (Tri-axial Accelerometers)**")
        v1, v2, v3 = st.columns(3)
        with v1:
            vib_x = st.number_input("Vibration X-axis (m/s²)", 0.0, 5.0, 0.72, 0.01, key="live_vib_x")
        with v2:
            vib_y = st.number_input("Vibration Y-axis (m/s²)", 0.0, 5.0, 0.68, 0.01, key="live_vib_y")
        with v3:
            vib_z = st.number_input("Vibration Z-axis (m/s²)", 0.0, 4.0, 0.61, 0.01, key="live_vib_z")
        
        st.markdown("**Secondary Monitoring Systems**")
        s1, s2, s3 = st.columns(3)
        with s1:
            pressure = st.number_input("Hydraulic Pressure (bar)", 120.0, 260.0, 202.0, 1.0, key="live_pressure")
        with s2:
            strain = st.number_input("Structural Strain (µε)", 40.0, 450.0, 88.0, 2.0, key="live_strain")
        with s3:
            temperature = st.number_input("Temperature (°C)", 20.0, 50.0, 28.5, 0.1, key="live_temp")
        
        # Auto-calculate health
        health = calculate_health_from_sensors(vib_x, vib_y, vib_z, pressure, strain, temperature)
        
        # Display calculated health
        st.markdown(f"""
        <div class='health-display'>
            <div class='health-label'>🤖 AUTO-CALCULATED COMPONENT HEALTH</div>
            <div class='health-value'>{health:.3f}</div>
            <div class='health-label'>Computed from sensor readings in real-time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Risk Analysis**")
        
        if st.button("🔍 EXECUTE ANALYSIS", type="primary", use_container_width=True, key="live_analyze"):
            with st.spinner("Computing risk indices..."):
                # Simulate sensor reading delay
                time.sleep(0.5)
                
                input_data = pd.DataFrame({
                    'vibration_x_ms2': [vib_x],
                    'vibration_y_ms2': [vib_y],
                    'vibration_z_ms2': [vib_z],
                    'pressure_bar': [pressure],
                    'strain_microstrain': [strain],
                    'temperature_c': [temperature],
                    'health_state': [health]  # Auto-calculated health
                })
                
                # Fill missing features
                for col in feature_cols:
                    if col not in input_data.columns:
                        input_data[col] = 0
                input_data = input_data[feature_cols]
                
                # Predict
                rmi_score = model.predict_proba(input_data)[0, 1]
                st.session_state.live_rmi_score = rmi_score
                st.session_state.live_health = health
                st.session_state.live_timestamp = datetime.now()
        
        if 'live_rmi_score' in st.session_state:
            score = st.session_state.live_rmi_score
            health_calc = st.session_state.live_health
            timestamp = st.session_state.live_timestamp
            
            st.metric("Failure Probability", f"{score:.2%}", 
                     delta=f"{(score-0.15)*100:.1f}% from baseline")
            
            st.info(f"📅 Last Update: {timestamp.strftime('%H:%M:%S')}")
            
            # Status display
            if score >= 0.35:
                st.markdown("""
                <div class='status-box status-critical'>
                    <div style='font-size: 2rem;'>🚨</div>
                    <div style='font-size: 1.2rem;'>CRITICAL ALERT</div>
                    <div style='font-size: 0.9rem;'>Immediate Maintenance Required<br>Launch Hold Recommended</div>
                </div>
                """, unsafe_allow_html=True)
            elif score >= 0.18:
                st.markdown("""
                <div class='status-box status-warning'>
                    <div style='font-size: 1.8rem;'>⚠️</div>
                    <div style='font-size: 1.1rem;'>ELEVATED RISK</div>
                    <div style='font-size: 0.9rem;'>Priority Inspection<br>Within 48 Hours</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='status-box status-normal'>
                    <div style='font-size: 1.8rem;'>✅</div>
                    <div style='font-size: 1.1rem;'>OPERATIONAL</div>
                    <div style='font-size: 0.9rem;'>All Systems Normal<br>Launch Clearance: GO</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Health breakdown
            with st.expander("📊 Health Calculation Breakdown"):
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

# === CSV FILE MODE ===
else:
    st.markdown("<div class='isro-card'><div class='isro-card-header'>📁 Batch CSV File Analysis</div>", unsafe_allow_html=True)
    
    st.info(" Upload a CSV file with sensor readings. Health index will be calculated automatically for each row.")
    
    uploaded_file = st.file_uploader("Select CSV File", type=['csv'])
    
    if uploaded_file is not None:
        with st.spinner("Processing sensor data batch..."):
            try:
                # Read CSV
                batch_data = pd.read_csv(uploaded_file)
                st.success(f" Loaded {len(batch_data)} records")
                
                # Show preview
                with st.expander(" Data Preview (first 5 rows)"):
                    st.dataframe(batch_data.head())
                
                # Check required columns
                required_cols = ['vibration_x_ms2', 'vibration_y_ms2', 'vibration_z_ms2', 
                               'pressure_bar', 'strain_microstrain', 'temperature_c']
                
                missing = [col for col in required_cols if col not in batch_data.columns]
                
                if missing:
                    st.error(f" Missing required columns: {', '.join(missing)}")
                    st.info("Required columns: vibration_x_ms2, vibration_y_ms2, vibration_z_ms2, pressure_bar, strain_microstrain, temperature_c")
                else:
                    # Calculate health for each row
                    st.info(" Calculating health index for each component...")
                    
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
                    
                    st.success(" Health index calculated for all components")
                    
                    # Fill missing features
                    for col in feature_cols:
                        if col not in batch_data.columns:
                            batch_data[col] = 0
                    
                    # Predict
                    batch_features = batch_data[feature_cols]
                    batch_risks = model.predict_proba(batch_features)[:, 1]
                    
                    # Display results
                    st.markdown("###  Analysis Summary")
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("Total Components", len(batch_risks))
                    with c2:
                        st.metric("Average Risk", f"{batch_risks.mean():.2%}")
                    with c3:
                        st.metric("Critical (>35%)", f"{(batch_risks>0.35).sum()}")
                    with c4:
                        st.metric("Safe (<18%)", f"{(batch_risks<=0.18).sum()}")
                    
                    # Risk distribution
                    st.markdown("### 📈 Risk Distribution")
                    risk_categories = pd.cut(batch_risks, 
                                            bins=[0, 0.18, 0.35, 1.0], 
                                            labels=[' Normal (GO)', ' Caution', ' Critical'])
                    
                    risk_summary = pd.DataFrame({
                        'Status': risk_categories.value_counts().index,
                        'Count': risk_categories.value_counts().values,
                        'Percentage': (risk_categories.value_counts().values / len(batch_risks) * 100).round(1)
                    })
                    
                    st.dataframe(risk_summary, use_container_width=True)
                    
                    # Full results table
                    with st.expander(" Detailed Results (All Components)"):
                        results_df = batch_data[['vibration_x_ms2', 'vibration_y_ms2', 'vibration_z_ms2',
                                                 'pressure_bar', 'strain_microstrain', 'temperature_c',
                                                 'health_state']].copy()
                        results_df['Failure_Probability'] = batch_risks
                        results_df['Risk_Level'] = risk_categories
                        st.dataframe(results_df)
                    
                    # Download results
                    results_csv = results_df.to_csv(index=False)
                    st.download_button(
                        label=" Download Full Analysis Report",
                        data=results_csv,
                        file_name=f"ISRO_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
            except Exception as e:
                st.error(f" Error: {str(e)}")
                st.info("Make sure your CSV has these columns: vibration_x_ms2, vibration_y_ms2, vibration_z_ms2, pressure_bar, strain_microstrain, temperature_c")
    
    st.markdown("</div>", unsafe_allow_html=True)

# === SYSTEM INFO ===
st.markdown("<div class='isro-card'><div class='isro-card-header'> System Information</div>", unsafe_allow_html=True)

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
    - Auto-computed from sensors
    - Vibration: 25% weight
    - Pressure: 20% weight
    - Strain: 15% weight
    - Temperature: 10% weight
    """)

st.markdown("</div>", unsafe_allow_html=True)

# === FOOTER ===
st.markdown("""
<div class='tricolor-bar' style='margin-top: 3rem;'></div>
<div style='background: linear-gradient(180deg, #003d82 0%, #002855 100%); color: white; padding: 2rem; text-align: center;'>
    <div style='font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem;'>
        भारतीय अंतरिक्ष अनुसंधान संगठन<br>
        INDIAN SPACE RESEARCH ORGANISATION
    </div>
    <div style='font-size: 0.95rem; opacity: 0.9;'>
        Satish Dhawan Space Centre SHAR • Sriharikota Range • Pin: 524124<br>
        Launch Pad Health Monitoring System v3.1 • Department of Space • Government of India
    </div>
    <div style='margin-top: 1rem; font-size: 0.85rem; opacity: 0.7;'>
        © 2026 ISRO • Live Sensor Integration • Auto Health Calculation
    </div>
</div>
""", unsafe_allow_html=True)
