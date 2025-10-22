#!/usr/bin/env python3
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
        print("\nCreating healthcare data warehouse...")
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
        print("\nCreating healthcare database...")
        cursor.execute(f"""
            CREATE DATABASE IF NOT EXISTS HEALTHCARE_DB
            COMMENT = 'Healthcare Patient Analytics Database'
        """)
        print(" Healthcare database created!")
        
        # Use healthcare database
        cursor.execute("USE DATABASE HEALTHCARE_DB")
        cursor.execute("USE SCHEMA PUBLIC")
        
        # Create healthcare tables
        print("\nCreating healthcare tables...")
        
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
        print("\nCreating analytics views...")
        
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
        print("\n Snowflake setup completed successfully!")
        print("Your healthcare data warehouse is ready!")
        
    except Exception as e:
        print(f" Error connecting to Snowflake: {e}")
        print("Please check your credentials and try again.")

if __name__ == "__main__":
    connect_to_snowflake()
