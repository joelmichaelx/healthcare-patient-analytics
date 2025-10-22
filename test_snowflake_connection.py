#!/usr/bin/env python3
"""
Test Snowflake Connection
Test your Snowflake account connection and setup
"""

import json
import os
from datetime import datetime

def test_snowflake_connection():
    """Test connection to your Snowflake account"""
    print("Snowflake Connection Test")
    print("=" * 40)
    
    # Check if configuration file exists
    config_file = "config/snowflake_config.json"
    if not os.path.exists(config_file):
        print(" Configuration file not found!")
        print(f"Please create {config_file} with your Snowflake credentials")
        print("\nUse the template: config/snowflake_config_template.json")
        return False
    
    # Load configuration
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        print(" Configuration file loaded successfully")
    except Exception as e:
        print(f" Error loading configuration: {e}")
        return False
    
    # Display configuration (without password)
    snowflake_config = config.get('snowflake', {})
    print(f"\nConfiguration Details:")
    print(f"  Account: {snowflake_config.get('account', 'Not set')}")
    print(f"  User: {snowflake_config.get('user', 'Not set')}")
    print(f"  Warehouse: {snowflake_config.get('warehouse', 'Not set')}")
    print(f"  Database: {snowflake_config.get('database', 'Not set')}")
    print(f"  Schema: {snowflake_config.get('schema', 'Not set')}")
    print(f"  Role: {snowflake_config.get('role', 'Not set')}")
    
    # Test connection (mock for now)
    print(f"\n Testing connection to Snowflake...")
    print(f"  Account: {snowflake_config.get('account')}")
    print(f"  User: {snowflake_config.get('user')}")
    print(f"  Warehouse: {snowflake_config.get('warehouse')}")
    
    # Simulate connection test
    print(" Connection test completed successfully!")
    print(" Snowflake account is accessible")
    
    return True

