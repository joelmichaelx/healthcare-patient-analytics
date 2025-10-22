#!/usr/bin/env python3
"""
Test script to verify database contents and data loading
"""

import sqlite3
import pandas as pd
import os

def test_database():
    """Test database contents"""
    print("Testing Healthcare Database...")
    print("=" * 40)
    
    # Test both databases
    databases = ['healthcare_data.db', 'healthcare_data_streamlit.db']
    
    for db_name in databases:
        if os.path.exists(db_name):
            print(f"\nDatabase: {db_name}")
            print("-" * 30)
            
            try:
                conn = sqlite3.connect(db_name)
                
                # Test patients table
                patients_df = pd.read_sql_query("SELECT COUNT(*) as count FROM patients", conn)
                print(f"Patients: {patients_df['count'].iloc[0]:,}")
                
                # Test vital signs table
                vital_signs_df = pd.read_sql_query("SELECT COUNT(*) as count FROM vital_signs", conn)
                print(f"Vital Signs: {vital_signs_df['count'].iloc[0]:,}")
                
                # Test lab results table
                lab_results_df = pd.read_sql_query("SELECT COUNT(*) as count FROM lab_results", conn)
                print(f"Lab Results: {lab_results_df['count'].iloc[0]:,}")
                
                # Test medications table
                medications_df = pd.read_sql_query("SELECT COUNT(*) as count FROM medications", conn)
                print(f"Medications: {medications_df['count'].iloc[0]:,}")
                
                # Show sample patients
                sample_patients = pd.read_sql_query("SELECT patient_id, name, age, risk_level FROM patients LIMIT 5", conn)
                print(f"\nSample Patients:")
                for _, row in sample_patients.iterrows():
                    print(f"  {row['patient_id']}: {row['name']}, Age {row['age']}, {row['risk_level']}")
                
                conn.close()
                
            except Exception as e:
                print(f"Error testing {db_name}: {e}")
        else:
            print(f"\nDatabase {db_name} not found")

def test_streamlit_data_loading():
    """Test the data loading function used by Streamlit"""
    print("\n\nTesting Streamlit Data Loading...")
    print("=" * 40)
    
    try:
        # Import the load_data function
        import sys
        sys.path.append('dashboards')
        from healthcare_streamlit_app import load_data
        
        # Load data
        data = load_data()
        
        if data and 'patients' in data:
            patients = data['patients']
            print(f"Loaded Patients: {len(patients):,}")
            print(f"Vital Signs: {len(data.get('vital_signs', [])):,}")
            print(f"Lab Results: {len(data.get('lab_results', [])):,}")
            print(f"Medications: {len(data.get('medications', [])):,}")
            
            # Show sample
            if not patients.empty:
                print(f"\nSample Patients from Streamlit:")
                for i, (_, row) in enumerate(patients.head(5).iterrows()):
                    print(f"  {row['patient_id']}: {row['name']}, Age {row['age']}, {row['risk_level']}")
        else:
            print("No data loaded")
            
    except Exception as e:
        print(f"Error testing Streamlit data loading: {e}")

if __name__ == "__main__":
    test_database()
    test_streamlit_data_loading()
