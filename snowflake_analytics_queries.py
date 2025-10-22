#!/usr/bin/env python3
"""
Snowflake Healthcare Analytics Queries
=====================================
This script runs comprehensive analytics queries on the healthcare data
stored in Snowflake to generate insights and reports.
"""

import json
import os
import snowflake.connector
from snowflake.connector import DictCursor
import pandas as pd

def load_snowflake_config():
    """Load Snowflake configuration"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'snowflake_config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def connect_to_snowflake(config):
    """Connect to Snowflake"""
    print(" Connecting to Snowflake...")
    conn = snowflake.connector.connect(
        account=config['snowflake']['account'],
        user=config['snowflake']['user'],
        password=config['snowflake']['password'],
        warehouse=config['snowflake']['warehouse'],
        database=config['snowflake']['database'],
        schema=config['snowflake']['schema'],
        role=config['snowflake']['role']
    )
    print(" Connected to Snowflake successfully!")
    return conn

def run_patient_analytics(cursor):
    """Run patient analytics queries"""
    print("\n PATIENT ANALYTICS")
    print("=" * 50)
    
    # Patient demographics
    print("\n1. Patient Demographics:")
    cursor.execute("""
        SELECT 
            GENDER,
            COUNT(*) as patient_count,
            ROUND(AVG(AGE), 1) as avg_age,
            MIN(AGE) as min_age,
            MAX(AGE) as max_age
        FROM PATIENTS 
        GROUP BY GENDER
        ORDER BY patient_count DESC
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  {row[0]}: {row[1]} patients, Avg Age: {row[2]}, Range: {row[3]}-{row[4]}")
    
    # Risk level distribution
    print("\n2. Risk Level Distribution:")
    cursor.execute("""
        SELECT 
            RISK_LEVEL,
            COUNT(*) as patient_count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM PATIENTS), 1) as percentage
        FROM PATIENTS 
        GROUP BY RISK_LEVEL
        ORDER BY patient_count DESC
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  {row[0]}: {row[1]} patients ({row[2]}%)")
    
    # Top conditions
    print("\n3. Top Medical Conditions:")
    cursor.execute("""
        SELECT 
            CONDITION,
            COUNT(*) as patient_count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM PATIENTS), 1) as percentage
        FROM PATIENTS 
        GROUP BY CONDITION
        ORDER BY patient_count DESC
        LIMIT 10
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  {row[0]}: {row[1]} patients ({row[2]}%)")

def run_vital_signs_analytics(cursor):
    """Run vital signs analytics"""
    print("\n VITAL SIGNS ANALYTICS")
    print("=" * 50)
    
    # Vital signs summary
    print("\n1. Vital Signs Summary (Latest Readings):")
    cursor.execute("""
        SELECT 
            ROUND(AVG(HEART_RATE), 1) as avg_heart_rate,
            ROUND(AVG(BLOOD_PRESSURE_SYSTOLIC), 1) as avg_systolic_bp,
            ROUND(AVG(BLOOD_PRESSURE_DIASTOLIC), 1) as avg_diastolic_bp,
            ROUND(AVG(TEMPERATURE), 1) as avg_temperature,
            ROUND(AVG(OXYGEN_SATURATION), 1) as avg_oxygen_sat,
            ROUND(AVG(RESPIRATORY_RATE), 1) as avg_respiratory_rate
        FROM VITAL_SIGNS
    """)
    results = cursor.fetchone()
    print(f"  Heart Rate: {results[0]} bpm")
    print(f"  Blood Pressure: {results[1]}/{results[2]} mmHg")
    print(f"  Temperature: {results[3]}°F")
    print(f"  Oxygen Saturation: {results[4]}%")
    print(f"  Respiratory Rate: {results[5]} breaths/min")
    
    # Critical vital signs alerts
    print("\n2. Critical Vital Signs Alerts:")
    cursor.execute("""
        SELECT 
            COUNT(*) as critical_alerts,
            SUM(CASE WHEN HEART_RATE > 120 THEN 1 ELSE 0 END) as high_heart_rate,
            SUM(CASE WHEN BLOOD_PRESSURE_SYSTOLIC > 180 THEN 1 ELSE 0 END) as high_bp,
            SUM(CASE WHEN TEMPERATURE > 100.4 THEN 1 ELSE 0 END) as high_temp,
            SUM(CASE WHEN OXYGEN_SATURATION < 90 THEN 1 ELSE 0 END) as low_oxygen
        FROM VITAL_SIGNS
        WHERE TIMESTAMP >= DATEADD(day, -1, CURRENT_TIMESTAMP())
    """)
    results = cursor.fetchone()
    print(f"  Total Critical Alerts (24h): {results[0]}")
    print(f"  High Heart Rate: {results[1]}")
    print(f"  High Blood Pressure: {results[2]}")
    print(f"  High Temperature: {results[3]}")
    print(f"  Low Oxygen Saturation: {results[4]}")

