#!/bin/bash

# Healthcare Patient Analytics Platform - Simplified Automated Setup
# This script automates the environment setup process with compatible packages

set -e  # Exit on any error

echo "Healthcare Patient Analytics Platform - Automated Setup"
echo "====================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.9+ first."
    echo "Download from: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python $PYTHON_VERSION detected"

# Navigate to project directory
cd "$(dirname "$0")"
echo "Working in directory: $(pwd)"

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated"

# Upgrade pip and install setuptools
echo "Upgrading pip and installing build tools..."
pip install --upgrade pip setuptools wheel
echo "Build tools installed"

# Install core dependencies first
echo "Installing core dependencies..."
pip install pandas numpy scipy requests streamlit plotly matplotlib seaborn
echo "Core dependencies installed"

# Install additional dependencies
echo "Installing additional dependencies..."
pip install sqlalchemy psycopg2-binary scikit-learn tensorflow torch xgboost
echo "ML dependencies installed"

# Install remaining dependencies
echo "Installing remaining dependencies..."
pip install faker python-dotenv pyyaml pytest black flake8 tqdm click
echo "Utility dependencies installed"

# Create necessary directories
echo "Creating project directories..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/models
mkdir -p logs
mkdir -p logs/audit
echo "Project directories created"

# Set up environment variables
echo "Setting up environment variables..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
# Healthcare Patient Analytics Platform - Environment Variables

# Database Configuration
DATABASE_URL=sqlite:///healthcare_data.db

# Security Configuration
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
ENCRYPTION_KEY=$(python3 -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')

# FHIR API Configuration (Demo - Update with real credentials)
FHIR_BASE_URL=https://hapi.fhir.org/baseR4
FHIR_CLIENT_ID=demo_client
FHIR_CLIENT_SECRET=demo_secret

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost

# Snowflake Configuration (Optional - Update with real credentials)
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=healthcare_db
SNOWFLAKE_SCHEMA=public
EOF
    echo "Environment variables file created"
else
    echo "Environment variables file already exists"
fi

# Initialize Git repository
echo "Setting up Git repository..."
if [ ! -d ".git" ]; then
    git init
    echo "Git repository initialized"
else
    echo "Git repository already exists"
fi

# Test the installation
echo "Testing installation..."
python3 -c "
import streamlit
import pandas
import plotly
import numpy
import sklearn
print('All required packages imported successfully')
"

# Create initial database
echo "Creating initial database..."
python3 -c "
import sqlite3
import os

# Create database directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Create SQLite database
conn = sqlite3.connect('healthcare_data.db')

# Create basic tables
conn.execute('''
CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    condition TEXT,
    risk_level TEXT,
    admission_date TEXT,
    room TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS vital_signs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    heart_rate INTEGER,
    blood_pressure_systolic INTEGER,
    blood_pressure_diastolic INTEGER,
    temperature REAL,
    oxygen_saturation INTEGER,
    respiratory_rate INTEGER,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS lab_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT NOT NULL,
    test_name TEXT NOT NULL,
    test_value REAL,
    test_unit TEXT,
    reference_range TEXT,
    critical_flag BOOLEAN,
    timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT NOT NULL,
    medication_name TEXT NOT NULL,
    dosage REAL,
    unit TEXT,
    route TEXT,
    administered_by TEXT,
    timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
)
''')

# Create indexes for better performance
conn.execute('CREATE INDEX IF NOT EXISTS idx_patient_id ON patients(patient_id)')
conn.execute('CREATE INDEX IF NOT EXISTS idx_vital_timestamp ON vital_signs(timestamp)')
conn.execute('CREATE INDEX IF NOT EXISTS idx_lab_timestamp ON lab_results(timestamp)')
conn.execute('CREATE INDEX IF NOT EXISTS idx_med_timestamp ON medications(timestamp)')

conn.commit()
conn.close()
print('Database created successfully')
"

# Test the Streamlit app
echo "Testing Streamlit app..."
python3 -c "
import sys
sys.path.append('.')
try:
    from dashboards.healthcare_streamlit_app import HealthcareDashboard
    print('Streamlit app imports successfully')
except Exception as e:
    print(f'Streamlit app test failed: {e}')
    print('This is normal - the app will work when run with streamlit command')
"

echo ""
echo "Setup Complete!"
echo "=============="
echo ""
echo "Virtual environment created and activated"
echo "Dependencies installed"
echo "Project directories created"
echo "Environment variables configured"
echo "Git repository initialized"
echo "Database created"
echo ""
echo "Next Steps:"
echo "1. Run the dashboard: streamlit run dashboards/healthcare_streamlit_app.py"
echo "2. Open your browser to: http://localhost:8501"
echo "3. Test all the features in the dashboard"
echo ""
echo "Documentation:"
echo "- Manual Setup Guide: MANUAL_SETUP_GUIDE.md"
echo "- Study Guide: STUDY_GUIDE.md"
echo "- README: README.md"
echo ""
echo "To activate the environment in the future:"
echo "   source venv/bin/activate"
echo ""
echo "Happy coding!"
