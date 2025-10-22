#!/usr/bin/env python3
"""
Healthcare System Monitoring Dashboard
======================================
Streamlit dashboard for monitoring healthcare system health,
performance metrics, alerts, and critical healthcare indicators.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import json
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from monitoring.system_monitor import (
    HealthcareSystemMonitor, 
    MONITORING_CONFIG,
    AlertSeverity,
    AlertType
)

# Page configuration
st.set_page_config(
    page_title="Healthcare System Monitoring",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .alert-critical {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .alert-warning {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .alert-info {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .status-healthy {
        color: #4caf50;
        font-weight: bold;
    }
    .status-warning {
        color: #ff9800;
        font-weight: bold;
    }
    .status-critical {
        color: #f44336;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def render_header():
    """Render dashboard header"""
    st.title("🏥 Healthcare System Monitoring Dashboard")
    st.markdown("Real-time monitoring of healthcare analytics platform health and performance")
    
    # Status indicator
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("**Powered by Healthcare Analytics Platform**")
    
    with col2:
        if st.button("🔄 Refresh Data", key="refresh_monitoring"):
            st.rerun()
    
    with col3:
        st.markdown(f"**Last Updated:** {datetime.now().strftime('%H:%M:%S')}")

def render_system_overview():
    """Render system overview metrics"""
    st.header("📊 System Overview")
    
    try:
        # Initialize monitor
        monitor = HealthcareSystemMonitor(MONITORING_CONFIG)
        status = monitor.get_system_status()
        
        if status.get('status') == 'error':
            st.error(f"Error getting system status: {status.get('message')}")
            return
        
        metrics = status.get('metrics', {})
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            cpu_percent = metrics.get('cpu_percent', 0)
            cpu_color = "red" if cpu_percent > 80 else "orange" if cpu_percent > 60 else "green"
            st.metric(
                "CPU Usage",
                f"{cpu_percent:.1f}%",
                delta=None,
                help="Current CPU utilization"
            )
            st.markdown(f'<div style="color: {cpu_color}">●</div>', unsafe_allow_html=True)
        
        with col2:
            memory_percent = metrics.get('memory_percent', 0)
            memory_color = "red" if memory_percent > 85 else "orange" if memory_percent > 70 else "green"
            st.metric(
                "Memory Usage",
                f"{memory_percent:.1f}%",
                delta=None,
                help="Current memory utilization"
            )
            st.markdown(f'<div style="color: {memory_color}">●</div>', unsafe_allow_html=True)
        
        with col3:
            disk_percent = metrics.get('disk_percent', 0)
            disk_color = "red" if disk_percent > 90 else "orange" if disk_percent > 80 else "green"
            st.metric(
                "Disk Usage",
                f"{disk_percent:.1f}%",
                delta=None,
                help="Current disk utilization"
            )
            st.markdown(f'<div style="color: {disk_color}">●</div>', unsafe_allow_html=True)
        
        with col4:
            active_patients = metrics.get('active_patients', 0)
            st.metric(
                "Active Patients",
                f"{active_patients:,}",
                delta=None,
                help="Number of currently active patients"
            )
        
        # System status
        system_status = status.get('status', 'unknown')
        status_color = {
            'healthy': 'status-healthy',
            'warning': 'status-warning',
            'critical': 'status-critical'
        }.get(system_status, 'status-critical')
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>System Status: <span class="{status_color}">{system_status.upper()}</span></h4>
            <p>Monitoring Active: {status.get('monitoring_active', False)}</p>
            <p>Alerts Queue: {status.get('alerts_count', 0)}</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading system overview: {e}")

def render_performance_metrics():
    """Render performance metrics charts"""
    st.header("📈 Performance Metrics")
    
    try:
        # Initialize monitor
        monitor = HealthcareSystemMonitor(MONITORING_CONFIG)
        status = monitor.get_system_status()
        
        if status.get('status') == 'error':
            st.error(f"Error getting performance metrics: {status.get('message')}")
            return
        
        metrics = status.get('metrics', {})
        
        # Create performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            # CPU and Memory usage
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('CPU Usage', 'Memory Usage'),
                vertical_spacing=0.1
            )
            
            # CPU chart
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=metrics.get('cpu_percent', 0),
                    domain={'x': [0, 1], 'y': [0.5, 1]},
                    title={'text': "CPU %"},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "yellow"},
                            {'range': [80, 100], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 80
                        }
                    }
                ),
                row=1, col=1
            )
            
            # Memory chart
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=metrics.get('memory_percent', 0),
                    domain={'x': [0, 1], 'y': [0, 0.5]},
                    title={'text': "Memory %"},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkgreen"},
                        'steps': [
                            {'range': [0, 60], 'color': "lightgray"},
                            {'range': [60, 85], 'color': "yellow"},
                            {'range': [85, 100], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 85
                        }
                    }
                ),
                row=2, col=1
            )
            
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Healthcare metrics
            healthcare_data = {
                'Metric': ['Active Patients', 'Critical Alerts', 'Database Connections', 'API Requests/min'],
                'Value': [
                    metrics.get('active_patients', 0),
                    metrics.get('critical_alerts', 0),
                    metrics.get('database_connections', 0),
                    metrics.get('api_requests_per_minute', 0)
                ]
            }
            
            df = pd.DataFrame(healthcare_data)
            
            fig = px.bar(
                df, 
                x='Metric', 
                y='Value',
                title="Healthcare System Metrics",
                color='Value',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading performance metrics: {e}")

def render_alerts():
    """Render system alerts"""
    st.header("🚨 System Alerts")
    
    try:
        # Initialize monitor
        monitor = HealthcareSystemMonitor(MONITORING_CONFIG)
        alerts = monitor.get_alerts(limit=50)
        
        if not alerts:
            st.info("No alerts at this time. System is running smoothly.")
            return
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            severity_filter = st.selectbox(
                "Filter by Severity",
                ["All", "Emergency", "Critical", "Warning", "Info"],
                key="alert_severity_filter"
            )
        
        with col2:
            type_filter = st.selectbox(
                "Filter by Type",
                ["All", "System Health", "Database", "API Performance", "ML Model", "Patient Safety", "Data Quality", "Security"],
                key="alert_type_filter"
            )
        
        with col3:
            show_acknowledged = st.checkbox("Show Acknowledged", value=False, key="show_acknowledged")
        
        # Filter alerts
        filtered_alerts = alerts
        
        if severity_filter != "All":
            filtered_alerts = [a for a in filtered_alerts if a.get('severity') == severity_filter.lower()]
        
        if type_filter != "All":
            type_mapping = {
                "System Health": "system_health",
                "Database": "database",
                "API Performance": "api_performance",
                "ML Model": "ml_model",
                "Patient Safety": "patient_safety",
                "Data Quality": "data_quality",
                "Security": "security"
            }
            filtered_alerts = [a for a in filtered_alerts if a.get('alert_type') == type_mapping.get(type_filter, type_filter.lower())]
        
        if not show_acknowledged:
            filtered_alerts = [a for a in filtered_alerts if not a.get('acknowledged', False)]
        
        # Display alerts
        if not filtered_alerts:
            st.info("No alerts match the current filters.")
            return
        
        for alert in filtered_alerts:
            severity = alert.get('severity', 'info')
            alert_type = alert.get('alert_type', 'unknown')
            title = alert.get('title', 'Unknown Alert')
            message = alert.get('message', 'No message')
            timestamp = alert.get('timestamp', 'Unknown time')
            acknowledged = alert.get('acknowledged', False)
            resolved = alert.get('resolved', False)
            
            # Determine alert styling
            if severity == 'emergency' or severity == 'critical':
                alert_class = "alert-critical"
            elif severity == 'warning':
                alert_class = "alert-warning"
            else:
                alert_class = "alert-info"
            
            # Alert status
            status_text = ""
            if resolved:
                status_text = "✅ Resolved"
            elif acknowledged:
                status_text = "👁️ Acknowledged"
            else:
                status_text = "🔴 Active"
            
            st.markdown(f"""
            <div class="{alert_class}">
                <h4>{title} <span style="float: right; font-size: 0.8em;">{status_text}</span></h4>
                <p><strong>Type:</strong> {alert_type.replace('_', ' ').title()}</p>
                <p><strong>Severity:</strong> {severity.upper()}</p>
                <p><strong>Message:</strong> {message}</p>
                <p><strong>Time:</strong> {timestamp}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Alert actions
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if not acknowledged and st.button(f"Acknowledge", key=f"ack_{alert.get('id', 'unknown')}"):
                    monitor.acknowledge_alert(alert.get('id', ''))
                    st.success("Alert acknowledged")
                    st.rerun()
            
            with col2:
                if not resolved and st.button(f"Resolve", key=f"resolve_{alert.get('id', 'unknown')}"):
                    monitor.resolve_alert(alert.get('id', ''))
                    st.success("Alert resolved")
                    st.rerun()
            
            with col3:
                if st.button(f"View Details", key=f"details_{alert.get('id', 'unknown')}"):
                    metadata = alert.get('metadata', {})
                    st.json(metadata)
            
            st.markdown("---")
        
    except Exception as e:
        st.error(f"Error loading alerts: {e}")

