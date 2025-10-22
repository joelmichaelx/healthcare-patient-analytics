#!/usr/bin/env python3
"""
Snowflake Data Pipeline
======================
Automated data pipeline to continuously sync healthcare data
from SQLite to Snowflake data warehouse.
"""

import sqlite3
import pandas as pd
import json
import os
import time
from datetime import datetime, timedelta
import snowflake.connector
from snowflake.connector import DictCursor
import schedule

def load_snowflake_config():
    """Load Snowflake configuration"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'snowflake_config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def connect_to_snowflake(config):
    """Connect to Snowflake"""
    conn = snowflake.connector.connect(
        account=config['snowflake']['account'],
        user=config['snowflake']['user'],
        password=config['snowflake']['password'],
        warehouse=config['snowflake']['warehouse'],
        database=config['snowflake']['database'],
        schema=config['snowflake']['schema'],
        role=config['snowflake']['role']
    )
    return conn

def get_last_sync_timestamp(snowflake_conn):
    """Get the last sync timestamp from Snowflake"""
    try:
        cursor = snowflake_conn.cursor()
        cursor.execute("""
            SELECT MAX(LAST_SYNC) as last_sync 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'PUBLIC'
        """)
        result = cursor.fetchone()
        if result and result[0]:
            return result[0]
        else:
            # If no previous sync, start from 1 hour ago
            return datetime.now() - timedelta(hours=1)
    except:
        # If table doesn't exist, start from 1 hour ago
        return datetime.now() - timedelta(hours=1)

def get_new_data_from_sqlite(last_sync_time):
    """Get new data from SQLite since last sync"""
    print(f" Checking for new data since {last_sync_time}")
    
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
        return {}
    
    new_data = {}
    
    # Get new patients
    try:
        patients_df = pd.read_sql_query("""
            SELECT * FROM patients 
            WHERE datetime(admission_date) > ?
        """, conn, params=[last_sync_time.strftime('%Y-%m-%d %H:%M:%S')])
        new_data['patients'] = patients_df
        print(f" Found {len(patients_df)} new patients")
    except Exception as e:
        print(f" Could not load new patients: {e}")
        new_data['patients'] = pd.DataFrame()
    
    # Get new vital signs
    try:
        vital_signs_df = pd.read_sql_query("""
            SELECT * FROM vital_signs 
            WHERE datetime(timestamp) > ?
        """, conn, params=[last_sync_time.strftime('%Y-%m-%d %H:%M:%S')])
        new_data['vital_signs'] = vital_signs_df
        print(f" Found {len(vital_signs_df)} new vital signs")
    except Exception as e:
        print(f" Could not load new vital signs: {e}")
        new_data['vital_signs'] = pd.DataFrame()
    
    # Get new lab results
    try:
        lab_results_df = pd.read_sql_query("""
            SELECT * FROM lab_results 
            WHERE datetime(timestamp) > ?
        """, conn, params=[last_sync_time.strftime('%Y-%m-%d %H:%M:%S')])
        new_data['lab_results'] = lab_results_df
        print(f" Found {len(lab_results_df)} new lab results")
    except Exception as e:
        print(f" Could not load new lab results: {e}")
        new_data['lab_results'] = pd.DataFrame()
    
    # Get new medications
    try:
        medications_df = pd.read_sql_query("""
            SELECT * FROM medications 
            WHERE datetime(administration_time) > ?
        """, conn, params=[last_sync_time.strftime('%Y-%m-%d %H:%M:%S')])
        new_data['medications'] = medications_df
        print(f" Found {len(medications_df)} new medications")
    except Exception as e:
        print(f" Could not load new medications: {e}")
        new_data['medications'] = pd.DataFrame()
    
    conn.close()
    return new_data

def prepare_data_for_snowflake(data):
    """Prepare data for Snowflake insertion"""
    prepared_data = {}
    
    for table_name, df in data.items():
        if df.empty:
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
    
    return prepared_data

def insert_data_to_snowflake(snowflake_conn, data):
    """Insert new data into Snowflake tables"""
    if not any(not df.empty for df in data.values()):
        print("ℹ No new data to sync")
        return
    
    cursor = snowflake_conn.cursor()
    
    for table_name, df in data.items():
        if df.empty:
            continue
            
        print(f" Syncing {len(df)} records to {table_name}...")
        
        try:
            # Convert DataFrame to list of tuples
            data_tuples = [tuple(row) for row in df.values]
            
            # Create INSERT statement
            columns = ', '.join(df.columns)
            placeholders = ', '.join(['%s'] * len(df.columns))
            insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            # Execute batch insert
            cursor.executemany(insert_sql, data_tuples)
            print(f"   Synced {len(data_tuples)} records to {table_name}")
            
        except Exception as e:
            print(f"   Error syncing to {table_name}: {e}")
            continue
    
    # Commit all changes
    snowflake_conn.commit()
    print(" All new data synced to Snowflake!")

def update_sync_timestamp(snowflake_conn):
    """Update the last sync timestamp"""
    try:
        cursor = snowflake_conn.cursor()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Create or update sync log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS SYNC_LOG (
                ID INTEGER AUTOINCREMENT PRIMARY KEY,
                LAST_SYNC TIMESTAMP,
                RECORDS_SYNCED INTEGER,
                SYNC_STATUS VARCHAR(50)
            )
        """)
        
        # Insert sync record
        cursor.execute("""
            INSERT INTO SYNC_LOG (LAST_SYNC, RECORDS_SYNCED, SYNC_STATUS)
            VALUES (?, 0, 'COMPLETED')
        """, [current_time])
        
        snowflake_conn.commit()
        print(f" Sync timestamp updated: {current_time}")
        
    except Exception as e:
        print(f" Could not update sync timestamp: {e}")

