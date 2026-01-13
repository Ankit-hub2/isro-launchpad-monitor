import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime

# === ISRO OFFICIAL CONFIG ===
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

# === LIVE RISK ANALYZER - NO BUTTON NEEDED ===
st.markdown("<h2 style='color: #1a1a1a; border-left: 5px solid #FF9933; padding-left: 1rem;'>🔬 LIVE STRUCTURAL HEALTH ANALYZER</h2>", unsafe_allow_html=True)
st.info("🎯 **Risk updates in REAL-TIME** - Adjust sensors below to see live probability changes")

# === DUAL PANEL LAYOUT ===
left_panel, right_panel = st.columns([2, 1])

# === LEFT: LIVE SENSORS (Real-time input) ===
with left_panel:
    st.markdown("### 📡 SENSOR READINGS")
    
    # Vibration cluster
    with st.container():
        st.markdown("**🏗️ TOWER VIBRATION**")
        col_v1, col_v2, col_v3 = st.columns(3)
        with col_v1:
            vib_x = st.slider("Vibration-X ➡️", 0.0, 5.0, 0.72, 0.01)
        with col_v2:
            vib_y = st.slider("Vibration-Y ➡️", 0.0, 5.0, 0.68, 0.01)
        with col_v3:
            vib_z = st.slider("Vibration-Z ➡️", 0.0, 4.0, 0.61, 0.01)
    
    # Mechanical cluster  
    with st.container():
        st.markdown("**🔧 MECHANICAL SYSTEMS**")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            pressure = st.slider("Pressure ➡️", 120.0, 260.0, 202.0, 1.0)
        with col_p2:
            strain = st.slider("Strain ➡️", 40.0, 450.0, 88.0, 2.0)
    
    # Health index
    health = st.slider("🩺 Health Index ➡️", 0.75, 1.00, 0.982, 0.005)

# === RIGHT: LIVE RISK DISPLAY (Auto-updates) ===
with right_panel:
    st.markdown("### 🎯 **LIVE RISK MANAGEMENT INDEX**")
    
    # === AUTOMATIC REAL-TIME PREDICTION ===
    input_data = pd.DataFrame({
        'vibration_x_ms2': [vib_x], 'vibration_y_ms2': [vib_y],
        'vibration_z_ms2': [vib_z], 'pressure_bar': [pressure],
        'strain_microstrain': [strain], 'health_state': [health],
        'temperature_c': [28.5]
    })
    
    # Safe feature alignment
    for col in feature_cols:
        if col not in input_data.columns:
            input_data[col] = 0
    input_data = input_data[feature_cols]
    
    # LIVE PREDICTION (No button needed!)
    live_risk = model.predict_proba(input_data)[0, 1]
    
    # === HUGE LIVE RISK DISPLAY ===
    st.metric("🚨 7-DAY FAILURE RISK", f"{live_risk:.2%}", delta=None)
    
    # === PROGRESS BAR FOR RISK ===
    st.markdown("**Risk Level**")
    risk_color = "inverse" if live_risk > 0.35 else "normal"
    st.progress(min(live_risk, 1.0))
    
    # === INSTANT STATUS PANEL ===
    st.markdown("**📊 STATUS**")
    if live_risk >= 0.35:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #b71c1c, #d32f2f); color: white; 
                    padding: 1.2rem; border-radius: 10px; text-align: center; 
                    border-left: 6px solid #FF9933; font-weight: bold;'>
            🚨 CRITICAL<br><span style='font-size: 0.9em;'>LAUNCH HOLD • IMMEDIATE MAINTENANCE</span>
        </div>
        """, unsafe_allow_html=True)
    elif live_risk >= 0.18:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f57c00, #ff9800); color: white; 
                    padding: 1.2rem; border-radius: 10px; text-align: center; 
                    border-left: 6px solid #FF9933; font-weight: bold;'>
            ⚠️ HIGH RISK<br><span style='font-size: 0.9em;'>PRIORITY INSPECTION REQUIRED</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #2e7d32, #4caf50); color: white; 
                    padding: 1.2rem; border-radius: 10px; text-align: center; 
                    border-left: 6px solid #FF9933; font-weight: bold;'>
            ✅ LAUNCH READY<br><span style='font-size: 0.9em;'>ALL SYSTEMS NOMINAL</span>
        </div>
        """, unsafe_allow_html=True)

# === CURRENT vs LIMITS TABLE (Live updates) ===
st.markdown("---")
st.markdown("<h3 style='border-left: 5px solid #138808; padding-left: 1rem;'>📋 LIVE STATUS vs SDSC LIMITS</h3>", unsafe_allow_html=True)

live_status = pd.DataFrame({
    'Sensor': ['🇮🇳 Vibration X/Y/Z', '🇮🇳 Pressure', '🇮🇳 Strain', '🇮🇳 Health'],
    'Current': [f"{vib_x:.2f}", f"{pressure:.0f}", f"{strain:.0f}", f"{health:.1%}"],
    'Status': ['✅' if vib_x < 2.5 else '⚠️' if vib_x < 3.0 else '🚨',
              '✅' if pressure > 175 else '⚠️' if pressure > 150 else '🚨',
              '✅' if strain < 200 else '⚠️' if strain < 300 else '🚨',
              '✅' if health > 0.95 else '⚠️' if health > 0.90 else '🚨'],
    'Limit': ['0-2.5 m/s²', '175-250 bar', '50-200 µε', '95-100%']
})
st.dataframe(live_status, use_container_width=True, hide_index=True)

# === BATCH ANALYSIS ===
st.markdown("---")
st.markdown("<h3 style='border-left: 5px solid #FF9933; padding-left: 1rem;'>🏭 FLEET ANALYSIS</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload sensor CSV", type='csv')

if uploaded_file:
    batch_data = pd.read_csv(uploaded_file)
    batch_data = batch_data[feature_cols].fillna(0)
    batch_risk = model.predict_proba(batch_data)[:, 1]
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Fleet Risk", f"{batch_risk.mean():.1%}")
    with col2: st.metric("🚨 Critical", f"{(batch_risk>0.35).sum()}")
    with col3: st.metric("✅ Ready", f"{(batch_risk<0.18).sum()}")

# === ISRO AUTHENTIC FOOTER ===
st.markdown("""
<div style='background: linear-gradient(180deg, #1a1a1a, #0d1b2a); padding: 2rem; border-radius: 12px; 
            color: #e0e0e0; text-align: center; margin-top: 2rem;'>
    <div style='font-size: 1.1rem; margin-bottom: 1rem;'>🇮🇳 भारतीय अंतरिक्ष अनुसंधान संगठन</div>
    <div style='font-size: 0.9rem; opacity: 0.8;'>Satish Dhawan Space Centre SHAR • Launch Pad Live Risk Analyzer v4.0<br>
    Department of Space • Government of India • Mission Critical Operations</div>
</div>
""", unsafe_allow_html=True)