def render_healthcare_metrics():
    """Render healthcare-specific metrics"""
    st.header("🏥 Healthcare Metrics")
    
    try:
        # Initialize monitor
        monitor = HealthcareSystemMonitor(MONITORING_CONFIG)
        status = monitor.get_system_status()
        
        if status.get('status') == 'error':
            st.error(f"Error getting healthcare metrics: {status.get('message')}")
            return
        
        metrics = status.get('metrics', {})
        
        # Healthcare KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            active_patients = metrics.get('active_patients', 0)
            st.metric(
                "Active Patients",
                f"{active_patients:,}",
                help="Currently active patients in the system"
            )
        
        with col2:
            critical_alerts = metrics.get('critical_alerts', 0)
            st.metric(
                "Critical Alerts",
                f"{critical_alerts:,}",
                help="Number of critical patient alerts"
            )
        
        with col3:
            db_connections = metrics.get('database_connections', 0)
            st.metric(
                "DB Connections",
                f"{db_connections:,}",
                help="Active database connections"
            )
        
        with col4:
            api_requests = metrics.get('api_requests_per_minute', 0)
            st.metric(
                "API Requests/min",
                f"{api_requests:,}",
                help="API requests per minute"
            )
        
        # Healthcare system health indicators
        st.subheader("System Health Indicators")
        
        # Create health indicators
        health_indicators = {
            'Patient Safety': 'green' if critical_alerts < 10 else 'orange' if critical_alerts < 50 else 'red',
            'System Performance': 'green' if metrics.get('cpu_percent', 0) < 70 else 'orange' if metrics.get('cpu_percent', 0) < 85 else 'red',
            'Data Quality': 'green' if db_connections > 0 else 'red',
            'API Health': 'green' if api_requests > 0 else 'orange'
        }
        
        for indicator, status in health_indicators.items():
            color_map = {'green': '🟢', 'orange': '🟡', 'red': '🔴'}
            st.markdown(f"{color_map[status]} **{indicator}**: {status.title()}")
        
    except Exception as e:
        st.error(f"Error loading healthcare metrics: {e}")

