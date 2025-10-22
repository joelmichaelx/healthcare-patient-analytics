#!/bin/bash
# Healthcare Patient Analytics Platform - Startup Script

echo "Starting Healthcare Patient Analytics Dashboard..."
echo "================================================"

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Start Streamlit dashboard
echo "Starting Streamlit dashboard..."
echo "Dashboard will be available at: http://localhost:8501"
echo "Press Ctrl+C to stop the dashboard"
echo ""

streamlit run dashboards/healthcare_streamlit_app.py
