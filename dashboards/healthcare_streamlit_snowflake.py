#!/usr/bin/env python3
"""
Healthcare Streamlit Dashboard - Snowflake Edition
=================================================
Interactive healthcare analytics dashboard powered by Snowflake data warehouse.
Real-time analytics with enterprise-scale data processing.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import snowflake.connector
from snowflake.connector import DictCursor

# Page configuration
st.set_page_config(
    page_title="Healthcare Analytics - Snowflake",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for healthcare theme
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E86AB;
        margin: 0.5rem 0;
    }
    .alert-card {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
    .critical-card {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
    }
    .snowflake-badge {
        background-color: #29B5E8;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-size: 0.9rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource(ttl=300)  # Cache for 5 minutes
def get_snowflake_connection():
    """Get Snowflake connection"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'snowflake_config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        conn = snowflake.connector.connect(
            account=config['snowflake']['account'],
            user=config['snowflake']['user'],
            password=config['snowflake']['password'],
            warehouse=config['snowflake']['warehouse'],
            database=config['snowflake']['database'],
            schema=config['snowflake']['schema'],
            role=config['snowflake']['role']
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {e}")
        return None

@st.cache_data(ttl=300)
def load_patients_data():
    """Load patients data from Snowflake"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'snowflake_config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
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

@st.cache_data(ttl=300)
def load_vital_signs_data():
    """Load vital signs data from Snowflake"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'snowflake_config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
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
        cursor.execute("""
            SELECT * FROM VITAL_SIGNS 
            WHERE TIMESTAMP >= DATEADD(day, -7, CURRENT_TIMESTAMP())
            ORDER BY TIMESTAMP DESC
        """)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading vital signs: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_lab_results_data():
    """Load lab results data from Snowflake"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'snowflake_config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
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
        cursor.execute("""
            SELECT * FROM LAB_RESULTS 
            WHERE TIMESTAMP >= DATEADD(day, -30, CURRENT_TIMESTAMP())
            ORDER BY TIMESTAMP DESC
        """)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading lab results: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_medications_data():
    """Load medications data from Snowflake"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'snowflake_config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
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
        cursor.execute("""
            SELECT * FROM MEDICATIONS 
            WHERE TIMESTAMP >= DATEADD(day, -30, CURRENT_TIMESTAMP())
            ORDER BY TIMESTAMP DESC
        """)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading medications: {e}")
        return pd.DataFrame()

