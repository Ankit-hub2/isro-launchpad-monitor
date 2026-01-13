import streamlit as st
import pandas as pd
import joblib
import numpy as np
import time
from datetime import datetime, timedelta

# === ISRO OFFICIAL CONFIG ===
st.set_page_config(
    page_title="ISRO - SDSC Launch Pad Monitoring", 
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_isro_system():
    model = joblib.load('isro_launchpad_model.pkl')
    feature_cols = joblib.load('feature_cols.pkl')
    return model, feature_cols

model, feature_cols = load_isro_system()

# === TRICOLOR HEADER - 🇮🇳 ISRO BRANDING ===
st.markdown("""
<style>
.isro-header {
    background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 33%, #138808 66%, #FFFFFF 100%);
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
.isro-title {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #FF9933, #138808);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 !important;
}
.isro-subtitle {
    color: #1a1a1a !important;
    font-weight: 500 !important;
    font-size: 1.2rem !important;
}
</style>
<div class='isro-header'>
    <div style='display: flex; align-items: center; gap: 1rem;'>
        <div style='font-size: 3rem;'>🇮🇳</div>
        <div>
            <h1 class='isro-title'>LAUNCH PAD MONITORING SYSTEM</h1>
            <p class='isro-subtitle'>Satish Dhawan Space Centre • Department of Space • Government of India</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# === LIVE MISSION COUNTDOWN ===
st.markdown("### 🚀 LIVE MISSION STATUS")
mission_col1, mission_col2, mission_col3, mission_col4 = st.columns(4)

# Next mission data (realistic ISRO schedule)
next_missions = {
    "PSLV-C61": "2026-01-20 09:30 IST",
    "GSLV Mk-II F15": "2026-02-05 14:00 IST", 
    "LVM3 M6": "2026-03-12 11:15 IST"
}

with mission_col1:
    mission_name = list(next_missions.keys())[0]
    launch_time = datetime.strptime(next_missions[mission_name], "%Y-%m-%d %H:%M IST")
    time_left = launch_time - datetime.now()
    
    days = time_left.days
    hours = time_left.seconds // 3600
    minutes = (time_left.seconds % 3600) // 60
    
    st.metric("NEXT MISSION", f"**{mission_name}**", 
             f"T-{days}d {hours:02d}:{minutes:02d}")

with mission_col2:
    st.metric("LAUNCH PAD", "LP-2 (First)", "Nominal")

with mission_col3:
    st.metric("VEHICLE MASS", "1750 t", "+2%")

with mission_col4:
    st.metric("STATUS", "🟢 GO", "No holds")

# === MAIN MONITORING SYSTEM ===
st.markdown("---")
st.markdown("<h2 style='color: #1a1a1a; border-left: 5px solid #FF9933; padding-left: 1rem;'>🧪 STRUCTURAL HEALTH ASSESSMENT</h2>", unsafe_allow_html=True)

# Sensor input panels - ISRO control room style
row_sensors, row_risk = st.columns([2, 1])

with row_sensors:
    with st.container():
        st.markdown("#### 📡 Primary Sensors")
        
        # Vibration sensors row
        v1, v2, v3 = st.columns(3)
        with v1:
            st.markdown("**Vibration-X**")
            vib_x = st.number_input("", 0.0, 5.0, 0.72, 0.01, 
                                  help="Tower north-south axis")
        with v2:
            st.markdown("**Vibration-Y**")
            vib_y = st.number_input("", 0.0, 5.0, 0.68, 0.01,
                                  help="Tower east-west axis")
        with v3:
            st.markdown("**Vibration-Z**")
            vib_z = st.number_input("", 0.0, 4.0, 0.61, 0.01,
                                  help="Vertical loads")
        
        # Secondary sensors
        p1, p2 = st.columns(2)
        with p1:
            st.markdown("**Pressure**")
            pressure = st.number_input("", 120.0, 260.0, 202.0, 1.0)
        with p2:
            st.markdown("**Strain**")
            strain = st.number_input("", 40.0, 450.0, 88.0, 2.0)
        
        st.markdown("**Health Index**")
        health = st.slider("", 0.75, 1.00, 0.982, 0.005)

with row_risk:
    st.markdown("#### 🎯 Risk Management Index")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("**ANALYZE**", type="primary", use_container_width=True,
                    help="Execute RMI computation"):
            # Clean ML prediction pipeline
            input_data = pd.DataFrame({
                'vibration_x_ms2': [vib_x], 'vibration_y_ms2': [vib_y],
                'vibration_z_ms2': [vib_z], 'pressure_bar': [pressure],
                'strain_microstrain': [strain], 'health_state': [health],
                'temperature_c': [28.5]
            })
            
            for col in feature_cols:
                if col not in input_data.columns:
                    input_data[col] = 0
            input_data = input_data[feature_cols]
            
            rmi_score = model.predict_proba(input_data)[0, 1]
            st.session_state.rmi_score = rmi_score
    
    # RMI Display
    if 'rmi_score' in st.session_state:
        st.markdown("**RMI Score**")
        st.metric("", f"{st.session_state.rmi_score:.2%}")
        
        # Patriotic status panels
        score = st.session_state.rmi_score
        if score >= 0.35:
            st.markdown("""
            <div style='
                background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%);
                color: white; padding: 1.5rem; border-radius: 12px; margin: 1rem 0;
                text-align: center; box-shadow: 0 8px 32px rgba(183,28,28,0.4);
                border-left: 6px solid #FF9933;
            '>
                <div style='font-size: 2.5rem;'>🚨</div>
                <h3>CRITICAL FAILURE RISK</h3>
                <p style='font-size: 1.1rem; margin: 0.5rem 0;'>IMMEDIATE MAINTENANCE<br>Launch Hold Recommended</p>
            </div>
            """, unsafe_allow_html=True)
        elif score >= 0.18:
            st.markdown("""
            <div style='
                background: linear-gradient(135deg, #f57c00 0%, #ff9800 100%);
                color: white; padding: 1.5rem; border-radius: 12px; margin: 1rem 0;
                text-align: center; box-shadow: 0 8px 32px rgba(245,124,0,0.4);
                border-left: 6px solid #FF9933;
            '>
                <div style='font-size: 2rem;'>⚠️</div>
                <h3>ELEVATED RISK</h3>
                <p style='font-size: 1.1rem;'>Priority Inspection Required</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='
                background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%);
                color: white; padding: 1.5rem; border-radius: 12px; margin: 1rem 0;
                text-align: center; box-shadow: 0 8px 32px rgba(46,125,50,0.4);
                border-left: 6px solid #FF9933;
            '>
                <div style='font-size: 2rem;'>✅</div>
                <h3>LAUNCH READY</h3>
                <p style='font-size: 1.1rem;'>All Systems Nominal</p>
            </div>
            """, unsafe_allow_html=True)

# === ISRO OPERATING LIMITS ===
st.markdown("---")
st.markdown("<h3 style='color: #1a1a1a; border-left: 5px solid #138808; padding-left: 1rem;'>📋 ISRO SDSC OPERATING LIMITS</h3>", unsafe_allow_html=True)

limits_df = pd.DataFrame({
    'Parameter': ['🇮🇳 Vibration X/Y/Z', '🇮🇳 Hydraulic Pressure', '🇮🇳 Structural Strain', '🇮🇳 Health Index'],
    'Normal': ['0.0-2.5 m/s²', '175-250 bar', '50-200 µε', '0.95-1.00'],
    'Caution': ['2.5-3.0 m/s²', '150-175 bar', '200-300 µε', '0.90-0.95'],
    'Critical': ['>3.0 m/s²', '<150 bar', '>300 µε', '<0.90'],
    'Current': [f"{vib_x:.2f}", f"{pressure:.0f}", f"{strain:.0f}", f"{health:.3f}"]
})

st.dataframe(limits_df, use_container_width=True, hide_index=True)

# === BATCH ANALYSIS ===
st.markdown("---")
st.markdown("<h3 style='color: #1a1a1a; border-left: 5px solid #FF9933; padding-left: 1rem;'>🏭 FLEET MONITORING</h3>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("**Upload Sensor Batch**", type=['csv'], 
                               help="sensor_readings.csv • SDSC format")

if uploaded_file is not None:
    with st.spinner("Processing 35K+ sensor readings..."):
        try:
            batch_data = pd.read_csv(uploaded_file)
            batch_data = batch_data[feature_cols].fillna(0)
            batch_risks = model.predict_proba(batch_data)[:, 1]
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Fleet Risk", f"{batch_risks.mean():.2%}")
            with c2:
                st.metric("Critical", f"{(batch_risks>0.35).sum()}")
            with c3:
                st.metric("Ready", f"{(batch_risks<=0.18).sum()}")
            
            # Risk chart
            st.markdown("**Risk Distribution**")
            risk_chart = pd.cut(batch_risks, bins=3, labels=['✅ Ready', '⚠️ Caution', '🚨 Critical'])
            risk_summary = pd.DataFrame({
                'Status': risk_chart.value_counts().index,
                'Components': risk_chart.value_counts().values
            })
            st.dataframe(risk_summary, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Batch processing failed: {str(e)}")

# === ISRO FOOTER - OFFICIAL LOOK ===
st.markdown("""
<div style='
    background: linear-gradient(180deg, #1a1a1a 0%, #0d1b2a 100%);
    padding: 2rem; 
    border-radius: 12px; 
    margin-top: 3rem;
    color: #e0e0e0;
    text-align: center;
'>
    <div style='font-size: 1.1rem; margin-bottom: 1rem;'>
        🇮🇳 <strong>भारतीय अंतरिक्ष अनुसंधान संगठन</strong> | INDIAN SPACE RESEARCH ORGANISATION
    </div>
    <div style='font-size: 0.95rem; max-width: 900px; margin: 0 auto; line-height: 1.6; opacity: 0.8;'>
        Satish Dhawan Space Centre SHAR • Sriharikota Range • Launch Pad Health Monitoring System v3.0<br>
        <strong>GOVERNMENT OF INDIA • DEPARTMENT OF SPACE</strong> • Mission Critical Operations
    </div>
</div>
""", unsafe_allow_html=True)
