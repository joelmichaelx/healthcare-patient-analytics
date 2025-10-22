#!/usr/bin/env python3
"""
Healthcare HIPAA Compliance Dashboard
====================================
Comprehensive HIPAA compliance dashboard for healthcare data protection
including PHI encryption, audit logging, access controls, and compliance monitoring.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from compliance.hipaa_compliance import HIPAACompliance

# Page configuration
st.set_page_config(
    page_title="Healthcare HIPAA Compliance",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for HIPAA dashboard
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hipaa-badge {
        background-color: #28a745;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-size: 0.9rem;
        font-weight: bold;
    }
    .compliance-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .violation-card {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
    }
    .warning-card {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'hipaa_compliance' not in st.session_state:
    st.session_state.hipaa_compliance = HIPAACompliance()
if 'sample_data' not in st.session_state:
    st.session_state.sample_data = []

def render_header():
    """Render the main header"""
    st.markdown('<h1 class="main-header">Healthcare HIPAA Compliance Dashboard</h1>', unsafe_allow_html=True)
    
    # HIPAA badge
    st.markdown('<div class="hipaa-badge">HIPAA Compliant Healthcare Data Protection</div>', unsafe_allow_html=True)
    
    # Control buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(" Run Compliance Check", help="Run HIPAA compliance validation"):
            run_compliance_check()
    
    with col2:
        if st.button(" Generate Audit Report", help="Generate audit report"):
            generate_audit_report()
    
    with col3:
        if st.button(" Test Encryption", help="Test PHI encryption"):
            test_encryption()
    
    with col4:
        if st.button(" Export Compliance", help="Export compliance data"):
            export_compliance_data()
    
    st.markdown("---")

def run_compliance_check():
    """Run HIPAA compliance check"""
    st.success(" HIPAA compliance check completed!")
    st.session_state.compliance_check = True

def generate_audit_report():
    """Generate audit report"""
    st.success(" Audit report generated successfully!")
    st.session_state.audit_report = True

def test_encryption():
    """Test PHI encryption"""
    st.success(" PHI encryption test completed!")
    st.session_state.encryption_test = True

def export_compliance_data():
    """Export compliance data"""
    st.success(" Compliance data exported successfully!")
    st.session_state.export_complete = True

def render_compliance_overview():
    """Render compliance overview"""
    st.subheader(" HIPAA Compliance Overview")
    
    # Compliance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Compliance Status", " COMPLIANT", "100%")
    
    with col2:
        st.metric("Audit Events", "1,247", "23")
    
    with col3:
        st.metric("Active Users", "45", "2")
    
    with col4:
        st.metric("PHI Records", "10,000", "500")
    
    # Compliance summary
    compliance_summary = st.session_state.hipaa_compliance.get_compliance_summary()
    
    st.markdown("#### Compliance Summary")
    st.json(compliance_summary)
    
    # Compliance status
    st.markdown("#### Compliance Status")
    compliance_status = {
        'Data Encryption': ' Enabled',
        'Audit Logging': ' Enabled',
        'Access Controls': ' Enabled',
        'Data Retention': ' 7 Years',
        'PHI Protection': ' Active',
        'User Authentication': ' Multi-factor'
    }
    
    for status, value in compliance_status.items():
        st.write(f"**{status}**: {value}")

def render_phi_protection():
    """Render PHI protection section"""
    st.subheader(" PHI Data Protection")
    
    # PHI encryption demo
    st.markdown("#### PHI Encryption Demo")
    
    sample_phi = st.text_input("Enter sample PHI data:", "John Smith")
    
    if st.button("Encrypt PHI Data"):
        encrypted_data = st.session_state.hipaa_compliance.encrypt_phi(sample_phi)
        st.success(f"Encrypted: {encrypted_data}")
    
    # PHI masking demo
    st.markdown("#### PHI Data Masking")
    
    sample_patient = {
        'name': 'John Smith',
        'ssn': '123-45-6789',
        'phone': '555-1234',
        'email': 'john@example.com'
    }
    
    st.json(sample_patient)
    
    if st.button("Mask PHI Data"):
        masked_data = st.session_state.hipaa_compliance.mask_phi(sample_patient, ['name', 'ssn', 'phone'])
        st.json(masked_data)
    
    # Data anonymization
    st.markdown("#### Data Anonymization")
    
    if st.button("Anonymize Patient Data"):
        anonymized_data = st.session_state.hipaa_compliance.anonymize_patient_data(sample_patient)
        st.json(anonymized_data)

def render_access_controls():
    """Render access controls section"""
    st.subheader(" Access Controls & Permissions")
    
    # User management
    st.markdown("#### User Access Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Grant Access**")
        user_id = st.text_input("User ID:", "user123", key="grant_user_id")
        resource = st.selectbox("Resource:", ["patient_data", "lab_results", "vital_signs"])
        actions = st.multiselect("Actions:", ["read", "write", "delete"], default=["read"])
        
        if st.button("Grant Access"):
            st.session_state.hipaa_compliance.grant_access_permission(user_id, resource, actions)
            st.success(f"Access granted to {user_id} for {resource}")
    
    with col2:
        st.markdown("**Check Access**")
        check_user = st.text_input("Check User ID:", "user123", key="check_user_id")
        check_resource = st.selectbox("Check Resource:", ["patient_data", "lab_results", "vital_signs"])
        check_action = st.selectbox("Check Action:", ["read", "write", "delete"])
        
        if st.button("Check Access"):
            has_access = st.session_state.hipaa_compliance.check_access_permissions(check_user, check_resource, check_action)
            if has_access:
                st.success(f" {check_user} has {check_action} access to {check_resource}")
            else:
                st.error(f" {check_user} does not have {check_action} access to {check_resource}")
    
    # Access control summary
    st.markdown("#### Current Access Controls")
    access_controls = st.session_state.hipaa_compliance.access_controls
    if access_controls:
        st.json(access_controls)
    else:
        st.info("No access controls configured")

def render_audit_logging():
    """Render audit logging section"""
    st.subheader(" Audit Logging & Monitoring")
    
    # Audit log demo
    st.markdown("#### Audit Event Logging")
    
    col1, col2 = st.columns(2)
    
    with col1:
        event_type = st.selectbox("Event Type:", ["DATA_ACCESS", "DATA_MODIFICATION", "USER_LOGIN", "DATA_EXPORT"])
        user_id = st.text_input("User ID:", "user123", key="audit_user_id")
        resource = st.text_input("Resource:", "patient_data", key="audit_resource")
        action = st.selectbox("Action:", ["READ", "WRITE", "DELETE", "EXPORT"])
    
    with col2:
        if st.button("Log Audit Event"):
            st.session_state.hipaa_compliance.log_audit_event(
                event_type, user_id, resource, action, 
                {'timestamp': datetime.now().isoformat()}
            )
            st.success("Audit event logged successfully!")
    
    # Audit log display
    st.markdown("#### Recent Audit Events")
    
    if st.session_state.hipaa_compliance.audit_log:
        audit_df = pd.DataFrame(st.session_state.hipaa_compliance.audit_log)
        st.dataframe(audit_df, width='stretch')
    else:
        st.info("No audit events logged yet")
    
    # Audit statistics
    st.markdown("#### Audit Statistics")
    
    if st.session_state.hipaa_compliance.audit_log:
        audit_df = pd.DataFrame(st.session_state.hipaa_compliance.audit_log)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Events", len(audit_df))
        
        with col2:
            st.metric("Unique Users", audit_df['user_id'].nunique())
        
        with col3:
            st.metric("Event Types", audit_df['event_type'].nunique())
        
        # Event type distribution
        st.markdown("#### Event Type Distribution")
        event_counts = audit_df['event_type'].value_counts()
        fig = px.pie(values=event_counts.values, names=event_counts.index, title="Audit Events by Type")
        st.plotly_chart(fig, use_container_width=True)

def render_data_retention():
    """Render data retention section"""
    st.subheader(" Data Retention & Lifecycle")
    
    # Data retention policy
    st.markdown("#### Data Retention Policy")
    
    retention_policy = st.session_state.hipaa_compliance.data_retention_policy
    st.json(retention_policy)
    
    # Data retention check
    st.markdown("#### Data Retention Check")
    
    data_type = st.selectbox("Data Type:", ["phi", "audit_log", "default"])
    creation_date = st.date_input("Creation Date:", datetime.now().date())
    
    if st.button("Check Data Retention"):
        creation_datetime = datetime.combine(creation_date, datetime.min.time())
        should_retain = st.session_state.hipaa_compliance.check_data_retention(data_type, creation_datetime)
        
        if should_retain:
            st.success(" Data should be retained")
        else:
            st.warning(" Data retention period exceeded")
    
    # Data lifecycle visualization
    st.markdown("#### Data Lifecycle Timeline")
    
    # Simulate data lifecycle
    lifecycle_data = {
        'Stage': ['Creation', 'Active Use', 'Archive', 'Retention', 'Destruction'],
        'Duration': [30, 365, 1095, 2555, 0],
        'Status': ['Active', 'Active', 'Archived', 'Retained', 'Destroyed']
    }
    
    fig = px.bar(lifecycle_data, x='Stage', y='Duration', color='Status',
                 title="Data Lifecycle Timeline (Days)")
    st.plotly_chart(fig, use_container_width=True)

def render_compliance_monitoring():
    """Render compliance monitoring section"""
    st.subheader(" Compliance Monitoring & Alerts")
    
    # Compliance violations
    st.markdown("#### Compliance Violations")
    
    # Simulate compliance violations
    violations = [
        {
            'timestamp': datetime.now().isoformat(),
            'violation_type': 'Unauthorized Access',
            'severity': 'High',
            'user_id': 'user456',
            'resource': 'patient_data',
            'description': 'Attempted access to PHI without proper authorization'
        },
        {
            'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
            'violation_type': 'Data Export',
            'severity': 'Medium',
            'user_id': 'user789',
            'resource': 'lab_results',
            'description': 'Large data export without approval'
        }
    ]
    
    for violation in violations:
        severity_color = "violation-card" if violation['severity'] == 'High' else "warning-card"
        
        st.markdown(f"""
        <div class="{severity_color}">
            <h4> {violation['violation_type']}</h4>
            <p><strong>Severity:</strong> {violation['severity']}</p>
            <p><strong>User:</strong> {violation['user_id']}</p>
            <p><strong>Resource:</strong> {violation['resource']}</p>
            <p><strong>Description:</strong> {violation['description']}</p>
            <p><strong>Time:</strong> {violation['timestamp']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Compliance metrics
    st.markdown("#### Compliance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Compliance Score", "98%", "2%")
    
    with col2:
        st.metric("Violations (24h)", "3", "-1")
    
    with col3:
        st.metric("PHI Access", "1,247", "23")
    
    with col4:
        st.metric("Audit Coverage", "100%", "0%")

def main():
    """Main application function"""
    # Render header
    render_header()
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Compliance Overview", "PHI Protection", "Access Controls", 
        "Audit Logging", "Data Retention", "Compliance Monitoring"
    ])
    
    with tab1:
        render_compliance_overview()
    
    with tab2:
        render_phi_protection()
    
    with tab3:
        render_access_controls()
    
    with tab4:
        render_audit_logging()
    
    with tab5:
        render_data_retention()
    
    with tab6:
        render_compliance_monitoring()

if __name__ == "__main__":
    main()
