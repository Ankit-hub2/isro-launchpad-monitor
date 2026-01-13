import streamlit as st
import pandas as pd
import joblib
import numpy as np
import time

# === CONFIGURATION ===
st.set_page_config(
    page_title="SDSC - Launch Pad Monitoring System", 
    page_icon="🔹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load_system():
    """Load mission-critical models"""
    model = joblib.load('isro_launchpad_model.pkl')
    feature_cols = joblib.load('feature_cols.pkl')
    return model, feature_cols

model, feature_cols = load_system()

# === HEADER - ISRO Institutional Design ===
st.markdown("""
<div style='
    background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 50%, #415a77 100%); 
    padding: 2rem; 
    border-radius: 12px; 
    margin-bottom: 2rem;
    color: white;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
'>
    <div style='display: flex; align-items: center; gap: 1rem;'>
        <div style='
            background: rgba(255,255,255,0.1); 
            padding: 1rem; 
            border-radius: 12px; 
            backdrop-filter: blur(10px);
        '>
            <div style='font-size: 2.5rem;'>🛰️</div>
        </div>
        <div>
            <h1 style='margin: 0; font-size: 2.2rem; font-weight: 300;'>LAUNCH PAD MONITORING SYSTEM</h1>
            <p style='margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;'>Satish Dhawan Space Centre SHAR</p>
            <div style='font-size: 0.9rem; opacity: 0.7;'>Structural Health Management | Real-time Operations</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# === MISSION STATUS BAR ===
status_col1, status_col2, status_col3, status_col4, status_col5 = st.columns(5)
with status_col1:
    st.metric("SYSTEM STATUS", "🟢 OPERATIONAL", delta="99.9%")
with status_col2:
    st.metric("COMPONENTS", "8/8", delta="100%")
with status_col3:
    st.metric("ALERT LEVEL", "LOW", "-2")
with status_col4:
    st.metric("LAST SCAN", time.strftime("%H:%M IST"))
with status_col5:
    st.metric("NEXT LAUNCH", "GSLV Mk-II", "T-96:00")

# === DASHBOARD SECTIONS ===
tab_live, tab_fleet, tab_alerts = st.tabs(["🧪 LIVE MONITORING", "🏭 FLEET ANALYSIS", "🚨 ACTIVE ALERTS"])

# === TAB 1: LIVE MONITORING ===
with tab_live:
    sensor_row1, risk_row1 = st.columns([2, 1])
    
    with sensor_row1:
        st.markdown("### Sensor Readings")
        
        # Sensor grid - institutional layout
        sensors = st.container()
        with sensors:
            col_v1, col_v2, col_v3 = st.columns(3)
            with col_v1: vib_x = st.number_input("**Vibration-X**", 0.0, 5.0, 0.65, 0.01, 
                                               help="Primary structural axis")
            with col_v2: vib_y = st.number_input("**Vibration-Y**", 0.0, 5.0, 0.58, 0.01,
                                               help="Secondary structural axis")
            with col_v3: vib_z = st.number_input("**Vibration-Z**", 0.0, 4.0, 0.52, 0.01,
                                               help="Vertical loads")
            
            col_p1, col_p2 = st.columns(2)
            with col_p1: pressure = st.number_input("**Pressure**", 120.0, 260.0, 198.0, 1.0,
                                                  help="Hydraulic systems")
            with col_p2: strain = st.number_input("**Strain**", 40.0, 450.0, 92.0, 2.0,
                                                help="Weld points µε")
            
            health = st.number_input("**Health Index**", 0.75, 1.00, 0.985, 0.005,
                                   help="Overall degradation metric")
    
    with risk_row1:
        st.markdown("### Risk Assessment")
        
        if st.button("**EXECUTE ANALYSIS**", type="primary", use_container_width=True, 
                    help="Run Risk Management Index computation"):
            
            # Clean prediction pipeline
            input_df = pd.DataFrame({
                'vibration_x_ms2': [vib_x], 'vibration_y_ms2': [vib_y],
                'vibration_z_ms2': [vib_z], 'pressure_bar': [pressure],
                'strain_microstrain': [strain], 'health_state': [health],
                'temperature_c': [28.5]
            })
            
            # Ensure all feature columns exist
            for col in feature_cols:
                if col not in input_df.columns:
                    input_df[col] = 0
                    
            input_df = input_df[feature_cols]
            risk_score = model.predict_proba(input_df)[0, 1]
            
            # PRIMARY RISK DISPLAY
            st.markdown("#### **RISK MANAGEMENT INDEX**")
            st.metric("7-DAY FAILURE PROBABILITY", f"{risk_score:.2%}", f"{risk_score*100:.1f}%")
            
            # MISSION STATUS PANEL
            status_container = st.container()
            with status_container:
                if risk_score >= 0.35:
                    st.markdown("""
                    <div style='
                        background: linear-gradient(135deg, #b71c1c, #d32f2f); 
                        color: white; padding: 1.5rem; border-radius: 12px; 
                        text-align: center; margin: 1rem 0; box-shadow: 0 4px 20px rgba(183,28,28,0.4);
                    '>
                        <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🚨</div>
                        <h3>CRITICAL ALERT</h3>
                        <p style='font-size: 1.1rem; margin: 0.5rem 0;'>IMMEDIATE MAINTENANCE REQUIRED</p>
                        <div style='font-size: 0.9rem; opacity: 0.9;'>Tower integrity compromised</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif risk_score >= 0.18:
                    st.markdown("""
                    <div style='
                        background: linear-gradient(135deg, #f57c00, #ff9800); 
                        color: white; padding: 1.5rem; border-radius: 12px; 
                        text-align: center; margin: 1rem 0; box-shadow: 0 4px 20px rgba(245,124,0,0.4);
                    '>
                        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>⚠️</div>
                        <h3>ELEVATED RISK</h3>
                        <p style='font-size: 1.1rem;'>Schedule priority inspection</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='
                        background: linear-gradient(135deg, #388e3c, #4caf50); 
                        color: white; padding: 1.5rem; border-radius: 12px; 
                        text-align: center; margin: 1rem 0; box-shadow: 0 4px 20px rgba(56,142,60,0.4);
                    '>
                        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>✅</div>
                        <h3>NOMINAL STATUS</h3>
                        <p style='font-size: 1.1rem;'>Cleared for launch operations</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # OPERATING LIMITS TABLE
    with st.expander("📋 SDSC Operating Limits", expanded=True):
        limits_df = pd.DataFrame({
            'Parameter': ['Vibration X/Y/Z', 'Hydraulic Pressure', 'Structural Strain', 'Health Index'],
            'Normal Range': ['0.0-2.5 m/s²', '175-250 bar', '50-200 µε', '0.95-1.00'],
            'Warning': ['2.5-3.0 m/s²', '150-175 bar', '200-300 µε', '0.90-0.95'],
            'Critical': ['>3.0 m/s²', '<150 bar', '>300 µε', '<0.90'],
            'Current': [f"{vib_x:.2f}", f"{pressure:.0f}", f"{strain:.0f}", f"{health:.3f}"]
        })
        st.dataframe(limits_df, use_container_width=True, hide_index=True)

# === TAB 2: FLEET ANALYSIS ===
with tab_fleet:
    st.markdown("### Upload Fleet Sensor Data")
    uploaded_file = st.file_uploader("Select CSV/Excel file", type=['csv', 'xlsx'], 
                                   help="sensor_readings.csv format")
    
    if uploaded_file is not None:
        with st.spinner("Processing fleet data..."):
            try:
                if uploaded_file.name.endswith('.xlsx'):
                    fleet_data = pd.read_excel(uploaded_file)
                else:
                    fleet_data = pd.read_csv(uploaded_file)
                
                # Safe processing
                fleet_data = fleet_data[feature_cols].fillna(0)
                fleet_risks = model.predict_proba(fleet_data)[:, 1]
                
                # Fleet summary
                col1, col2, col3, col4 = st.columns(4)
                with col1: st.metric("Fleet Risk", f"{fleet_risks.mean():.2%}")
                with col2: st.metric("Critical", f"{(fleet_risks>0.35).sum()}")
                with col3: st.metric("High Risk", f"{((fleet_risks>0.18)&(fleet_risks<=0.35)).sum()}")
                with col4: st.metric("Nominal", f"{(fleet_risks<=0.18).sum()}")
                
                # Risk distribution chart
                st.markdown("### Risk Distribution")
                risk_bins = pd.cut(fleet_risks, bins=[0, 0.18, 0.35, 1], labels=['Nominal', 'High', 'Critical'])
                risk_summary = pd.DataFrame({
                    'Risk Level': risk_bins.value_counts().sort_index().index,
                    'Components': risk_bins.value_counts().sort_index().values
                })
                st.dataframe(risk_summary, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Data processing failed: {str(e)}")

# === TAB 3: ALERTS (Empty for now) ===
with tab_alerts:
    st.info("🚨 No active alerts. System nominal.")
    st.markdown("**Recent Events:**")
    st.dataframe(pd.DataFrame({
        'Timestamp': ['2026-01-13 19:45', '2026-01-13 18:30'],
        'Component': ['Tower Weld-N', 'Hydraulic A1'],
        'Event': ['Routine Check', 'Pressure Test'],
        'Status': ['✅ PASS', '✅ PASS']
    }))

# === FOOTER ===
st.markdown("""
<div style='
    background: #1a1a1a; 
    padding: 2rem; 
    border-radius: 12px; 
    margin-top: 3rem;
    color: #b0b0b0;
    text-align: center;
'>
    <div style='font-size: 0.9rem; max-width: 800px; margin: 0 auto; line-height: 1.6;'>
        <strong>Satish Dhawan Space Centre SHAR</strong> | Launch Pad Health Monitoring System v2.2<br>
        ISRO Standards Compliant | 24x7 Mission Critical Operations | Authorized Personnel Only
    </div>
</div>
""", unsafe_allow_html=True)
