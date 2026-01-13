import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Config - ISRO mission control style
st.set_page_config(
    page_title="SDSC Launch Pad Health Monitoring System", 
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_model():
    model = joblib.load('isro_launchpad_model.pkl')
    feature_cols = joblib.load('feature_cols.pkl')
    return model, list(feature_cols)

model, feature_cols = load_model()

# Header - ISRO mission control style
st.markdown("""
    <div style='background-color: #1a3c5e; padding: 1rem; border-radius: 8px; color: white;'>
        <h1 style='margin: 0; color: white;'>🛰️ SDSC Launch Pad Health Monitoring System</h1>
        <p style='margin: 0; opacity: 0.9;'>Satish Dhawan Space Centre | Real-time Structural Health Assessment</p>
    </div>
""", unsafe_allow_html=True)

# Status bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("System Status", "OPERATIONAL", "🟢")
with col2:
    st.metric("Last Update", datetime.now().strftime("%H:%M:%S"), "1m ago")
with col3:
    st.metric("Components Active", "8/8", "+0")
with col4:
    st.metric("Next Launch", "PSLV-C60", "T-72h")

st.markdown("---")

# Main dashboard tabs
tab1, tab2, tab3 = st.tabs(["📊 Live Monitoring", "📈 Trends", "⚙️ Batch Analysis"])

with tab1:
    # Live sensor layout - mission control panels
    row1_col1, row1_col2 = st.columns([2, 1])
    
    with row1_col1:
        st.subheader("Primary Sensors")
        
        sensor_col1, sensor_col2, sensor_col3 = st.columns(3)
        with sensor_col1:
            vib_x = st.number_input("**Vibration X**", 0.0, 5.0, 0.8, 0.05, 
                                  help="Tower structure primary axis")
        with sensor_col2:
            vib_y = st.number_input("**Vibration Y**", 0.0, 5.0, 0.7, 0.05,
                                  help="Tower structure secondary axis")  
        with sensor_col3:
            vib_z = st.number_input("**Vibration Z**", 0.0, 4.0, 0.6, 0.05,
                                  help="Vertical acceleration")
        
        pressure = st.number_input("**Hydraulic Pressure**", 100.0, 250.0, 195.0, 2.0,
                                 help="Umbilical tower actuators")
        
        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            strain = st.number_input("**Structural Strain**", 50.0, 400.0, 95.0, 5.0,
                                   help="Tower weld points µε")
        with row2_col2:
            health = st.number_input("**Health Index**", 0.80, 1.00, 0.98, 0.01,
                                   help="Composite degradation metric")
    
    with row1_col2:
        st.subheader("Risk Assessment")
        
        if st.button("🧠 COMPUTE RMI", type="primary", use_container_width=True):
            # Prediction logic
            input_data = pd.DataFrame({
                'vibration_x_ms2': [vib_x],
                'vibration_y_ms2': [vib_y],
                'vibration_z_ms2': [vib_z],
                'pressure_bar': [pressure],
                'temperature_c': [28.5],
                'strain_microstrain': [strain],
                'health_state': [health]
            })
            
            # Safe column handling
            for col in feature_cols:
                if col not in input_data.columns:
                    input_data[col] = 0
            input_data = input_data[feature_cols]
            
            risk_score = model.predict_proba(input_data)[0, 1]
            
            # Mission-critical display
            risk_col1, risk_col2 = st.columns(2)
            with risk_col1:
                st.metric("🚨 Risk Management Index", f"{risk_score:.1%}", 
                         delta=f"{risk_score*100:.0f}%")
            
            with risk_col2:
                if risk_score > 0.3:
                    st.markdown("""
                        <div style='background: #d32f2f; color: white; padding: 1rem; 
                        border-radius: 8px; text-align: center; font-weight: bold;'>
                            ⛔ CRITICAL ALERT<br>IMMEDIATE MAINTENANCE REQUIRED
                        </div>
                    """, unsafe_allow_html=True)
                elif risk_score > 0.12:
                    st.markdown("""
                        <div style='background: #ff9800; color: white; padding: 1rem; 
                        border-radius: 8px; text-align: center; font-weight: bold;'>
                            ⚠️  HIGH RISK<br>Schedule Inspection
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div style='background: #4caf50; color: white; padding: 1rem; 
                        border-radius: 8px; text-align: center; font-weight: bold;'>
                            ✅ NOMINAL<br>Launch Operations Cleared
                        </div>
                    """, unsafe_allow_html=True)
    
    # Threshold table - mission control style
    st.markdown("### Sensor Limits (SDSC Standards)")
    st.dataframe(pd.DataFrame({
        'Parameter': ['Vibration X/Y', 'Vibration Z', 'Pressure', 'Strain', 'Health'],
        'Normal': ['<2.5 m/s²', '<2.0 m/s²', '>175 bar', '<200 µε', '>0.95'],
        'Warning': ['2.5-3.0 m/s²', '2.0-2.5 m/s²', '150-175 bar', '200-300 µε', '0.90-0.95'],
        'Critical': ['>3.0 m/s²', '>2.5 m/s²', '<150 bar', '>300 µε', '<0.90']
    }), use_container_width=True)

with tab2:
    st.subheader("Historical Trends")
    st.info("📈 Component degradation trends coming soon")
    # Placeholder for time-series charts

with tab3:
    st.subheader("Fleet Analysis")
    uploaded_file = st.file_uploader("Select sensor batch file", type=['csv', 'xlsx'])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.xlsx'):
                data = pd.read_excel(uploaded_file)
            else:
                data = pd.read_csv(uploaded_file)
            
            data = data[feature_cols].fillna(0)
            risks = model.predict_proba(data)[:, 1]
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Fleet Average Risk", f"{risks.mean():.1%}")
                st.metric("Critical Components", f"{(risks > 0.3).sum()}")
            
            with col2:
                fig = px.histogram(risks, nbins=20, title="Risk Distribution")
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"File format error: {str(e)}")

# Footer - ISRO style
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1rem; color: #666;'>
    <p>Satish Dhawan Space Centre | Structural Health Monitoring System v2.1</p>
    <p>Mission Critical | Operational 24x7 | ISRO Standards Compliant</p>
</div>
""", unsafe_allow_html=True)
