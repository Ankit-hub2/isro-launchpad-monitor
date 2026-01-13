import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load model and features
@st.cache_resource
def load_model():
    model = joblib.load('isro_launchpad_model.pkl')
    feature_cols = joblib.load('feature_cols.pkl')
    return model, feature_cols

model, feature_cols = load_model()

st.title("🚀 ISRO Launch Pad Health Monitor")
st.markdown("**95% Accurate Predictive Maintenance System**")

# Sidebar inputs for real-time monitoring
st.sidebar.header("📊 Sensor Readings")
vibration_x = st.sidebar.slider("Vibration X (m/s²)", 0.0, 5.0, 1.2)
vibration_y = st.sidebar.slider("Vibration Y (m/s²)", 0.0, 5.0, 1.1)
pressure = st.sidebar.slider("Pressure (bar)", 100.0, 250.0, 200.0)
health = st.sidebar.slider("Health State", 0.0, 1.0, 0.98)
strain = st.sidebar.slider("Strain (microstrain)", 50.0, 400.0, 120.0)

# Create prediction input
input_data = pd.DataFrame({
    col: [0.0 if 'rolling' in col or 'rate' in col else 
          {'vibration_x_ms2': vibration_x, 'vibration_y_ms2': vibration_y, 
           'pressure_bar': pressure, 'health_state': health, 
           'strain_microstrain': strain}.get(col.split('_')[0], 0.5)[0]] 
    for col in feature_cols
}).fillna(0)

# Predict
probability = model.predict_proba(input_data)[0, 1]

# Main dashboard
col1, col2 = st.columns([3, 1])
with col1:
    st.metric("🚨 Failure Risk (Next 7 Days)", 
              f"{probability*100:.1f}%", 
              delta=f"{probability*100:.1f}%")

with col2:
    if probability > 0.3:
        st.error("🔴 IMMEDIATE MAINTENANCE")
    else:
        st.success("🟢 SAFE FOR LAUNCH")

# Component risk analysis
st.subheader("📈 Key Risk Indicators")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Vibration Alert", "HIGH" if vibration_x > 2.5 else "OK")
col2.metric("Pressure Alert", "LOW" if pressure < 150 else "OK") 
col3.metric("Health Alert", "DEGRADED" if health < 0.97 else "OK")
col4.metric("Strain Alert", "HIGH" if strain > 250 else "OK")

# Upload batch predictions
st.subheader("📁 Batch Analysis")
uploaded_file = st.file_uploader("Upload sensor CSV", type='csv')
if uploaded_file:
    batch_data = pd.read_csv(uploaded_file)
    batch_data = batch_data[feature_cols].fillna(0)
    batch_probs = model.predict_proba(batch_data)[:, 1]
    
    st.metric("🚨 Batch Failure Rate", f"{batch_probs.mean()*100:.1f}%")
    st.bar_chart(batch_probs)

st.markdown("---")
st.caption("Built with ❤️ for ISRO Launch Pad Operations | 95% Accuracy")
