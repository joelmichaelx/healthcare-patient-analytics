#!/usr/bin/env python3
"""
Healthcare Streaming Dashboard
=============================
Real-time streaming dashboard for healthcare data processing
with Kafka integration and live data monitoring.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time
import threading
import queue
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from streaming.kafka_consumer import HealthcareKafkaConsumer
from streaming.kafka_producer import HealthcareKafkaProducer

# Page configuration
st.set_page_config(
    page_title="Healthcare Streaming Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for streaming dashboard
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .streaming-badge {
        background-color: #FF6B6B;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-size: 0.9rem;
        font-weight: bold;
    }
    .streaming-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E86AB;
        margin: 1rem 0;
    }
    .alert-card {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
    }
    .success-card {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'streaming_data' not in st.session_state:
    st.session_state.streaming_data = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'kafka_consumer' not in st.session_state:
    st.session_state.kafka_consumer = None
if 'kafka_producer' not in st.session_state:
    st.session_state.kafka_producer = None
if 'streaming_active' not in st.session_state:
    st.session_state.streaming_active = False

def render_header():
    """Render the main header"""
    st.markdown('<h1 class="main-header">Healthcare Streaming Dashboard</h1>', unsafe_allow_html=True)
    
    # Streaming badge
    st.markdown('<div class="streaming-badge">Real-time Data Streaming with Apache Kafka</div>', unsafe_allow_html=True)
    
    # Control buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(" Start Streaming", help="Start Kafka data streaming"):
            start_streaming()
    
    with col2:
        if st.button(" Stop Streaming", help="Stop Kafka data streaming"):
            stop_streaming()
    
    with col3:
        if st.button(" Refresh Data", help="Refresh streaming data"):
            st.rerun()
    
    with col4:
        if st.button(" Clear Data", help="Clear all streaming data"):
            clear_streaming_data()
    
    st.markdown("---")

def start_streaming():
    """Start Kafka streaming"""
    try:
        # Try to initialize producer
        if st.session_state.kafka_producer is None:
            st.session_state.kafka_producer = HealthcareKafkaProducer()
            if not st.session_state.kafka_producer.connect():
                st.warning(" Kafka not available - running in demo mode with simulated data")
                st.session_state.kafka_producer = None
        
        # Try to initialize consumer
        if st.session_state.kafka_consumer is None:
            st.session_state.kafka_consumer = HealthcareKafkaConsumer()
            if not st.session_state.kafka_consumer.connect():
                st.warning(" Kafka not available - running in demo mode with simulated data")
                st.session_state.kafka_consumer = None
        
        # Start streaming (demo mode if Kafka not available)
        st.session_state.streaming_active = True
        if st.session_state.kafka_producer and st.session_state.kafka_consumer:
            st.success(" Kafka streaming started successfully!")
        else:
            st.success(" Demo streaming started successfully!")
        
    except Exception as e:
        st.warning(f" Kafka connection failed - running in demo mode: {e}")
        st.session_state.streaming_active = True

def stop_streaming():
    """Stop Kafka streaming"""
    try:
        st.session_state.streaming_active = False
        
        if st.session_state.kafka_consumer:
            st.session_state.kafka_consumer.stop_consuming()
        
        if st.session_state.kafka_producer:
            st.session_state.kafka_producer.close()
        
        st.success(" Streaming stopped successfully!")
        
    except Exception as e:
        st.error(f"Error stopping streaming: {e}")

def clear_streaming_data():
    """Clear all streaming data"""
    st.session_state.streaming_data = []
    st.session_state.alerts = []
    st.success(" Streaming data cleared!")

def simulate_streaming_data():
    """Simulate streaming data for demo purposes"""
    if not st.session_state.streaming_active:
        return
    
    # Generate simulated data
    patient_ids = [f"P{i:03d}" for i in range(1, 11)]
    
    # Vital signs data
    vital_data = {
        'patient_id': np.random.choice(patient_ids),
        'timestamp': datetime.now().isoformat(),
        'heart_rate': np.random.randint(60, 120),
        'blood_pressure_systolic': np.random.randint(100, 180),
        'blood_pressure_diastolic': np.random.randint(60, 110),
        'temperature': round(np.random.uniform(97.0, 100.0), 1),
        'oxygen_saturation': np.random.randint(90, 100),
        'respiratory_rate': np.random.randint(12, 25),
        'type': 'vital_signs'
    }
    
    # Lab results data
    lab_data = {
        'patient_id': np.random.choice(patient_ids),
        'timestamp': datetime.now().isoformat(),
        'test_name': np.random.choice(['Glucose', 'Hemoglobin', 'White Blood Cells', 'Creatinine']),
        'test_value': round(np.random.uniform(50, 200), 2),
        'test_unit': 'mg/dL',
        'critical_flag': np.random.choice([True, False], p=[0.1, 0.9]),
        'type': 'lab_results'
    }
    
    # Medication data
    med_data = {
        'patient_id': np.random.choice(patient_ids),
        'timestamp': datetime.now().isoformat(),
        'medication_name': np.random.choice(['Metformin', 'Lisinopril', 'Atorvastatin', 'Insulin']),
        'dosage': np.random.randint(5, 50),
        'unit': 'mg',
        'status': np.random.choice(['Administered', 'Scheduled', 'Missed'], p=[0.7, 0.2, 0.1]),
        'type': 'medications'
    }
    
    # Add to streaming data
    data_types = [vital_data, lab_data, med_data]
    selected_data = np.random.choice(data_types)
    
    st.session_state.streaming_data.append(selected_data)
    
    # Keep only last 100 records
    if len(st.session_state.streaming_data) > 100:
        st.session_state.streaming_data = st.session_state.streaming_data[-100:]

def render_streaming_status():
    """Render streaming status"""
    st.subheader(" Streaming Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.streaming_active:
            if st.session_state.kafka_producer and st.session_state.kafka_consumer:
                status = "🟢 Active (Kafka)"
            else:
                status = "🟡 Active (Demo)"
        else:
            status = " Inactive"
        st.metric("Streaming Status", status)
    
    with col2:
        st.metric("Data Points", len(st.session_state.streaming_data))
    
    with col3:
        st.metric("Alerts", len(st.session_state.alerts))
    
    # Kafka connection status
    if st.session_state.kafka_consumer:
        stats = st.session_state.kafka_consumer.get_consumer_stats()
        if stats:
            st.info(f"Kafka Consumer: {stats['group_id']} - Queue Size: {stats['queue_size']}")

def render_live_data():
    """Render live streaming data"""
    st.subheader(" Live Streaming Data")
    
    if not st.session_state.streaming_data:
        st.info("No streaming data available. Start streaming to see data.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(st.session_state.streaming_data)
    
    # Display recent data
    st.markdown("#### Recent Data Points")
    st.dataframe(df.tail(10), width='stretch')
    
    # Data type distribution
    if 'type' in df.columns:
        st.markdown("#### Data Type Distribution")
        type_counts = df['type'].value_counts()
        fig = px.pie(values=type_counts.values, names=type_counts.index, title="Streaming Data Types")
        st.plotly_chart(fig, use_container_width=True)
    
    # Timeline of data
    if 'timestamp' in df.columns:
        st.markdown("#### Data Timeline")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        timeline_data = df.groupby([df['timestamp'].dt.floor('T'), 'type']).size().reset_index(name='count')
        
        fig = px.line(timeline_data, x='timestamp', y='count', color='type', 
                     title="Data Points Over Time")
        st.plotly_chart(fig, use_container_width=True)

def render_vital_signs_monitoring():
    """Render vital signs monitoring"""
    st.subheader(" Vital Signs Monitoring")
    
    # Filter vital signs data
    vital_data = [d for d in st.session_state.streaming_data if d.get('type') == 'vital_signs']
    
    if not vital_data:
        st.info("No vital signs data available.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(vital_data)
    
    # Latest vital signs
    st.markdown("#### Latest Vital Signs")
    latest_vitals = df.sort_values('timestamp', ascending=False).head(5)
    st.dataframe(latest_vitals, width='stretch')
    
    # Vital signs trends
    if len(df) > 1:
        st.markdown("#### Vital Signs Trends")
        
        # Heart rate trend
        fig_hr = px.line(df, x='timestamp', y='heart_rate', color='patient_id',
                        title="Heart Rate Trends")
        st.plotly_chart(fig_hr, width='stretch')
        
        # Blood pressure trend
        fig_bp = px.line(df, x='timestamp', y='blood_pressure_systolic', color='patient_id',
                        title="Blood Pressure Trends")
        st.plotly_chart(fig_bp, width='stretch')

def render_lab_results_monitoring():
    """Render lab results monitoring"""
    st.subheader(" Lab Results Monitoring")
    
    # Filter lab results data
    lab_data = [d for d in st.session_state.streaming_data if d.get('type') == 'lab_results']
    
    if not lab_data:
        st.info("No lab results data available.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(lab_data)
    
    # Latest lab results
    st.markdown("#### Latest Lab Results")
    latest_labs = df.sort_values('timestamp', ascending=False).head(5)
    st.dataframe(latest_labs, width='stretch')
    
    # Critical lab results
    critical_labs = df[df.get('critical_flag', False) == True]
    if not critical_labs.empty:
        st.markdown("#### Critical Lab Results")
        st.dataframe(critical_labs, width='stretch')
    
    # Lab results distribution
    if 'test_name' in df.columns:
        st.markdown("#### Lab Tests Distribution")
        test_counts = df['test_name'].value_counts()
        fig = px.bar(x=test_counts.index, y=test_counts.values, title="Lab Tests by Type")
        st.plotly_chart(fig, use_container_width=True)

def render_medication_monitoring():
    """Render medication monitoring"""
    st.subheader(" Medication Monitoring")
    
    # Filter medication data
    med_data = [d for d in st.session_state.streaming_data if d.get('type') == 'medications']
    
    if not med_data:
        st.info("No medication data available.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(med_data)
    
    # Latest medications
    st.markdown("#### Latest Medication Records")
    latest_meds = df.sort_values('timestamp', ascending=False).head(5)
    st.dataframe(latest_meds, width='stretch')
    
    # Medication status distribution
    if 'status' in df.columns:
        st.markdown("#### Medication Status Distribution")
        status_counts = df['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index, 
                    title="Medication Status Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    # Missed medications
    missed_meds = df[df.get('status') == 'Missed']
    if not missed_meds.empty:
        st.markdown("#### Missed Medications")
        st.dataframe(missed_meds, width='stretch')

def render_alerts():
    """Render alerts section"""
    st.subheader(" Real-time Alerts")
    
    # Generate simulated alerts
    if st.session_state.streaming_active:
        # Check for critical values in streaming data
        for data in st.session_state.streaming_data[-10:]:  # Check last 10 records
            if data.get('type') == 'vital_signs':
                heart_rate = data.get('heart_rate', 0)
                if heart_rate > 120 or heart_rate < 60:
                    alert = {
                        'patient_id': data['patient_id'],
                        'alert_type': 'Critical Heart Rate',
                        'severity': 'High',
                        'message': f"Heart rate {heart_rate} bpm is outside normal range",
                        'timestamp': datetime.now().isoformat()
                    }
                    if alert not in st.session_state.alerts:
                        st.session_state.alerts.append(alert)
            
            elif data.get('type') == 'lab_results':
                if data.get('critical_flag'):
                    alert = {
                        'patient_id': data['patient_id'],
                        'alert_type': 'Critical Lab Result',
                        'severity': 'Critical',
                        'message': f"Critical {data.get('test_name')}: {data.get('test_value')}",
                        'timestamp': datetime.now().isoformat()
                    }
                    if alert not in st.session_state.alerts:
                        st.session_state.alerts.append(alert)
    
    # Display alerts
    if not st.session_state.alerts:
        st.success("No alerts at this time")
        return
    
    # Keep only last 20 alerts
    if len(st.session_state.alerts) > 20:
        st.session_state.alerts = st.session_state.alerts[-20:]
    
    for alert in reversed(st.session_state.alerts[-10:]):  # Show last 10 alerts
        severity_color = "alert-card" if alert['severity'] in ['High', 'Critical'] else "success-card"
        
        st.markdown(f"""
        <div class="{severity_color}">
            <h4> {alert['alert_type']}</h4>
            <p><strong>Patient:</strong> {alert['patient_id']}</p>
            <p><strong>Severity:</strong> {alert['severity']}</p>
            <p><strong>Message:</strong> {alert['message']}</p>
            <p><strong>Time:</strong> {alert['timestamp']}</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Render header
    render_header()
    
    # Simulate streaming data if active
    if st.session_state.streaming_active:
        simulate_streaming_data()
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Streaming Status", "Live Data", "Vital Signs", "Lab Results", "Alerts"
    ])
    
    with tab1:
        render_streaming_status()
    
    with tab2:
        render_live_data()
    
    with tab3:
        render_vital_signs_monitoring()
    
    with tab4:
        render_lab_results_monitoring()
    
    with tab5:
        render_alerts()
    
    # Auto-refresh if streaming is active
    if st.session_state.streaming_active:
        time.sleep(2)
        st.rerun()

if __name__ == "__main__":
    main()