def render_header():
    """Render the main header"""
    st.markdown('<h1 class="main-header">Healthcare Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Snowflake badge
    st.markdown('<div class="snowflake-badge">Powered by Snowflake Data Warehouse</div>', unsafe_allow_html=True)
    
    # Add refresh button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button(" Refresh Data", help="Click to refresh data from Snowflake"):
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("---")

def render_sidebar(data):
    """Render the sidebar with filters"""
    st.sidebar.title("Filters & Controls")
    
    # Patient filter
    st.sidebar.subheader("Patient Selection")
    if not data['patients'].empty:
        selected_patients = st.sidebar.multiselect(
            "Select Patients",
            options=data['patients']['PATIENT_ID'].tolist(),
            default=data['patients']['PATIENT_ID'].tolist()  # Show all patients by default
        )
    else:
        selected_patients = []
    
    # Risk level filter
    st.sidebar.subheader("Risk Level")
    if not data['patients'].empty:
        risk_levels = st.sidebar.multiselect(
            "Select Risk Levels",
            options=data['patients']['RISK_LEVEL'].unique(),
            default=data['patients']['RISK_LEVEL'].unique()
        )
    else:
        risk_levels = []
    
    # Time range filter
    st.sidebar.subheader("Time Range")
    time_range = st.sidebar.selectbox(
        "Select Time Range",
        options=["Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Time"],
        index=2
    )
    
    return {
        'selected_patients': selected_patients,
        'risk_levels': risk_levels,
        'time_range': time_range
    }

def filter_data(data, filters):
    """Apply filters to the data"""
    if data['patients'].empty:
        return data
    
    # Filter patients
    filtered_patients = data['patients'][
        (data['patients']['PATIENT_ID'].isin(filters['selected_patients'])) &
        (data['patients']['RISK_LEVEL'].isin(filters['risk_levels']))
    ]
    
    # Filter other data based on selected patients
    filtered_vital_signs = data['vital_signs'][
        data['vital_signs']['PATIENT_ID'].isin(filtered_patients['PATIENT_ID'])
    ] if not data['vital_signs'].empty else data['vital_signs']
    
    filtered_lab_results = data['lab_results'][
        data['lab_results']['PATIENT_ID'].isin(filtered_patients['PATIENT_ID'])
    ] if not data['lab_results'].empty else data['lab_results']
    
    filtered_medications = data['medications'][
        data['medications']['PATIENT_ID'].isin(filtered_patients['PATIENT_ID'])
    ] if not data['medications'].empty else data['medications']
    
    return {
        'patients': filtered_patients,
        'vital_signs': filtered_vital_signs,
        'lab_results': filtered_lab_results,
        'medications': filtered_medications
    }

def render_patient_overview(data, filters):
    """Render patient overview section"""
    st.subheader("Patient Overview")
    
    filtered_patients = data['patients']
    
    if filtered_patients.empty:
        st.info("No patient data available.")
        return
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Patients", len(filtered_patients))
    with col2:
        critical_count = len(filtered_patients[filtered_patients['RISK_LEVEL'] == 'Critical'])
        st.metric("Critical Patients", critical_count)
    with col3:
        high_risk_count = len(filtered_patients[filtered_patients['RISK_LEVEL'] == 'High'])
        st.metric("High Risk", high_risk_count)
    with col4:
        active_count = len(filtered_patients[filtered_patients['STATUS'] == 'Active'])
        st.metric("Active Patients", active_count)
    
    # Patient table
    st.subheader("Patient Details")
    st.dataframe(filtered_patients, width='stretch')
    
    # Summary statistics
    if not filtered_patients.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Age", f"{filtered_patients['AGE'].mean():.1f} years")
        with col2:
            most_common_condition = filtered_patients['CONDITION'].mode().iloc[0] if not filtered_patients.empty else "N/A"
            st.metric("Most Common Condition", most_common_condition)
        with col3:
            risk_dist = filtered_patients['RISK_LEVEL'].value_counts().to_dict()
            st.metric("Risk Distribution", str(risk_dist))

def render_vital_signs(data, filters):
    """Render vital signs section"""
    st.subheader("Vital Signs Monitoring")
    
    filtered_vital_signs = data['vital_signs']
    
    if filtered_vital_signs.empty:
        st.info("No vital signs data available.")
        return
    
    # Display latest vital signs
    st.markdown("#### Latest Vital Signs")
    latest_vitals = filtered_vital_signs.sort_values(by='TIMESTAMP', ascending=False).drop_duplicates(subset=['PATIENT_ID']).set_index('PATIENT_ID')
    st.dataframe(latest_vitals[['HEART_RATE', 'BLOOD_PRESSURE_SYSTOLIC', 'BLOOD_PRESSURE_DIASTOLIC', 'TEMPERATURE', 'OXYGEN_SATURATION', 'RESPIRATORY_RATE', 'TIMESTAMP']], width='stretch')
    
    # Plot trends
    st.markdown("#### Vital Signs Trends")
    selected_vital = st.selectbox("Select Vital Sign to Plot", ['HEART_RATE', 'BLOOD_PRESSURE_SYSTOLIC', 'BLOOD_PRESSURE_DIASTOLIC', 'TEMPERATURE', 'OXYGEN_SATURATION', 'RESPIRATORY_RATE'])
    
    if not filtered_vital_signs.empty:
        fig = px.line(
            filtered_vital_signs,
            x="TIMESTAMP",
            y=selected_vital,
            color="PATIENT_ID",
            title=f"{selected_vital.replace('_', ' ').title()} Over Time",
            labels={"TIMESTAMP": "Time", selected_vital: selected_vital.replace('_', ' ').title()}
        )
        st.plotly_chart(fig, use_container_width=True)

def render_lab_results(data, filters):
    """Render lab results section"""
    st.subheader("Lab Results & Critical Values")
    
    filtered_lab_results = data['lab_results']
    
    if filtered_lab_results.empty:
        st.info("No lab results data available.")
        return
    
    # Display critical lab results
    critical_labs = filtered_lab_results[filtered_lab_results['CRITICAL_FLAG'] == True]
    if not critical_labs.empty:
        st.markdown('<div class="critical-card"><h4>Critical Lab Results Detected!</h4></div>', unsafe_allow_html=True)
        st.dataframe(critical_labs[['PATIENT_ID', 'TEST_NAME', 'TEST_VALUE', 'TEST_UNIT', 'REFERENCE_RANGE', 'TIMESTAMP']], width='stretch')
    else:
        st.success("No critical lab results at this time.")
    
    st.markdown("#### All Lab Results")
    st.dataframe(filtered_lab_results[['PATIENT_ID', 'TEST_NAME', 'TEST_VALUE', 'TEST_UNIT', 'REFERENCE_RANGE', 'CRITICAL_FLAG', 'TIMESTAMP']], width='stretch')

def render_medications(data, filters):
    """Render medications section"""
    st.subheader("Medication Administration")
    
    filtered_meds = data['medications']
    
    if filtered_meds.empty:
        st.info("No medication data available.")
        return
    
    st.subheader("Medication Records")
    st.dataframe(filtered_meds, width='stretch')

def render_alerts(data, filters):
    """Render alerts section"""
    st.subheader("Alerts & Notifications")
    
    alerts = []
    
    # Critical patients alert
    critical_patients = data['patients'][data['patients']['RISK_LEVEL'] == 'Critical']
    if not critical_patients.empty:
        for _, patient in critical_patients.iterrows():
            alerts.append({
                'type': 'Critical Patient',
                'patient_id': patient['PATIENT_ID'],
                'message': f"Patient {patient['NAME']} is in critical condition",
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    # Critical lab values
    critical_labs = data['lab_results'][data['lab_results']['CRITICAL_FLAG'] == True]
    if not critical_labs.empty:
        for _, lab in critical_labs.head(3).iterrows():
            alerts.append({
                'type': 'Critical Lab Value',
                'patient_id': lab['PATIENT_ID'],
                'message': f"{lab['TEST_NAME']}: {lab['TEST_VALUE']} {lab['TEST_UNIT']} (Critical)",
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    if alerts:
        for alert in alerts:
            st.markdown(f"""
            <div class="alert-card">
                <strong>{alert['type']}</strong> for Patient {alert['patient_id']}<br>
                {alert['message']}<br>
                <small>Time: {alert['timestamp']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("No critical alerts at this time")

def render_population_health(data, filters):
    """Render population health section"""
    st.subheader("Population Health Analytics")
    
    filtered_patients = data['patients']
    
    if filtered_patients.empty:
        st.info("No patient data available.")
        return
    
    # Age distribution
    st.markdown("#### Age Distribution")
    fig_age = px.histogram(filtered_patients, x="AGE", nbins=10, title="Patient Age Distribution")
    st.plotly_chart(fig_age, width='stretch')
    
    # Condition distribution
    st.markdown("#### Condition Distribution")
    fig_condition = px.pie(filtered_patients, names="CONDITION", title="Patient Condition Distribution")
    st.plotly_chart(fig_condition, width='stretch')
    
    # Risk level distribution
    st.markdown("#### Risk Level Distribution")
    fig_risk = px.pie(filtered_patients, names="RISK_LEVEL", title="Patient Risk Level Distribution",
                    color_discrete_map={'Critical':'red', 'High':'orange', 'Medium':'yellow', 'Low':'green'})
    st.plotly_chart(fig_risk, width='stretch')

def main():
    """Main application function"""
    # Load data from Snowflake
    data = {
        'patients': load_patients_data(),
        'vital_signs': load_vital_signs_data(),
        'lab_results': load_lab_results_data(),
        'medications': load_medications_data()
    }
    
    # Render header
    render_header()
    
    # Render sidebar and get filters
    filters = render_sidebar(data)
    
    # Apply filters to data
    filtered_data = filter_data(data, filters)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Patient Overview", "Vital Signs", "Lab Results", 
        "Medications", "Alerts", "Population Health"
    ])
    
    with tab1:
        render_patient_overview(filtered_data, filters)
    
    with tab2:
        render_vital_signs(filtered_data, filters)
    
    with tab3:
        render_lab_results(filtered_data, filters)
    
    with tab4:
        render_medications(filtered_data, filters)
    
    with tab5:
        render_alerts(filtered_data, filters)
    
    with tab6:
        render_population_health(filtered_data, filters)

if __name__ == "__main__":
    main()