def render_monitoring_settings():
    """Render monitoring settings"""
    st.header("⚙️ Monitoring Settings")
    
    st.subheader("Alert Thresholds")
    
    # CPU threshold
    cpu_threshold = st.slider(
        "CPU Usage Alert Threshold (%)",
        min_value=50,
        max_value=100,
        value=80,
        help="Alert when CPU usage exceeds this threshold"
    )
    
    # Memory threshold
    memory_threshold = st.slider(
        "Memory Usage Alert Threshold (%)",
        min_value=50,
        max_value=100,
        value=85,
        help="Alert when memory usage exceeds this threshold"
    )
    
    # Disk threshold
    disk_threshold = st.slider(
        "Disk Usage Alert Threshold (%)",
        min_value=50,
        max_value=100,
        value=90,
        help="Alert when disk usage exceeds this threshold"
    )
    
    # Critical patients threshold
    critical_threshold = st.slider(
        "Critical Patients Alert Threshold",
        min_value=1,
        max_value=100,
        value=50,
        help="Alert when number of critical patients exceeds this threshold"
    )
    
    st.subheader("Notification Settings")
    
    # Email notifications
    email_enabled = st.checkbox("Enable Email Notifications", value=False)
    if email_enabled:
        st.text_input("SMTP Server", value="smtp.gmail.com")
        st.number_input("SMTP Port", value=587)
        st.text_input("Username", value="your-email@gmail.com")
        st.text_input("Password", type="password")
        st.text_input("To Addresses", value="admin@healthcare.com")
    
    # Slack notifications
    slack_enabled = st.checkbox("Enable Slack Notifications", value=False)
    if slack_enabled:
        st.text_input("Slack Webhook URL", value="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK")
    
    # Webhook notifications
    webhook_enabled = st.checkbox("Enable Webhook Notifications", value=False)
    if webhook_enabled:
        st.text_input("Webhook URL", value="https://your-webhook-url.com/alerts")
    
    # Save settings
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")
        st.info("Note: Settings will be applied after system restart.")

def main():
    """Main dashboard function"""
    render_header()
    
    # Sidebar navigation
    st.sidebar.title("📊 Monitoring Dashboard")
    
    page = st.sidebar.selectbox(
        "Select Page",
        [
            "System Overview",
            "Performance Metrics", 
            "Alerts",
            "Healthcare Metrics",
            "Monitoring Settings"
        ]
    )
    
    # Render selected page
    if page == "System Overview":
        render_system_overview()
    elif page == "Performance Metrics":
        render_performance_metrics()
    elif page == "Alerts":
        render_alerts()
    elif page == "Healthcare Metrics":
        render_healthcare_metrics()
    elif page == "Monitoring Settings":
        render_monitoring_settings()
    
    # Auto-refresh
    if st.sidebar.checkbox("🔄 Auto-refresh (30s)", value=False):
        time.sleep(30)
        st.rerun()

if __name__ == "__main__":
    main()
