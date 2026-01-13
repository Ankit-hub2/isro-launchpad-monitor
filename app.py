import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.set_page_config(page_title="SDSC Launch Pad Monitor", page_icon="🛰️", layout="wide")

@st.cache_resource
def load_model():
    model = joblib.load('isro_launchpad_model.pkl')
    feature_cols = joblib.load('feature_cols.pkl')
    return model, list(feature_cols)

model, feature_cols = load_model()

# Header
st.markdown("""
<div style='background: linear-gradient(90deg, #1a3c5e 0%, #2a5a8e 100%); padding: 1.5rem; border-radius: 10px; color: white;'>
    <h1 style='margin: 0;'>🛰️ SDSC Launch Pad Health Monitoring</h1>
    <p style='margin: 0; opacity: 0.9;'>Satish Dhawan Space Centre | Mission Critical Operations</p>
</div>
""", unsafe_allow_html=True)

# Status row
col1, col2, col3 = st.columns(3)
with col1: st.metric("Status", "🟢 OPERATIONAL")
with col2: st.metric("Updated", "19:45 IST")
with col3: st.metric("8 Components", "100% Active")

st.markdown("---")

# Main monitoring section
row1, row2 = st.columns([2, 1])

with row1:
    st.subheader("🔬 Live Sensor Readings")
    
    c1, c2, c3 = st.columns(3)
    with c1: vib_x = st.number_input("Vibration X", 0.0, 5.0, 0.8, 0.05)
    with c2: vib_y = st.number_input("Vibration Y", 0.0, 5.0, 0.7, 0.05)
    with c3: vib_z = st.number_input("Vibration Z", 0.0, 4.0, 0.6, 0.05)
    
    pressure = st.number_input("Pressure", 100.0, 250.0, 195.0, 2.0)
    strain = st.number_input("Strain (µε)", 50.0, 400.0, 95.0, 5.0)
    health = st.number_input("Health", 0.80, 1.00, 0.98, 0.01)

with row2:
    st.subheader("Risk Assessment")
    
    if st.button("🧠 ANALYZE", type="primary", use_container_width=True):
        # Safe prediction
        input_data = pd.DataFrame({
            'vibration_x_ms2': [vib_x], 'vibration_y_ms2': [vib_y], 
            'vibration_z_ms2': [vib_z], 'pressure_bar': [pressure],
            'temperature_c': [28.5], 'strain_microstrain': [strain],
            'health_state': [health]
        })
        
        for col in feature_cols:
            if col not in input_data.columns:
                input_data[col] = 0
        input_data = input_data[feature_cols]
        
        risk = model.predict_proba(input_data)[0, 1]
        
        # Big risk metric
        st.metric("🚨 7-Day Failure Risk", f"{risk:.1%}")
        
        # Status panels
        if risk > 0.3:
            st.markdown("<div style='background:#d32f2f;color:white;padding:1rem;border-radius:8px;text-align:center;font-size:1.2em;'>🔴 CRITICAL<br>MAINTENANCE NOW</div>", unsafe_allow_html=True)
        elif risk > 0.15:
            st.markdown("<div style='background:#ff9800;color:white;padding:1rem;border-radius:8px;text-align:center;font-size:1.2em;'>🟡 HIGH RISK<br>INSPECT SOON</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background:#4caf50;color:white;padding:1rem;border-radius:8px;text-align:center;font-size:1.2em;'>🟢 NOMINAL<br>LAUNCH READY</div>", unsafe_allow_html=True)

# Thresholds table
st.markdown("### 📋 SDSC Operating Limits")
st.dataframe(pd.DataFrame({
    'Sensor': ['Vibration XY', 'Vibration Z', 'Pressure', 'Strain', 'Health'],
    'Normal': ['0-2.5', '0-2.0', '175-250', '50-200', '0.95-1.0'],
    'Warning': ['2.5-3.0', '2.0-2.5', '150-175', '200-300', '0.90-0.95'],
    'Critical': ['>3.0', '>2.5', '<150', '>300', '<0.90']
}), use_container_width=True)

# Batch analysis
st.markdown("---")
st.subheader("🏭 Fleet Analysis")
uploaded = st.file_uploader("Upload CSV/Excel", type=['csv', 'xlsx'])

if uploaded:
    try:
        if uploaded.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded)
        else:
            data = pd.read_csv(uploaded)
        
        data = data[feature_cols].fillna(0) 
        risks = model.predict_proba(data)[:, 1]
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Average Risk", f"{risks.mean():.1%}")
            st.metric("Critical Count", f"{(risks>0.3).sum()}")
        
        with c2:
            st.subheader("Risk Distribution")
            fig, ax = plt.subplots()
            ax.hist(risks, bins=20, edgecolor='black')
            ax.set_xlabel('Risk Score')
            ax.set_ylabel('Components')
            st.pyplot(fig)
            
    except:
        st.error("File format issue. Use sensor_readings.csv")

st.markdown("---")
st.markdown("<div style='text-align:center;color:#666;padding:1rem'>SDSC Launch Infrastructure | v2.1 | ISRO Compliant</div>", unsafe_allow_html=True)
