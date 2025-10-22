#!/usr/bin/env python3
"""
Healthcare Monitoring Startup Script
===================================
Startup script for the Healthcare System Monitoring Dashboard.
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

def main():
    """Start the Healthcare Monitoring Dashboard"""
    print("🏥 Starting Healthcare System Monitoring Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8506")
    print("🔍 Monitoring system health, performance, and alerts")
    print("🚨 Real-time alerting and notification system")
    print("\n" + "="*60)
    
    # Start the monitoring dashboard
    import subprocess
    subprocess.run([
        "streamlit", "run", 
        "dashboards/healthcare_monitoring_dashboard.py",
        "--server.port", "8506",
        "--server.headless", "true"
    ])

if __name__ == "__main__":
    main()
