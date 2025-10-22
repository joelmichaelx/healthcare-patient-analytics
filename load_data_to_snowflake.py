#!/usr/bin/env python3
"""
Load Healthcare Data from SQLite to Snowflake
============================================
This script transfers all healthcare data from the local SQLite database
to the Snowflake data warehouse for enterprise-scale analytics.
"""

import sqlite3
import pandas as pd
import json
import os
from datetime import datetime
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

def load_sqlite_data():
    """Load data from SQLite database"""
    print(" Loading data from SQLite database...")
    
    # Try to load from the optimized database first
    db_paths = ['healthcare_data_streamlit.db', 'healthcare_data.db']
    conn = None
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            print(f" Found database: {db_path}")
            break
    
    if not conn:
        print(" No SQLite database found!")
        return None
    
    # Load all tables
    tables = {}
    
    # Load patients
    try:
        patients_df = pd.read_sql_query("SELECT * FROM patients", conn)
        tables['patients'] = patients_df
        print(f" Loaded {len(patients_df)} patients")
    except Exception as e:
        print(f" Could not load patients: {e}")
        tables['patients'] = pd.DataFrame()
    
    # Load vital signs
    try:
        vital_signs_df = pd.read_sql_query("SELECT * FROM vital_signs", conn)
        tables['vital_signs'] = vital_signs_df
        print(f" Loaded {len(vital_signs_df)} vital signs records")
    except Exception as e:
        print(f" Could not load vital signs: {e}")
        tables['vital_signs'] = pd.DataFrame()
    
    # Load lab results
    try:
        lab_results_df = pd.read_sql_query("SELECT * FROM lab_results", conn)
        tables['lab_results'] = lab_results_df
        print(f" Loaded {len(lab_results_df)} lab results")
    except Exception as e:
        print(f" Could not load lab results: {e}")
        tables['lab_results'] = pd.DataFrame()
    
    # Load medications
    try:
        medications_df = pd.read_sql_query("SELECT * FROM medications", conn)
        tables['medications'] = medications_df
        print(f" Loaded {len(medications_df)} medication records")
    except Exception as e:
        print(f" Could not load medications: {e}")
        tables['medications'] = pd.DataFrame()
    
    conn.close()
    return tables

def prepare_data_for_snowflake(data):
    """Prepare data for Snowflake insertion"""
    print(" Preparing data for Snowflake...")
    
    prepared_data = {}
    
    for table_name, df in data.items():
        if df.empty:
            print(f" Skipping empty table: {table_name}")
            continue
            
        # Convert column names to uppercase for Snowflake
        df_snowflake = df.copy()
        df_snowflake.columns = [col.upper() for col in df_snowflake.columns]
        
        # Handle timestamp columns - convert to string for Snowflake
        timestamp_cols = ['TIMESTAMP', 'ADMINISTRATION_TIME', 'CREATED_AT', 'UPDATED_AT']
        for col in timestamp_cols:
            if col in df_snowflake.columns:
                df_snowflake[col] = pd.to_datetime(df_snowflake[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Handle boolean columns
        if 'CRITICAL_FLAG' in df_snowflake.columns:
            df_snowflake['CRITICAL_FLAG'] = df_snowflake['CRITICAL_FLAG'].astype(bool)
        
        prepared_data[table_name] = df_snowflake
        print(f" Prepared {len(df_snowflake)} records for {table_name}")
    
    return prepared_data

def insert_data_to_snowflake(snowflake_conn, data):
    """Insert data into Snowflake tables"""
    print(" Inserting data into Snowflake...")
    
    cursor = snowflake_conn.cursor()
    
    for table_name, df in data.items():
        if df.empty:
            continue
            
        print(f"\n Inserting data into {table_name}...")
        
        try:
            # Clear existing data
            cursor.execute(f"DELETE FROM {table_name}")
            print(f"   Cleared existing data from {table_name}")
            
            # Insert new data
            if not df.empty:
                # Convert DataFrame to list of tuples
                data_tuples = [tuple(row) for row in df.values]
                
                # Create INSERT statement
                columns = ', '.join(df.columns)
                placeholders = ', '.join(['%s'] * len(df.columns))
                insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                
                # Execute batch insert
                cursor.executemany(insert_sql, data_tuples)
                print(f"   Inserted {len(data_tuples)} records into {table_name}")
            
        except Exception as e:
            print(f"   Error inserting into {table_name}: {e}")
            continue
    
    # Commit all changes
    snowflake_conn.commit()
    print("\n All data committed to Snowflake!")

def verify_data_in_snowflake(snowflake_conn):
    """Verify data was loaded correctly"""
    print("\n Verifying data in Snowflake...")
    
    cursor = snowflake_conn.cursor()
    
    tables_to_check = ['PATIENTS', 'VITAL_SIGNS', 'LAB_RESULTS', 'MEDICATIONS']
    
    for table in tables_to_check:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {table}: {count} records")
        except Exception as e:
            print(f"   {table}: Error - {e}")

def main():
    """Main function to load data from SQLite to Snowflake"""
    print("Healthcare Data Migration: SQLite → Snowflake")
    print("=" * 50)
    
    try:
        # Load configuration
        config = load_snowflake_config()
        
        # Connect to Snowflake
        snowflake_conn = connect_to_snowflake(config)
        
        # Load data from SQLite
        sqlite_data = load_sqlite_data()
        if not sqlite_data:
            print(" No data to migrate!")
            return
        
        # Prepare data for Snowflake
        prepared_data = prepare_data_for_snowflake(sqlite_data)
        
        # Insert data into Snowflake
        insert_data_to_snowflake(snowflake_conn, prepared_data)
        
        # Verify data
        verify_data_in_snowflake(snowflake_conn)
        
        print("\n Data migration completed successfully!")
        print("Your healthcare data is now available in Snowflake for enterprise analytics!")
        
    except Exception as e:
        print(f" Error during migration: {e}")
    finally:
        if 'snowflake_conn' in locals():
            snowflake_conn.close()
            print(" Snowflake connection closed.")

if __name__ == "__main__":
    main()
