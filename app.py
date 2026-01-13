import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime

st.set_page_config(page_title="ISRO - SDSC Live Risk Analyzer", page_icon="🇮🇳", layout="wide")

@st.cache_resource
def load_isro_system():
    model = joblib.load('isro_launchpad_model.pkl')
    feature_cols = joblib.load('feature_cols.pkl')
    return model, feature_cols

model, feature_cols = load_isro_system()

# === TRICOLOR HEADER ===
st.markdown("""
<style>
.isro-header { background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 33%, #138808 66%, #FFFFFF 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; }
.isro-title { font-size: 2.2rem !important; font-weight: 700 !important; background: linear-gradient(135deg, #FF9933, #138808); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
</style>
<div class='isro-header'>
    <div style='display: flex; align-items: center; gap: 1rem;'>
        <div style='font-size: 3rem;'>🇮🇳</div>
        <h1 class='isro-title'>LIVE LAUNCH PAD RISK ANALYZER</h1>
        <p style='color: #1a1a1a; font-weight: 500;'>Satish Dhawan Space Centre SHAR • Real-time Structural Assessment</p>
    </div>
</div>
""", unsafe_allow_html=True)

# === LIVE MISSION COUNTDOWN ===
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🛰️ NEXT MISSION", "PSLV-C61 / EOS-09", "T-6d 14:32")
with col2:
    st.metric("📍 PAD STATUS", "LP-2 ACTIVE", "Nominal")
with col3:
    st.metric("⏰ LIVE UPDATE", datetime.now().strftime("%H:%M:%S IST"))
with col4:
    st.metric("🛠️ SYSTEM", "8/8 OPERATIONAL", "100%")

st.markdown("---")

# === LIVE RISK ANALYZER ===
st.markdown("<h2 style='color: #1a1a1a; border-left: 5px solid #FF9933; padding-left: 1rem;'>🔬 LIVE STRUCTURAL HEALTH ANALYZER</h2>", unsafe_allow_html=True)
st.info("🎯 **Risk updates AUTOMATICALLY** - Slide sensors to see live probability changes")

# === DUAL PANEL LAYOUT ===
left_panel, right_panel = st.columns([2, 1])

# === LEFT: LIVE SENSORS ===
with left_panel:
    st.markdown("### 📡 SENSOR READINGS")
    
    # Vibration cluster
    st.markdown("**🏗️ TOWER VIBRATION**")
    col_v1, col_v2, col_v3 = st.columns(3)
    with col_v1:
        vib_x = st.slider("Vibration-X", 0.0, 5.0, 0.72, 0.01)
    with col_v2:
        vib_y = st.slider("Vibration-Y", 0.0, 5.0, 0.68, 0.01)
    with col_v3:
        vib_z = st.slider("Vibration-Z", 0.0, 4.0, 0.61, 0.01)
    
    # Mechanical cluster  
    st.markdown("**🔧 MECHANICAL SYSTEMS**")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        pressure = st.slider("Pressure", 120.0, 260.0, 202.0, 1.0)
    with col_p2:
        strain = st.slider("Strain", 40.0, 450.0, 88.0, 2.0)
    
    health = st.slider("🩺 Health Index", 0.75, 1.00, 0.982, 0.005)

# === RIGHT: LIVE RISK DISPLAY (Auto-updates) ===
with right_panel:
    st.markdown("### 🎯 **LIVE RISK MANAGEMENT INDEX**")
    
    # AUTOMATIC REAL-TIME PREDICTION
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
    
    live_risk = model.predict_proba(input_data)[0, 1]
    
    # HUGE LIVE RISK DISPLAY
    st.metric("🚨 7-DAY FAILURE RISK", f"{live_risk:.2%}")
    
    # FIXED PROGRESS BAR (float 0-1)
    st.markdown("**Risk Level**")
    st.progress(float(live_risk))
    
    # INSTANT STATUS PANEL
    if live_risk >= 0.35:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #b71c1
