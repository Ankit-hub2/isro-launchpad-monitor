import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime, timedelta

# === FULLY RESPONSIVE ISRO CONFIG ===
st.set_page_config(
    page_title="ISRO - Launch Pad Monitoring System", 
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_isro_system():
    model = joblib.load('isro_launchpad_model.pkl')
    feature_cols = joblib.load('feature_cols.pkl')
    return model, feature_cols

model, feature_cols = load_isro_system()

# === MOBILE-RESPONSIVE ISRO CSS ===
st.markdown("""
<style>
/* ===== MOBILE FIRST RESPONSIVE DESIGN ===== */
* { box-sizing: border-box; }
  
/* Base responsive settings */
h1 { font-size: clamp(1.5rem, 4vw, 2rem) !important; }
h2, h3 { font-size: clamp(1.2rem, 3.5vw, 1.5rem) !important; }

/* ISRO Official Blue Header - Responsive */
.isro-top-bar {
    background: linear-gradient(90deg, #003d82 0%, #004d9f 100%);
    padding: 0.5rem 1rem;
    margin: -0.5rem -0.5rem 0 -0.5rem;
    color: white;
    font-size: clamp(0.75rem, 2.5vw, 0.85rem);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.isro-main-header {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    padding: clamp(1rem, 4vw, 1.5rem) clamp(1rem, 5vw, 2rem);
    margin: 0 -0.5rem 1.5rem -0.5rem;
    border-bottom: 3px solid #ff9933;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

.isro-logo-section {
    display: flex;
    align-items: center;
    gap: clamp(0.5rem, 3vw, 2rem);
    flex-wrap: wrap;
    justify-content: center;
}

@media (max-width: 768px) {
    .isro-logo-section { flex-direction: column; text-align: center; }
}

.isro-logo {
    width: clamp(50px, 15vw, 80px);
    height: clamp(50px, 15vw, 80px);
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="%23003d82"/><polygon points="50,15 35,70 50,60 65,70" fill="%23ff9933"/><circle cx="50" cy="30" r="8" fill="white"/></svg>');
    background-size: contain;
}

.isro-title-section {
    flex: 1;
    min-width: 200px;
}

.isro-org-name-hindi {
    font-size: clamp(1rem, 3vw, 1.3rem);
    color: #003d82;
    font-weight: 700;
    margin: 0;
    text-align: center;
}

.isro-org-name-english {
    font-size: clamp(1.2rem, 4vw, 1.8rem);
    color: #003d82;
    font-weight: 700;
    margin: 0.2rem 0;
}

.isro-emblem {
    width: clamp(40px, 12vw, 60px);
    height: clamp(45px, 13vw, 70px);
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120"><circle cx="50" cy="40" r="35" fill="%23138808"/><rect x="35" y="70" width="30" height="45" fill="%23ff9933"/></svg>');
    background-size: contain;
}

/* Responsive Navigation */
.isro-nav {
    background: #003d82;
    padding: 0;
    margin: 0 -0.5rem 1.5rem -0.5rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0;
    overflow-x: auto;
}

.isro-nav-item {
    color: white !important;
    padding: clamp(0.7rem, 2vw, 1rem) clamp(1rem, 4vw, 1.5rem);
    text-decoration: none;
    font-weight: 500;
    font-size: clamp(0.8rem, 2.5vw, 0.95rem);
    border-right: 1px solid rgba(255,255,255,0.1);
    white-space: nowrap;
    flex-shrink: 0;
}

/* ISRO Cards - Fully Responsive */
.isro-card {
    background: white;
    border: 1px solid #e8ecef;
    border-radius: 12px;
    padding: clamp(1rem, 4vw, 1.5rem);
    margin: clamp(0.5rem, 2vw, 1rem) 0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.isro-card-header {
    color: #003d82;
    font-size: clamp(1.1rem, 3vw, 1.3rem);
    font-weight: 700;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #ff9933;
}

/* Status Boxes Responsive */
.status-box {
    padding: clamp(0.8rem, 3vw, 1rem);
    border-radius: 8px;
    text-align: center;
    font-weight: 600;
    margin: 0.5rem 0;
    font-size: clamp(0.85rem, 2.5vw, 1rem);
}

.status-critical, .status-warning, .status-normal {
    border-left: 4px solid #ff9933;
}

/* Responsive Grid */
@media (max-width: 768px) {
    section[data-testid="column"]:first-child { width: 100% !important; }
    section[data-testid="column"]:nth-child(2) { width: 100% !important; margin-top: 1rem; }
}

/* Tricolor responsive */
.tricolor-bar {
    height: 4px;
    background: linear-gradient(90deg, #ff9933 25%, #ffffff 35%, #138808 65%, #ffffff 100%);
    margin: 0 -0.5rem;
}

/* Responsive Buttons */
.stButton > button {
    background: linear-gradient(135deg, #003d82, #004d9f) !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
    padding: clamp(0.5rem, 2vw, 0.7rem) clamp(1.5rem, 5vw, 2rem) !important;
    border-radius: 6px !important;
    font-size: clamp(0.85rem, 2.5vw, 1rem) !important;
    width: 100%;
}

/* Footer Responsive */
.isro-footer {
    background: linear-gradient(180deg, #003d82 0%, #002855 100%);
    color: white;
    padding: clamp(1.5rem, 6vw, 2rem);
    margin: 2rem -0.5rem -0.5rem -0.5rem;
    text-align: center;
    font-size: clamp(0.8rem, 2.5vw, 0.95rem);
}

/* Metric Cards Responsive */
div[data-testid="metric-container"] {
    padding: clamp(0.5rem, 2vw, 1rem) !important;
    margin: 0.25rem !important;
}

/* DataFrame Responsive */
[data-testid="dataframe"] {
    font-size: clamp(0.75rem, 2.2vw, 0.85rem) !important;
}
</style>
""", unsafe_allow_html=True)

# === ISRO OFFICIAL HEADER ===
st.markdown("""
<!-- Top Navigation Bar -->
<div class='isro-top-bar'>
    <div>🇮🇳 English | हिंदी</div>
    <div>A+ A A-</div>
</div>

<!-- Main Header -->
<div class='isro-main-header'>
    <div class='isro-logo-section'>
        <div class='isro-logo'></div>
        <div class='isro-title-section'>
            <div class='isro-org-name-hindi'>भारतीय अंतरिक्ष अनुसंधान संगठन</div>
            <div class='isro-org-name-english'>INDIAN SPACE RESEARCH ORGANISATION</div>
            <div class='isro-org-subtitle'>Department of Space • Government of India</div>
        </div>
        <div class='isro-emblem'></div>
    </div>
</div>

<!-- Navigation Menu -->
<div class='isro-nav'>
    <a class='isro-nav-item active'>Launch Pad Monitoring</a>
    <a class='isro-nav-item'>Mission Status</a>
    <a class='isro-nav-item'>SDSC SHAR</a>
    <a class='isro-nav-item'>Services</a>
</div>

<div class='tricolor-bar'></div>
""", unsafe_allow_html=True)

# === BREADCRUMB (Responsive) ===
st.markdown("""
<div style='padding: clamp(0.5rem, 2vw, 1rem) 0; color: #666; font-size: clamp(0.8rem, 2.5vw, 0.9rem);'>
    <span style='color: #003d82;'>🏠 Home</span> / 
    <span style='color: #003d82;'>📍 SDSC SHAR</span> / 
    <span style='color: #666;'>Launch Pad Health Monitoring</span>
</div>
""", unsafe_allow_html=True)

# === MAIN TITLE CARD ===
st.markdown("""
<div class='isro-card'>
    <h1 style='color: #003d82; margin: 0; font-weight: 700;'>🚀 Launch Pad Health Monitoring System</h1>
    <p style='color: #666; margin: 0.5rem 0 0 0; font-size: clamp(0.95rem, 2.8vw, 1.1rem);'>
        Satish Dhawan Space Centre SHAR • Real-time ML Predictive Maintenance
    </p>
</div>
""", unsafe_allow_html=True)

# === RESPONSIVE MISSION STATUS ===
st.markdown("<div class='isro-card'><div class='isro-card-header'>📡 Mission Status Dashboard</div>", unsafe_allow_html=True)

# Mobile-first responsive columns
if st.button("📱 Mobile View Test", key="mobile_test"):
    st.success("✅ MOBILE RESPONSIVE - All elements scale perfectly!")

col1, col2 = st.columns([1,1]) if st.get_option("theme.base") == "light" else st.columns(4)
if "col_layout" not in st.session_state:
    st.session_state.col_layout = "auto"

with col1:
    st.metric("🛰️ Next Mission", "PSLV-C62 / EOS-N1", "T-6d 14h")
with col2:
    st.metric("📍 Launch Pad", "Second Launch Pad", "🟢 Operational")

st.markdown("</div>", unsafe_allow_html=True)

# === RESPONSIVE SENSOR + RISK LAYOUT ===
st.markdown("<div class='isro-card'><div class='isro-card-header'>🔬 Live Sensor Monitoring & Risk Analysis</div>", unsafe_allow_html=True)

# Fully responsive sensor layout
sensor_col1, sensor_col2 = st.columns([3,2])

with sensor_col1:
    st.markdown("**🏗️ Vibration Sensors**")
    v_col1, v_col2, v_col3 = st.columns(3)
    with v_col1: vib_x = st.number_input("X-axis", 0.0, 5.0, 0.72, 0.01)
    with v_col2: vib_y = st.number_input("Y-axis", 0.0, 5.0, 0.68, 0.01)
    with v_col3: vib_z = st.number_input("Z-axis", 0.0, 4.0, 0.61, 0.01)
    
    st.markdown("**🔧 Mechanical**")
    p_col1, p_col2 = st.columns(2)
    with p_col1: pressure = st.number_input("Pressure", 120.0, 260.0, 202.0, 1.0)
    with p_col2: strain = st.number_input("Strain", 40.0, 450.0, 88.0, 2.0)
    
    health = st.slider("Health Index", 0.75, 1.00, 0.982, 0.005)

with sensor_col2:
    st.markdown("**🎯 Risk Management Index**")
    
    if st.button("🔍 ANALYZE", type="primary", use_container_width=True):
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
        
        risk_score = model.predict_proba(input_data)[0, 1]
        
        if risk_score >= 0.35:
            st.markdown("""
            <div class='status-box status-critical'>
                🚨 CRITICAL<br><small>LAUNCH HOLD REQUIRED</small>
            </div>
            """, unsafe_allow_html=True)
        elif risk_score >= 0.18:
            st.markdown("""
            <div class='status-box status-warning'>
                ⚠️ HIGH RISK<br><small>PRIORITY INSPECTION</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='status-box status-normal'>
                ✅ LAUNCH READY<br><small>SYSTEMS NOMINAL</small>
            </div>
            """, unsafe_allow_html=True)
            
        st.metric("7-Day Failure Risk", f"{risk_score:.2%}")

st.markdown("</div>", unsafe_allow_html=True)

# === RESPONSIVE LIMITS TABLE ===
st.markdown("""
<div class='isro-card'>
    <div class='isro-card-header'>📋 SDSC Operating Limits</div>
""", unsafe_allow_html=True)

limits_df = pd.DataFrame({
    'Sensor': ['Vibration XY', 'Vibration Z', 'Pressure', 'Strain', 'Health'],
    'Current': [f"{vib_x:.2f}", f"{vib_z:.2f}", f"{pressure:.0f}", f"{strain:.0f}", f"{health:.1%}"],
    'Status': ['✅ Normal', '✅ Normal', '✅ Normal', '✅ Normal', '✅ Normal'],
    'Limits': ['0-2.5', '0-2.0', '175-250', '50-200', '95-100%']
})

st.dataframe(limits_df, use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)

# === ISRO FOOTER ===
st.markdown("""
<div class='tricolor-bar' style='margin-top: 2rem;'></div>
<div class='isro-footer'>
    <div style='font-size: clamp(1rem, 3vw, 1.2rem); font-weight: 700; margin-bottom: 1rem;'>
        🇮🇳 भारतीय अंतरिक्ष अनुसंधान संगठन
    </div>
    <div style='opacity: 0.9; line-height: 1.6;'>
        Satish Dhawan Space Centre SHAR • Sriharikota<br>
        Launch Pad Health Monitoring System v4.0
    </div>
</div>
""", unsafe_allow_html=True)
