#!/usr/bin/env python3
"""
Test Snowflake Queries
======================
Simple test to verify Snowflake data and queries work correctly.
"""

import json
import os
import snowflake.connector
from snowflake.connector import DictCursor

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

def test_basic_queries(cursor):
    """Test basic queries"""
    print("\n Testing Basic Queries")
    print("=" * 40)
    
    # Test 1: Count patients
    print("\n1. Patient Count:")
    try:
        cursor.execute("SELECT COUNT(*) as patient_count FROM PATIENTS")
        result = cursor.fetchone()
        print(f"  Total Patients: {result[0]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Sample patients
    print("\n2. Sample Patients:")
    try:
        cursor.execute("SELECT PATIENT_ID, NAME, AGE, GENDER, CONDITION FROM PATIENTS LIMIT 5")
        results = cursor.fetchall()
        for row in results:
            print(f"  {row[0]}: {row[1]} ({row[2]} years, {row[3]}) - {row[4]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Vital signs count
    print("\n3. Vital Signs Count:")
    try:
        cursor.execute("SELECT COUNT(*) as vital_count FROM VITAL_SIGNS")
        result = cursor.fetchone()
        print(f"  Total Vital Signs: {result[0]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Lab results count
    print("\n4. Lab Results Count:")
    try:
        cursor.execute("SELECT COUNT(*) as lab_count FROM LAB_RESULTS")
        result = cursor.fetchone()
        print(f"  Total Lab Results: {result[0]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Medications count
    print("\n5. Medications Count:")
    try:
        cursor.execute("SELECT COUNT(*) as med_count FROM MEDICATIONS")
        result = cursor.fetchone()
        print(f"  Total Medications: {result[0]}")
    except Exception as e:
        print(f"   Error: {e}")

def test_analytics_queries(cursor):
    """Test analytics queries"""
    print("\n Testing Analytics Queries")
    print("=" * 40)
    
    # Test 1: Gender distribution
    print("\n1. Gender Distribution:")
    try:
        cursor.execute("""
            SELECT GENDER, COUNT(*) as count 
            FROM PATIENTS 
            GROUP BY GENDER
        """)
        results = cursor.fetchall()
        for row in results:
            print(f"  {row[0]}: {row[1]} patients")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Risk level distribution
    print("\n2. Risk Level Distribution:")
    try:
        cursor.execute("""
            SELECT RISK_LEVEL, COUNT(*) as count 
            FROM PATIENTS 
            GROUP BY RISK_LEVEL
        """)
        results = cursor.fetchall()
        for row in results:
            print(f"  {row[0]}: {row[1]} patients")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Top conditions
    print("\n3. Top Conditions:")
    try:
        cursor.execute("""
            SELECT CONDITION, COUNT(*) as count 
            FROM PATIENTS 
            GROUP BY CONDITION 
            ORDER BY count DESC 
            LIMIT 5
        """)
        results = cursor.fetchall()
        for row in results:
            print(f"  {row[0]}: {row[1]} patients")
    except Exception as e:
        print(f"   Error: {e}")

def main():
    """Main function"""
    print("Snowflake Query Test")
    print("=" * 30)
    
    try:
        config = load_snowflake_config()
        conn = connect_to_snowflake(config)
        cursor = conn.cursor()
        
        test_basic_queries(cursor)
        test_analytics_queries(cursor)
        
        print("\n All tests completed!")
        
    except Exception as e:
        print(f" Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print(" Connection closed.")

if __name__ == "__main__":
    main()