def run_lab_results_analytics(cursor):
    """Run lab results analytics"""
    print("\n LAB RESULTS ANALYTICS")
    print("=" * 50)
    
    # Critical lab values
    print("\n1. Critical Lab Values:")
    cursor.execute("""
        SELECT 
            TEST_NAME,
            COUNT(*) as total_tests,
            SUM(CASE WHEN CRITICAL_FLAG = TRUE THEN 1 ELSE 0 END) as critical_count,
            ROUND(SUM(CASE WHEN CRITICAL_FLAG = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as critical_percentage
        FROM LAB_RESULTS
        GROUP BY TEST_NAME
        ORDER BY critical_count DESC
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  {row[0]}: {row[2]}/{row[1]} critical ({row[3]}%)")
    
    # Lab value ranges
    print("\n2. Lab Value Statistics:")
    cursor.execute("""
        SELECT 
            TEST_NAME,
            ROUND(AVG(TEST_VALUE), 2) as avg_value,
            ROUND(MIN(TEST_VALUE), 2) as min_value,
            ROUND(MAX(TEST_VALUE), 2) as max_value,
            TEST_UNIT
        FROM LAB_RESULTS
        GROUP BY TEST_NAME, TEST_UNIT
        ORDER BY TEST_NAME
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  {row[0]}: {row[1]} {row[4]} (Range: {row[2]}-{row[3]})")

def run_medication_analytics(cursor):
    """Run medication analytics"""
    print("\n MEDICATION ANALYTICS")
    print("=" * 50)
    
    # Medication adherence
    print("\n1. Medication Adherence:")
    cursor.execute("""
        SELECT 
            STATUS,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM MEDICATIONS), 1) as percentage
        FROM MEDICATIONS
        GROUP BY STATUS
        ORDER BY count DESC
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  {row[0]}: {row[1]} ({row[2]}%)")
    
    # Top medications
    print("\n2. Most Prescribed Medications:")
    cursor.execute("""
        SELECT 
            MEDICATION_NAME,
            COUNT(*) as prescription_count,
            ROUND(AVG(DOSAGE), 1) as avg_dosage,
            UNIT
        FROM MEDICATIONS
        GROUP BY MEDICATION_NAME, UNIT
        ORDER BY prescription_count DESC
        LIMIT 10
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  {row[0]}: {row[1]} prescriptions, Avg: {row[2]} {row[3]}")

def run_clinical_insights(cursor):
    """Run clinical insights and correlations"""
    print("\n CLINICAL INSIGHTS")
    print("=" * 50)
    
    # High-risk patients with critical vitals
    print("\n1. High-Risk Patients with Critical Vital Signs:")
    cursor.execute("""
        SELECT 
            p.PATIENT_ID,
            p.NAME,
            p.CONDITION,
            p.RISK_LEVEL,
            COUNT(vs.ID) as vital_readings,
            AVG(vs.HEART_RATE) as avg_heart_rate,
            AVG(vs.BLOOD_PRESSURE_SYSTOLIC) as avg_systolic_bp
        FROM PATIENTS p
        JOIN VITAL_SIGNS vs ON p.PATIENT_ID = vs.PATIENT_ID
        WHERE p.RISK_LEVEL IN ('Critical', 'High')
        AND vs.TIMESTAMP >= DATEADD(day, -7, CURRENT_TIMESTAMP())
        GROUP BY p.PATIENT_ID, p.NAME, p.CONDITION, p.RISK_LEVEL
        HAVING AVG(vs.HEART_RATE) > 100 OR AVG(vs.BLOOD_PRESSURE_SYSTOLIC) > 140
        ORDER BY avg_heart_rate DESC
        LIMIT 10
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  {row[1]} ({row[2]}): HR {row[5]:.1f}, BP {row[6]:.1f} ({row[3]} risk)")
    
    # Patients with multiple critical lab values
    print("\n2. Patients with Multiple Critical Lab Values:")
    cursor.execute("""
        SELECT 
            p.PATIENT_ID,
            p.NAME,
            p.CONDITION,
            COUNT(lr.ID) as critical_labs
        FROM PATIENTS p
        JOIN LAB_RESULTS lr ON p.PATIENT_ID = lr.PATIENT_ID
        WHERE lr.CRITICAL_FLAG = TRUE
        AND lr.TIMESTAMP >= DATEADD(day, -30, CURRENT_TIMESTAMP())
        GROUP BY p.PATIENT_ID, p.NAME, p.CONDITION
        HAVING COUNT(lr.ID) >= 2
        ORDER BY critical_labs DESC
        LIMIT 10
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  {row[1]} ({row[2]}): {row[3]} critical lab values")

def run_population_health_analytics(cursor):
    """Run population health analytics"""
    print("\n POPULATION HEALTH ANALYTICS")
    print("=" * 50)
    
    # Age group analysis
    print("\n1. Age Group Distribution:")
    cursor.execute("""
        SELECT 
            CASE 
                WHEN AGE < 18 THEN 'Pediatric (<18)'
                WHEN AGE BETWEEN 18 AND 35 THEN 'Young Adult (18-35)'
                WHEN AGE BETWEEN 36 AND 55 THEN 'Middle Age (36-55)'
                WHEN AGE BETWEEN 56 AND 75 THEN 'Senior (56-75)'
                ELSE 'Elderly (75+)'
            END as age_group,
            COUNT(*) as patient_count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM PATIENTS), 1) as percentage
        FROM PATIENTS
        GROUP BY age_group
        ORDER BY patient_count DESC
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  {row[0]}: {row[1]} patients ({row[2]}%)")
    
    # Condition prevalence by age
    print("\n2. Top Conditions by Age Group:")
    cursor.execute("""
        SELECT 
            CASE 
                WHEN AGE < 18 THEN 'Pediatric'
                WHEN AGE BETWEEN 18 AND 35 THEN 'Young Adult'
                WHEN AGE BETWEEN 36 AND 55 THEN 'Middle Age'
                WHEN AGE BETWEEN 56 AND 75 THEN 'Senior'
                ELSE 'Elderly'
            END as age_group,
            CONDITION,
            COUNT(*) as patient_count
        FROM PATIENTS
        GROUP BY age_group, CONDITION
        QUALIFY ROW_NUMBER() OVER (PARTITION BY age_group ORDER BY COUNT(*) DESC) <= 3
        ORDER BY age_group, patient_count DESC
    """)
    results = cursor.fetchall()
    current_group = None
    for row in results:
        if current_group != row[0]:
            print(f"\n  {row[0]}:")
            current_group = row[0]
        print(f"    {row[1]}: {row[2]} patients")

def main():
    """Main function to run all analytics queries"""
    print("Healthcare Analytics Dashboard - Snowflake")
    print("=" * 60)
    
    try:
        # Load configuration and connect
        config = load_snowflake_config()
        conn = connect_to_snowflake(config)
        cursor = conn.cursor(DictCursor)
        
        # Run all analytics
        run_patient_analytics(cursor)
        run_vital_signs_analytics(cursor)
        run_lab_results_analytics(cursor)
        run_medication_analytics(cursor)
        run_clinical_insights(cursor)
        run_population_health_analytics(cursor)
        
        print("\n Analytics completed successfully!")
        print("All healthcare insights have been generated from your Snowflake data warehouse!")
        
    except Exception as e:
        print(f" Error running analytics: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print(" Snowflake connection closed.")

if __name__ == "__main__":
    main()