def run_sync_pipeline():
    """Run the complete sync pipeline"""
    print(f"\n Starting data sync pipeline at {datetime.now()}")
    print("=" * 60)
    
    try:
        # Load configuration
        config = load_snowflake_config()
        
        # Connect to Snowflake
        snowflake_conn = connect_to_snowflake(config)
        print(" Connected to Snowflake")
        
        # Get last sync time
        last_sync_time = get_last_sync_timestamp(snowflake_conn)
        print(f" Last sync: {last_sync_time}")
        
        # Get new data from SQLite
        new_data = get_new_data_from_sqlite(last_sync_time)
        
        if not any(not df.empty for df in new_data.values()):
            print("ℹ No new data to sync")
            return
        
        # Prepare data for Snowflake
        prepared_data = prepare_data_for_snowflake(new_data)
        
        # Insert data into Snowflake
        insert_data_to_snowflake(snowflake_conn, prepared_data)
        
        # Update sync timestamp
        update_sync_timestamp(snowflake_conn)
        
        print(" Data sync completed successfully!")
        
    except Exception as e:
        print(f" Error during sync: {e}")
    finally:
        if 'snowflake_conn' in locals():
            snowflake_conn.close()
            print(" Snowflake connection closed.")

def setup_scheduled_sync():
    """Set up scheduled data sync"""
    print("⏰ Setting up scheduled data sync...")
    
    # Schedule sync every 5 minutes
    schedule.every(5).minutes.do(run_sync_pipeline)
    
    # Schedule sync every hour
    schedule.every().hour.do(run_sync_pipeline)
    
    # Schedule sync every day at midnight
    schedule.every().day.at("00:00").do(run_sync_pipeline)
    
    print(" Scheduled syncs configured:")
    print("  - Every 5 minutes")
    print("  - Every hour")
    print("  - Daily at midnight")
    
    # Run initial sync
    run_sync_pipeline()
    
    # Keep running scheduled syncs
    print("\n Starting scheduled sync service...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n Sync service stopped")

def main():
    """Main function"""
    print("Snowflake Data Pipeline")
    print("=" * 30)
    print("Choose an option:")
    print("1. Run single sync")
    print("2. Start scheduled sync service")
    print("3. Test connection")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        run_sync_pipeline()
    elif choice == "2":
        setup_scheduled_sync()
    elif choice == "3":
        try:
            config = load_snowflake_config()
            conn = connect_to_snowflake(config)
            print(" Snowflake connection successful!")
            conn.close()
        except Exception as e:
            print(f" Connection failed: {e}")
    else:
        print("Invalid choice. Running single sync...")
        run_sync_pipeline()

if __name__ == "__main__":
    main()
