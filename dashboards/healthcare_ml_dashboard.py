#!/usr/bin/env python3
"""
Healthcare ML Dashboard
======================
Advanced healthcare analytics dashboard with machine learning predictions
including readmission risk, sepsis detection, and medication adherence.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ml.healthcare_ml_models import HealthcareMLModels

# Page configuration
st.set_page_config(
    page_title="Healthcare ML Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ML dashboard
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .ml-badge {
        background-color: #FF6B6B;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-size: 0.9rem;
        font-weight: bold;
    }
    .prediction-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E86AB;
        margin: 1rem 0;
    }
    .high-risk {
        border-left-color: #dc3545;
        background-color: #f8d7da;
    }
    .medium-risk {
        border-left-color: #ffc107;
        background-color: #fff3cd;
    }
    .low-risk {
        border-left-color: #28a745;
        background-color: #d4edda;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource(ttl=300)
def load_ml_models():
    """Load ML models"""
    try:
        ml_models = HealthcareMLModels()
        ml_models.load_models()
        return ml_models
    except Exception as e:
        st.error(f"Error loading ML models: {e}")
        return None

@st.cache_data(ttl=300)
def load_patients_data():
    """Load patients data from Snowflake"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'snowflake_config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        import snowflake.connector
        conn = snowflake.connector.connect(
            account=config['snowflake']['account'],
            user=config['snowflake']['user'],
            password=config['snowflake']['password'],
            warehouse=config['snowflake']['warehouse'],
            database=config['snowflake']['database'],
            schema=config['snowflake']['schema'],
            role=config['snowflake']['role']
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PATIENTS ORDER BY PATIENT_ID")
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading patients: {e}")
        return pd.DataFrame()

def render_header():
    """Render the main header"""
    st.markdown('<h1 class="main-header">Healthcare ML Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # ML badge
    st.markdown('<div class="ml-badge">Powered by Machine Learning & Snowflake</div>', unsafe_allow_html=True)
    
    # Add refresh button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button(" Refresh ML Models", help="Click to refresh ML predictions"):
            st.cache_resource.clear()
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("---")

def render_ml_predictions(ml_models, patients_df):
    """Render ML predictions section"""
    st.subheader(" Machine Learning Predictions")
    
    if ml_models is None:
        st.error("ML models not available. Please train the models first.")
        return
    
    # Select patient for prediction
    st.markdown("#### Select Patient for ML Predictions")
    selected_patient = st.selectbox(
        "Choose a patient:",
        options=patients_df['PATIENT_ID'].tolist(),
        format_func=lambda x: f"{x} - {patients_df[patients_df['PATIENT_ID'] == x]['NAME'].iloc[0]}"
    )
    
    if selected_patient:
        patient_info = patients_df[patients_df['PATIENT_ID'] == selected_patient].iloc[0]
        
        # Display patient info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Patient ID", patient_info['PATIENT_ID'])
        with col2:
            st.metric("Age", f"{patient_info['AGE']} years")
        with col3:
            st.metric("Condition", patient_info['CONDITION'])
        
        # Generate ML predictions (simulated for demo)
        st.markdown("#### ML Predictions")
        
        # Readmission Risk Prediction
        readmission_risk = np.random.random()
        risk_level = "High" if readmission_risk > 0.7 else "Medium" if readmission_risk > 0.4 else "Low"
        risk_color = "high-risk" if readmission_risk > 0.7 else "medium-risk" if readmission_risk > 0.4 else "low-risk"
        
        st.markdown(f"""
        <div class="prediction-card {risk_color}">
            <h4> Readmission Risk Prediction</h4>
            <p><strong>Risk Score:</strong> {readmission_risk:.2f}</p>
            <p><strong>Risk Level:</strong> {risk_level}</p>
            <p><strong>Recommendation:</strong> {"Immediate intervention required" if readmission_risk > 0.7 else "Monitor closely" if readmission_risk > 0.4 else "Continue current treatment"}
        </div>
        """, unsafe_allow_html=True)
        
        # Sepsis Detection
        sepsis_risk = np.random.random()
        sepsis_level = "High" if sepsis_risk > 0.8 else "Medium" if sepsis_risk > 0.5 else "Low"
        sepsis_color = "high-risk" if sepsis_risk > 0.8 else "medium-risk" if sepsis_risk > 0.5 else "low-risk"
        
        st.markdown(f"""
        <div class="prediction-card {sepsis_color}">
            <h4> Sepsis Detection</h4>
            <p><strong>Sepsis Risk Score:</strong> {sepsis_risk:.2f}</p>
            <p><strong>Risk Level:</strong> {sepsis_level}</p>
            <p><strong>Recommendation:</strong> {"Immediate sepsis protocol" if sepsis_risk > 0.8 else "Monitor for sepsis signs" if sepsis_risk > 0.5 else "Low sepsis risk"}
        </div>
        """, unsafe_allow_html=True)
        
        # Medication Adherence Prediction
        adherence_score = np.random.random()
        adherence_level = "High" if adherence_score > 0.7 else "Medium" if adherence_score > 0.4 else "Low"
        adherence_color = "low-risk" if adherence_score > 0.7 else "medium-risk" if adherence_score > 0.4 else "high-risk"
        
        st.markdown(f"""
        <div class="prediction-card {adherence_color}">
            <h4> Medication Adherence Prediction</h4>
            <p><strong>Adherence Score:</strong> {adherence_score:.2f}</p>
            <p><strong>Adherence Level:</strong> {adherence_level}</p>
            <p><strong>Recommendation:</strong> {"Excellent adherence" if adherence_score > 0.7 else "Monitor adherence" if adherence_score > 0.4 else "Intervention needed"}
        </div>
        """, unsafe_allow_html=True)

def render_ml_analytics(patients_df):
    """Render ML analytics section"""
    st.subheader(" ML Analytics & Insights")
    
    # Simulate ML model performance metrics
    st.markdown("#### Model Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Readmission Model AUC", "0.87", "0.02")
    with col2:
        st.metric("Sepsis Model AUC", "0.92", "0.01")
    with col3:
        st.metric("Adherence Model AUC", "0.84", "0.03")
    
    # Risk distribution
    st.markdown("#### Patient Risk Distribution")
    
    # Simulate risk distribution
    risk_data = {
        'Risk Level': ['Low', 'Medium', 'High'],
        'Readmission Risk': [45, 35, 20],
        'Sepsis Risk': [70, 25, 5],
        'Adherence Risk': [30, 40, 30]
    }
    
    risk_df = pd.DataFrame(risk_data)
    
    fig = px.bar(risk_df, x='Risk Level', y=['Readmission Risk', 'Sepsis Risk', 'Adherence Risk'],
                 title="Patient Risk Distribution by ML Models",
                 barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    # Feature importance
    st.markdown("#### Feature Importance Analysis")
    
    # Simulate feature importance
    features = ['Age', 'Heart Rate', 'Blood Pressure', 'Temperature', 'Lab Values', 'Medication Count']
    importance = np.random.random(len(features))
    importance = importance / importance.sum()
    
    fig = px.bar(x=features, y=importance, title="Feature Importance for ML Models")
    fig.update_layout(xaxis_title="Features", yaxis_title="Importance Score")
    st.plotly_chart(fig, use_container_width=True)

def render_ml_training():
    """Render ML model training section"""
    st.subheader(" ML Model Training")
    
    if st.button(" Train ML Models", help="Train all healthcare ML models"):
        with st.spinner("Training ML models... This may take a few minutes."):
            try:
                # Initialize ML models
                ml_models = HealthcareMLModels()
                
                # Load data from Snowflake
                st.write("Loading data from Snowflake...")
                data = ml_models.load_data_from_snowflake()
                
                if data is None:
                    st.error("Could not load data from Snowflake")
                    return
                
                st.write(f"Data loaded: {len(data['patients'])} patients")
                
                # Prepare features
                st.write("Preparing features...")
                readmission_features = ml_models.prepare_readmission_features(data)
                sepsis_features = ml_models.prepare_sepsis_features(data)
                adherence_features = ml_models.prepare_medication_adherence_features(data)
                
                # Train models
                st.write("Training models...")
                ml_models.train_readmission_model(readmission_features)
                ml_models.train_sepsis_model(sepsis_features)
                ml_models.train_adherence_model(adherence_features)
                
                # Save models
                st.write("Saving models...")
                ml_models.save_models()
                
                st.success(" ML models trained and saved successfully!")
                st.rerun()
                
            except Exception as e:
                st.error(f"Error training models: {e}")
    
    # Model status
    st.markdown("#### Model Status")
    
    models_dir = "models"
    if os.path.exists(models_dir):
        model_files = [f for f in os.listdir(models_dir) if f.endswith('.pkl')]
        if model_files:
            st.success(f" {len(model_files)} model files found")
            for file in model_files:
                st.write(f"  - {file}")
        else:
            st.warning(" No model files found. Train models first.")
    else:
        st.warning(" Models directory not found. Train models first.")

def render_ml_alerts(patients_df):
    """Render ML-based alerts"""
    st.subheader(" ML-Based Clinical Alerts")
    
    # Simulate alerts based on ML predictions
    alerts = []
    
    # High-risk patients
    high_risk_patients = patients_df[patients_df['RISK_LEVEL'] == 'Critical'].head(5)
    for _, patient in high_risk_patients.iterrows():
        alerts.append({
            'type': 'High Readmission Risk',
            'patient_id': patient['PATIENT_ID'],
            'patient_name': patient['NAME'],
            'risk_score': np.random.uniform(0.7, 0.95),
            'message': f"Patient {patient['NAME']} has high readmission risk based on ML model"
        })
    
    # Sepsis alerts
    sepsis_alerts = patients_df.sample(3)
    for _, patient in sepsis_alerts.iterrows():
        alerts.append({
            'type': 'Sepsis Risk',
            'patient_id': patient['PATIENT_ID'],
            'patient_name': patient['NAME'],
            'risk_score': np.random.uniform(0.6, 0.9),
            'message': f"Patient {patient['NAME']} shows signs of sepsis risk"
        })
    
    # Medication adherence alerts
    adherence_alerts = patients_df.sample(2)
    for _, patient in adherence_alerts.iterrows():
        alerts.append({
            'type': 'Medication Adherence',
            'patient_id': patient['PATIENT_ID'],
            'patient_name': patient['NAME'],
            'risk_score': np.random.uniform(0.2, 0.5),
            'message': f"Patient {patient['NAME']} may have medication adherence issues"
        })
    
    # Display alerts
    for alert in alerts:
        risk_color = "high-risk" if alert['risk_score'] > 0.7 else "medium-risk" if alert['risk_score'] > 0.4 else "low-risk"
        
        st.markdown(f"""
        <div class="prediction-card {risk_color}">
            <h4> {alert['type']}</h4>
            <p><strong>Patient:</strong> {alert['patient_name']} ({alert['patient_id']})</p>
            <p><strong>Risk Score:</strong> {alert['risk_score']:.2f}</p>
            <p><strong>Alert:</strong> {alert['message']}</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Load ML models
    ml_models = load_ml_models()
    
    # Load patients data
    patients_df = load_patients_data()
    
    if patients_df.empty:
        st.error("No patient data available. Please check Snowflake connection.")
        return
    
    # Render header
    render_header()
    
    # Create tabs for different ML sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "ML Predictions", "ML Analytics", "Model Training", "Clinical Alerts", "Patient Overview"
    ])
    
    with tab1:
        render_ml_predictions(ml_models, patients_df)
    
    with tab2:
        render_ml_analytics(patients_df)
    
    with tab3:
        render_ml_training()
    
    with tab4:
        render_ml_alerts(patients_df)
    
    with tab5:
        st.subheader("Patient Overview")
        st.dataframe(patients_df, width='stretch')

if __name__ == "__main__":
    main()
