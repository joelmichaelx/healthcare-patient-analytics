"""
Healthcare Patient Analytics Dashboard
Streamlit application for healthcare data visualization and analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import os

# Page configuration
st.set_page_config(
    page_title="Healthcare Patient Analytics",
    page_icon="hospital",
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
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)  # Cache for 1 minute to allow for updates
def load_data():
    """Load healthcare data from database with optimization for large datasets"""
    try:
        # Try to load from database (use optimized database for Streamlit Cloud)
        db_path = "healthcare_data_streamlit.db"
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            
            # Load patients (small dataset)
            patients = pd.read_sql_query("SELECT * FROM patients", conn)
            
            # Load recent vital signs (last 30 days) for performance
            vital_signs = pd.read_sql_query("""
                SELECT * FROM vital_signs 
                WHERE datetime(timestamp) >= datetime('now', '-30 days')
                ORDER BY timestamp DESC
                LIMIT 10000
            """, conn)
            
            # Load recent lab results (last 30 days) for performance
            lab_results = pd.read_sql_query("""
                SELECT * FROM lab_results 
                WHERE datetime(timestamp) >= datetime('now', '-30 days')
                ORDER BY timestamp DESC
                LIMIT 5000
            """, conn)
            
            # Load recent medications (last 30 days) for performance
            medications = pd.read_sql_query("""
                SELECT * FROM medications 
                WHERE datetime(timestamp) >= datetime('now', '-30 days')
                ORDER BY timestamp DESC
                LIMIT 10000
            """, conn)
            
            conn.close()
            
            # Convert timestamps to datetime
            if not vital_signs.empty:
                vital_signs['timestamp'] = pd.to_datetime(vital_signs['timestamp'])
            if not lab_results.empty:
                lab_results['timestamp'] = pd.to_datetime(lab_results['timestamp'])
            if not medications.empty:
                medications['timestamp'] = pd.to_datetime(medications['timestamp'])
            
            return {
                'patients': patients,
                'vital_signs': vital_signs,
                'lab_results': lab_results,
                'medications': medications
            }
    except Exception as e:
        st.error(f"Error loading data from database: {e}")
    
    # Fallback to simulated data
    return create_simulated_data()

def create_simulated_data():
    """Create simulated healthcare data"""
    # Patients
    patients = pd.DataFrame([
        {"patient_id": "P001", "name": "John Smith", "age": 65, "gender": "Male", "condition": "Hypertension", "risk_level": "High", "admission_date": "2024-01-15", "room": "201A", "status": "Active"},
        {"patient_id": "P002", "name": "Sarah Johnson", "age": 45, "gender": "Female", "condition": "Diabetes", "risk_level": "Medium", "admission_date": "2024-01-16", "room": "202B", "status": "Active"},
        {"patient_id": "P003", "name": "Michael Brown", "age": 72, "gender": "Male", "condition": "Heart Disease", "risk_level": "Critical", "admission_date": "2024-01-14", "room": "ICU-1", "status": "Critical"},
        {"patient_id": "P004", "name": "Emily Davis", "age": 28, "gender": "Female", "condition": "Pregnancy", "risk_level": "Low", "admission_date": "2024-01-17", "room": "301A", "status": "Active"},
        {"patient_id": "P005", "name": "Robert Wilson", "age": 58, "gender": "Male", "condition": "COPD", "risk_level": "High", "admission_date": "2024-01-13", "room": "302B", "status": "Active"},
        {"patient_id": "P006", "name": "Lisa Anderson", "age": 52, "gender": "Female", "condition": "Cancer", "risk_level": "Critical", "admission_date": "2024-01-12", "room": "ICU-2", "status": "Critical"},
        {"patient_id": "P007", "name": "David Miller", "age": 38, "gender": "Male", "condition": "Pneumonia", "risk_level": "Medium", "admission_date": "2024-01-18", "room": "203A", "status": "Active"},
        {"patient_id": "P008", "name": "Jennifer Taylor", "age": 61, "gender": "Female", "condition": "Stroke", "risk_level": "High", "admission_date": "2024-01-11", "room": "303A", "status": "Active"},
        {"patient_id": "P009", "name": "James Garcia", "age": 47, "gender": "Male", "condition": "Kidney Disease", "risk_level": "High", "admission_date": "2024-01-19", "room": "204B", "status": "Active"},
        {"patient_id": "P010", "name": "Maria Rodriguez", "age": 34, "gender": "Female", "condition": "Appendicitis", "risk_level": "Medium", "admission_date": "2024-01-20", "room": "205A", "status": "Active"}
    ])
    
    # Vital Signs
    vital_signs = []
    for patient_id in ["P001", "P002", "P003", "P004", "P005", "P006", "P007", "P008", "P009", "P010"]:
        for i in range(24):
            timestamp = datetime.now() - timedelta(hours=24-i)
            vital_signs.append({
                "patient_id": patient_id,
                "timestamp": timestamp,
                "heart_rate": np.random.randint(60, 120),
                "blood_pressure_systolic": np.random.randint(100, 180),
                "blood_pressure_diastolic": np.random.randint(60, 110),
                "temperature": round(np.random.uniform(97.0, 100.0), 1),
                "oxygen_saturation": np.random.randint(90, 100),
                "respiratory_rate": np.random.randint(12, 25)
            })
    
    # Lab Results
    lab_results = []
    lab_tests = [
        {"name": "Glucose", "unit": "mg/dL", "range": "70-100", "critical": 300},
        {"name": "Hemoglobin", "unit": "g/dL", "range": "12-16", "critical": 8},
        {"name": "White Blood Cells", "unit": "K/uL", "range": "4.5-11.0", "critical": 20},
        {"name": "Creatinine", "unit": "mg/dL", "range": "0.6-1.2", "critical": 3.0}
    ]
    
    for patient_id in ["P001", "P002", "P003", "P004", "P005", "P006", "P007", "P008", "P009", "P010"]:
        for test in lab_tests:
            # Generate realistic lab values based on test type
            if test["name"] == "Glucose":
                value = np.random.uniform(80, 150)  # Normal to slightly elevated
                critical = value > 200  # Only critical if very high
            elif test["name"] == "Hemoglobin":
                value = np.random.uniform(12, 16)  # Normal range
                critical = value < 8 or value > 18  # Critical if very low or very high
            elif test["name"] == "White Blood Cells":
                value = np.random.uniform(4, 12)  # Normal range
                critical = value < 2 or value > 20  # Critical if very low or very high
            elif test["name"] == "Creatinine":
                value = np.random.uniform(0.6, 1.5)  # Normal to slightly elevated
                critical = value > 3.0  # Critical if very high
            else:
                value = np.random.uniform(50, 200)
                critical = False
            
            lab_results.append({
                "patient_id": patient_id,
                "test_name": test["name"],
                "test_value": round(value, 2),
                "test_unit": test["unit"],
                "reference_range": test["range"],
                "critical_flag": critical,
                "timestamp": datetime.now() - timedelta(hours=np.random.randint(1, 48))
            })
    
    # Medications
    medications = []
    med_list = [
        {"name": "Metformin", "dosage": 500, "unit": "mg", "route": "Oral"},
        {"name": "Lisinopril", "dosage": 10, "unit": "mg", "route": "Oral"},
        {"name": "Atorvastatin", "dosage": 20, "unit": "mg", "route": "Oral"},
        {"name": "Insulin", "dosage": 10, "unit": "units", "route": "Subcutaneous"}
    ]
    
    for patient_id in ["P001", "P002", "P003", "P004", "P005", "P006", "P007", "P008", "P009", "P010"]:
        for med in med_list:
            for i in range(3):
                medications.append({
                    "patient_id": patient_id,
                    "medication_name": med["name"],
                    "dosage": med["dosage"],
                    "unit": med["unit"],
                    "route": med["route"],
                    "administered_by": f"Nurse_{np.random.randint(1, 5):03d}",
                    "timestamp": datetime.now() - timedelta(hours=np.random.randint(1, 72)),
                    "status": "Administered"
                })
    
    return {
        'patients': patients,
        'vital_signs': pd.DataFrame(vital_signs),
        'lab_results': pd.DataFrame(lab_results),
        'medications': pd.DataFrame(medications)
    }

def render_header():
    """Render the main header"""
    st.markdown('<h1 class="main-header">Healthcare Patient Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Add refresh button to clear cache
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Refresh Data", help="Click to refresh data from database"):
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("---")

def render_sidebar(data):
    """Render the sidebar with filters and controls"""
    st.sidebar.title("Filters & Controls")
    
    # Patient filter
    st.sidebar.subheader("Patient Selection")
    selected_patients = st.sidebar.multiselect(
        "Select Patients",
        options=data['patients']['patient_id'].tolist(),
        default=data['patients']['patient_id'].tolist()
    )
    
    # Risk level filter
    st.sidebar.subheader("Risk Level")
    risk_levels = st.sidebar.multiselect(
        "Select Risk Levels",
        options=data['patients']['risk_level'].unique(),
        default=data['patients']['risk_level'].unique()
    )
    
    # Time range filter
    st.sidebar.subheader("Time Range")
    time_range = st.sidebar.selectbox(
        "Select Time Range",
        options=["Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Time"],
        index=1
    )
    
    # Real-time updates
    st.sidebar.subheader("Real-time Updates")
    auto_refresh = st.sidebar.checkbox("Enable Auto-refresh", value=False)
    refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 10, 300, 30)
    
    return {
        'selected_patients': selected_patients,
        'risk_levels': risk_levels,
        'time_range': time_range,
        'auto_refresh': auto_refresh,
        'refresh_interval': refresh_interval
    }

def render_patient_overview(data, filters):
    """Render patient overview section"""
    st.subheader("Patient Overview")
    
    # Filter data based on selections
    filtered_patients = data['patients'][
        (data['patients']['patient_id'].isin(filters['selected_patients'])) &
        (data['patients']['risk_level'].isin(filters['risk_levels']))
    ]
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Patients", len(filtered_patients))
    
    with col2:
        critical_count = len(filtered_patients[filtered_patients['risk_level'] == 'Critical'])
        st.metric("Critical Patients", critical_count)
    
    with col3:
        high_risk_count = len(filtered_patients[filtered_patients['risk_level'] == 'High'])
        st.metric("High Risk", high_risk_count)
    
    with col4:
        active_count = len(filtered_patients[filtered_patients['status'] == 'Active'])
        st.metric("Active Patients", active_count)
    
    # Patient table with pagination
    st.subheader("Patient Details")
    
    # Add pagination for large datasets
    if len(filtered_patients) > 200:
        st.info(f"Showing first 200 of {len(filtered_patients)} patients. Use filters to narrow down results.")
        display_patients = filtered_patients.head(200)
    else:
        display_patients = filtered_patients
    
    st.dataframe(display_patients, use_container_width=True)
    
    # Show summary statistics
    if not filtered_patients.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Age", f"{filtered_patients['age'].mean():.1f} years")
        with col2:
            st.metric("Most Common Condition", filtered_patients['condition'].mode().iloc[0] if not filtered_patients.empty else "N/A")
        with col3:
            st.metric("Risk Distribution", f"{filtered_patients['risk_level'].value_counts().to_dict()}")

def render_vital_signs(data, filters):
    """Render vital signs section"""
    st.subheader("Vital Signs Monitoring")
    
    # Filter vital signs data
    filtered_vitals = data['vital_signs'][
        data['vital_signs']['patient_id'].isin(filters['selected_patients'])
    ]
    
    if not filtered_vitals.empty:
        # Convert timestamp to datetime if it's a string
        if filtered_vitals['timestamp'].dtype == 'object':
            filtered_vitals['timestamp'] = pd.to_datetime(filtered_vitals['timestamp'])
        
        # Latest vital signs for each patient
        latest_vitals = filtered_vitals.groupby('patient_id').last().reset_index()
        
        # Create vital signs chart
        fig = px.line(
            filtered_vitals, 
            x='timestamp', 
            y='heart_rate', 
            color='patient_id',
            title='Heart Rate Trends'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Vital signs table
        st.subheader("Latest Vital Signs")
        st.dataframe(latest_vitals, use_container_width=True)
    else:
        st.info("No vital signs data available for selected patients")

def render_lab_results(data, filters):
    """Render lab results section"""
    st.subheader("Lab Results")
    
    # Filter lab results data
    filtered_labs = data['lab_results'][
        data['lab_results']['patient_id'].isin(filters['selected_patients'])
    ]
    
    if not filtered_labs.empty:
        # Critical values
        critical_labs = filtered_labs[filtered_labs['critical_flag'] == True]
        
        if not critical_labs.empty:
            st.subheader("Critical Lab Values")
            for _, lab in critical_labs.iterrows():
                st.markdown(f"""
                <div class="critical-card">
                    <strong>{lab['test_name']}</strong> for Patient {lab['patient_id']}: 
                    {lab['test_value']} {lab['test_unit']} (Critical)
                </div>
                """, unsafe_allow_html=True)
        
        # Lab results chart
        fig = px.bar(
            filtered_labs, 
            x='test_name', 
            y='test_value', 
            color='patient_id',
            title='Lab Results by Test'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Lab results table
        st.subheader("All Lab Results")
        st.dataframe(filtered_labs, use_container_width=True)
    else:
        st.info("No lab results data available for selected patients")

def render_medications(data, filters):
    """Render medications section"""
    st.subheader("Medication Administration")
    
    # Filter medications data
    filtered_meds = data['medications'][
        data['medications']['patient_id'].isin(filters['selected_patients'])
    ]
    
    if not filtered_meds.empty:
        # Medication summary
        med_summary = filtered_meds.groupby(['patient_id', 'medication_name']).size().reset_index(name='count')
        
        # Medications chart
        fig = px.bar(
            med_summary, 
            x='medication_name', 
            y='count', 
            color='patient_id',
            title='Medication Administration Count'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Medications table
        st.subheader("Medication Records")
        st.dataframe(filtered_meds, use_container_width=True)
    else:
        st.info("No medication data available for selected patients")

def render_alerts(data, filters):
    """Render alerts section"""
    st.subheader("Alerts & Notifications")
    
    # Generate alerts based on data
    alerts = []
    
    # Critical patients alert (only for truly critical patients)
    critical_patients = data['patients'][data['patients']['risk_level'] == 'Critical']
    if not critical_patients.empty:
        for _, patient in critical_patients.iterrows():
            alerts.append({
                'type': 'Critical Patient',
                'patient_id': patient['patient_id'],
                'message': f"Patient {patient['name']} is in critical condition",
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    # Critical lab values (only show a few realistic ones)
    critical_labs = data['lab_results'][data['lab_results']['critical_flag'] == True]
    if not critical_labs.empty:
        # Only show first 2-3 critical lab values to avoid overwhelming
        for _, lab in critical_labs.head(3).iterrows():
            alerts.append({
                'type': 'Critical Lab Value',
                'patient_id': lab['patient_id'],
                'message': f"{lab['test_name']}: {lab['test_value']} {lab['test_unit']} (Critical)",
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    # Add some normal alerts for variety
    if len(alerts) < 3:
        alerts.append({
            'type': 'Medication Due',
            'patient_id': 'P001',
            'message': 'Medication administration due for Patient P001',
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
    
    # Filter data
    filtered_patients = data['patients'][
        (data['patients']['patient_id'].isin(filters['selected_patients'])) &
        (data['patients']['risk_level'].isin(filters['risk_levels']))
    ]
    
    if not filtered_patients.empty:
        # Demographics chart
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                filtered_patients, 
                names='risk_level', 
                title='Risk Level Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(
                filtered_patients, 
                x='age', 
                title='Age Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Condition analysis
        st.subheader("Condition Analysis")
        condition_counts = filtered_patients['condition'].value_counts()
        fig = px.bar(
            x=condition_counts.index, 
            y=condition_counts.values,
            title='Patient Conditions'
        )
        st.plotly_chart(fig, use_container_width=True)

def main():
    """Main application function"""
    # Load data
    data = load_data()
    
    # Render header
    render_header()
    
    # Render sidebar and get filters
    filters = render_sidebar(data)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Patient Overview", "Vital Signs", "Lab Results", 
        "Medications", "Alerts", "Population Health"
    ])
    
    with tab1:
        render_patient_overview(data, filters)
    
    with tab2:
        render_vital_signs(data, filters)
    
    with tab3:
        render_lab_results(data, filters)
    
    with tab4:
        render_medications(data, filters)
    
    with tab5:
        render_alerts(data, filters)
    
    with tab6:
        render_population_health(data, filters)

if __name__ == "__main__":
    main()