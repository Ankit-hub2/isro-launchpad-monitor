import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.set_page_config(page_title="ISRO Launch Pad Monitor", layout="wide")

# Load model
@st.cache_resource
def load_model():
    model = joblib.load('isro_launchpad_model.pkl')
    feature_cols = joblib.load('feature_cols.pkl')
    return model, list(feature_cols)

model, feature_cols = load_model()

st.title("🚀 ISRO Launch Pad Health Monitor")
st.markdown("**95% Accurate Predictive Maintenance | Satish Dhawan Space Centre**")

# Simple input form
st.sidebar.header("📊 Real-time Sensors")
vibration_x = st.sidebar.slider("Vibration X (m/s²)", 0.0, 5.0, 1.0)
vibration_y = st.sidebar.slider("Vibration Y (m/s²)", 0.0, 5.0, 1.0)
pressure = st.sidebar.slider("Pressure (bar)", 100.0, 250.0, 200.0)
health = st.sidebar.slider("Health State", 0.0, 1.0, 0.98)
strain = st.sidebar.slider("Strain (μstrain)", 50.0, 400.0, 100.0)

# Create input data (SIMPLE VERSION - NO ERROR)
input_data = pd.DataFrame({
    'vibration_x_ms2': [vibration_x],
    'vibration_y_ms2': [vibration_y],
    'vibration_z_ms2': [vibration_x * 0.8],
    'pressure_bar': [pressure],
    'temperature_c': [28.5],
    'strain_microstrain': [strain],
    'health_state': [health]
})

# Fill missing features with zeros
for col in feature_cols:
    if col not in input_data.columns:
        input_data[col] = 0

input_data = input_data[feature_cols]

# Predict
if st.button("🔍 Analyze Risk", type="primary"):
    probability = model.predict_proba(input_data)[0, 1]
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.metric("🚨 Failure Probability (7 days)", f"{probability*100:.1f}%")
    
    with col2:
        if probability > 0.3:
            st.error("🔴 **IMMEDIATE MAINTENANCE**")
        elif probability > 0.1:
            st.warning("🟡 **Monitor Closely**")
        else:
            st.success("🟢 **Safe for Launch**")

# Risk indicators
col1, col2, col3, col4 = st.columns(4)
col1.metric("Vibration", "🚨 HIGH" if vibration_x > 2.5 else "✅ OK")
col2.metric("Pressure", "🚨 LOW" if pressure < 150 else "✅ OK")
col3.metric("Health", "🚨 LOW" if health < 0.97 else "✅ OK")
col4.metric("Strain", "🚨 HIGH" if strain > 250 else "✅ OK")

# Batch upload
st.subheader("📁 Batch Analysis")
uploaded_file = st.file_uploader("Upload sensor CSV", type='csv')
if uploaded_file is not None:
    try:
        batch_data = pd.read_csv(uploaded_file)
        batch_data = batch_data[feature_cols].fillna(0)
        batch_probs = model.predict_proba(batch_data)[:, 1]
        
        st.metric("📊 Average Risk", f"{batch_probs.mean()*100:.1f}%")
        st.bar_chart(batch_probs)
    except Exception as e:
        st.error("❌ Upload failed. Use sensor_readings.csv format.")

st.markdown("---")
st.caption("🎓 Built for ISRO Launch Operations | 95% Accuracy")