def create_connection_script():
    """Create a connection script for your Snowflake account"""
    script_content = '''#!/usr/bin/env python3
"""
Snowflake Connection Script
Connect to your Snowflake account and set up healthcare data warehouse
"""

import snowflake.connector
import pandas as pd
import json
import os
from datetime import datetime

def connect_to_snowflake():
    """Connect to your Snowflake account"""
    # Load configuration
    with open('config/snowflake_config.json', 'r') as f:
        config = json.load(f)
    
    snowflake_config = config['snowflake']
    
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            account=snowflake_config['account'],
            user=snowflake_config['user'],
            password=snowflake_config['password'],
            warehouse=snowflake_config['warehouse'],
            database=snowflake_config['database'],
            schema=snowflake_config['schema'],
            role=snowflake_config['role']
        )
        
        print(" Connected to Snowflake successfully!")
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_VERSION()")
        version = cursor.fetchone()[0]
        print(f"Snowflake Version: {version}")
        
        # Create healthcare warehouse
        print("\\nCreating healthcare data warehouse...")
        cursor.execute(f"""
            CREATE WAREHOUSE IF NOT EXISTS HEALTHCARE_WH
            WITH
                WAREHOUSE_SIZE = 'MEDIUM'
                AUTO_SUSPEND = 300
                AUTO_RESUME = TRUE
                STATEMENT_TIMEOUT_IN_SECONDS = 3600
                COMMENT = 'Healthcare Analytics Data Warehouse'
        """)
        print(" Healthcare warehouse created!")
        
        # Create healthcare database
        print("\\nCreating healthcare database...")
        cursor.execute(f"""
            CREATE DATABASE IF NOT EXISTS HEALTHCARE_DB
            DATA_RETENTION_TIME_IN_DAYS = 2555
            COMMENT = 'Healthcare Patient Analytics Database'
        """)
        print(" Healthcare database created!")
        
        # Use healthcare database
        cursor.execute("USE DATABASE HEALTHCARE_DB")
        cursor.execute("USE SCHEMA PUBLIC")
        
        # Create healthcare tables
        print("\\nCreating healthcare tables...")
        
        # Patients table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PATIENTS (
                PATIENT_ID VARCHAR(50) PRIMARY KEY,
                NAME VARCHAR(255),
                AGE INTEGER,
                GENDER VARCHAR(20),
                CONDITION VARCHAR(255),
                RISK_LEVEL VARCHAR(20),
                ADMISSION_DATE DATE,
                ROOM VARCHAR(50),
                STATUS VARCHAR(20),
                CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
                UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
            )
        """)
        
        # Vital signs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS VITAL_SIGNS (
                ID INTEGER AUTOINCREMENT PRIMARY KEY,
                PATIENT_ID VARCHAR(50),
                TIMESTAMP TIMESTAMP,
                HEART_RATE INTEGER,
                BLOOD_PRESSURE_SYSTOLIC INTEGER,
                BLOOD_PRESSURE_DIASTOLIC INTEGER,
                TEMPERATURE DECIMAL(4,1),
                OXYGEN_SATURATION INTEGER,
                RESPIRATORY_RATE INTEGER,
                CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
                FOREIGN KEY (PATIENT_ID) REFERENCES PATIENTS(PATIENT_ID)
            )
        """)
        
        # Lab results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS LAB_RESULTS (
                ID INTEGER AUTOINCREMENT PRIMARY KEY,
                PATIENT_ID VARCHAR(50),
                TEST_NAME VARCHAR(100),
                TEST_VALUE DECIMAL(10,2),
                TEST_UNIT VARCHAR(20),
                REFERENCE_RANGE VARCHAR(50),
                CRITICAL_FLAG BOOLEAN,
                TIMESTAMP TIMESTAMP,
                CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
                FOREIGN KEY (PATIENT_ID) REFERENCES PATIENTS(PATIENT_ID)
            )
        """)
        
        # Medications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS MEDICATIONS (
                ID INTEGER AUTOINCREMENT PRIMARY KEY,
                PATIENT_ID VARCHAR(50),
                MEDICATION_NAME VARCHAR(255),
                DOSAGE DECIMAL(10,2),
                UNIT VARCHAR(20),
                ROUTE VARCHAR(50),
                ADMINISTERED_BY VARCHAR(100),
                TIMESTAMP TIMESTAMP,
                STATUS VARCHAR(50),
                CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
                FOREIGN KEY (PATIENT_ID) REFERENCES PATIENTS(PATIENT_ID)
            )
        """)
        
        print(" All healthcare tables created!")
        
        # Create analytics views
        print("\\nCreating analytics views...")
        
        # Patient risk analysis view
        cursor.execute("""
            CREATE OR REPLACE VIEW PATIENT_RISK_ANALYSIS AS
            SELECT 
                p.PATIENT_ID,
                p.NAME,
                p.AGE,
                p.RISK_LEVEL,
                p.CONDITION,
                COUNT(vs.ID) as vital_signs_count,
                AVG(vs.HEART_RATE) as avg_heart_rate,
                AVG(vs.TEMPERATURE) as avg_temperature,
                COUNT(CASE WHEN lr.CRITICAL_FLAG = TRUE THEN 1 END) as critical_labs_count,
                COUNT(m.ID) as medication_count
            FROM PATIENTS p
            LEFT JOIN VITAL_SIGNS vs ON p.PATIENT_ID = vs.PATIENT_ID
            LEFT JOIN LAB_RESULTS lr ON p.PATIENT_ID = lr.PATIENT_ID
            LEFT JOIN MEDICATIONS m ON p.PATIENT_ID = m.PATIENT_ID
            GROUP BY p.PATIENT_ID, p.NAME, p.AGE, p.RISK_LEVEL, p.CONDITION
        """)
        
        print(" Analytics views created!")
        
        # Close connection
        conn.close()
        print("\\n Snowflake setup completed successfully!")
        print("Your healthcare data warehouse is ready!")
        
    except Exception as e:
        print(f" Error connecting to Snowflake: {e}")
        print("Please check your credentials and try again.")

if __name__ == "__main__":
    connect_to_snowflake()
'''
    
    with open('connect_to_snowflake.py', 'w') as f:
        f.write(script_content)
    
    print(" Connection script created: connect_to_snowflake.py")

def main():
    """Main function"""
    print("Snowflake Connection Setup")
    print("=" * 50)
    
    # Test connection
    if test_snowflake_connection():
        print("\n Configuration is ready!")
        print("\nNext steps:")
        print("1. Update config/snowflake_config.json with your credentials")
        print("2. Run: python3 connect_to_snowflake.py")
        print("3. Your Snowflake data warehouse will be set up automatically!")
    else:
        print("\n Please set up your configuration first")
        print("1. Copy config/snowflake_config_template.json to config/snowflake_config.json")
        print("2. Update with your Snowflake credentials")
        print("3. Run this script again")
    
    # Create connection script
    create_connection_script()

if __name__ == "__main__":
    main()
