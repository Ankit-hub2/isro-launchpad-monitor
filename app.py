import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime

# === PERFECT RESPONSIVE CONFIG ===
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

# === MOBILE-RESPONSIVE CSS (SIMPLIFIED) ===
st.markdown("""
<style>
/* Mobile-First Responsive ISRO Design */
* { box-sizing: border-box; }

.isro-top-bar {
    background: linear-gradient(90deg, #003d82, #004d9f);
    padding: 0.5rem 1rem;
    margin: -0.5rem -0.5rem 0 -0.5rem;
    color: white;
    font-size: clamp(0.75rem, 3vw, 0.9rem);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.isro-main-header {
    background: linear-gradient(135deg, #ffffff, #f8f9fa);
    padding: clamp(1rem, 4vw, 1.5rem) 1rem;
    margin: 0 -0.5rem 1rem -0.5rem;
    border-bottom: 3px solid #ff9933;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.isro-logo-section {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
}

.isro-logo {
    width: clamp(60px, 18vw, 90px);
    height: clamp(60px, 18vw, 90px);
    backgr
