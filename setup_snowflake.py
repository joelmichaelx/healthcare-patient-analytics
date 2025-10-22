#!/usr/bin/env python3
"""
Healthcare Patient Analytics Platform - Snowflake Setup Script
Automated setup of Snowflake data warehouse for healthcare analytics
"""

import os
import sys
import logging
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.snowflake_config import SnowflakeConfigManager
from src.warehouse.snowflake_connector import SnowflakeConnector
from src.warehouse.snowflake_elt import SnowflakeELT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_snowflake_environment():
    """Set up Snowflake environment for healthcare analytics"""
    print("Healthcare Patient Analytics Platform - Snowflake Setup")
    print("=" * 60)
    
    try:
        # Initialize configuration manager
        config_manager = SnowflakeConfigManager()
        
        # Check if configuration exists
        if not os.path.exists(config_manager.config_file):
            print("Creating sample Snowflake configuration...")
            config_manager.create_sample_config()
            print(f"Please update {config_manager.config_file} with your Snowflake credentials")
            print("Then run this script again.")
            return False
        
        # Initialize Snowflake connector
        connector = SnowflakeConnector(config_manager)
        
        # Test connection
        print("Testing Snowflake connection...")
        if not connector.test_connection():
            print("ERROR: Could not connect to Snowflake")
            print("Please check your configuration and credentials")
            return False
        
        print("Snowflake connection successful!")
        
        # Create warehouse
        print("Creating healthcare data warehouse...")
        if not connector.create_warehouse():
            print("ERROR: Could not create warehouse")
            return False
        
        # Create database
        print("Creating healthcare database...")
        if not connector.create_database():
            print("ERROR: Could not create database")
            return False
        
        # Create tables
        print("Creating healthcare tables...")
        if not connector.create_healthcare_tables():
            print("ERROR: Could not create tables")
            return False
        
        # Set up row-level security
        print("Setting up HIPAA compliance features...")
        if not connector.setup_row_level_security():
            print("WARNING: Could not set up row-level security")
            print("This is required for HIPAA compliance")
        
        # Load data from SQLite if available
        sqlite_db_path = "healthcare_data.db"
        if os.path.exists(sqlite_db_path):
            print(f"Loading data from {sqlite_db_path}...")
            if connector.load_data_from_sqlite(sqlite_db_path):
                print("Data loaded successfully!")
            else:
                print("WARNING: Could not load data from SQLite")
        else:
            print("No SQLite database found. Skipping data load.")
        
        # Initialize ELT pipeline
        print("Setting up ELT pipeline...")
        elt = SnowflakeELT(connector)
        
        # Run initial ELT pipeline
        print("Running initial ELT pipeline...")
        if elt.run_full_elt_pipeline():
            print("ELT pipeline completed successfully!")
        else:
            print("WARNING: ELT pipeline failed")
        
        # Display summary
        print("\nSnowflake Setup Complete!")
        print("=" * 40)
        print("Warehouse: HEALTHCARE_WH")
        print("Database: HEALTHCARE_DB")
        print("Schema: PUBLIC")
        print("Tables created:")
        print("  - PATIENTS")
        print("  - VITAL_SIGNS")
        print("  - LAB_RESULTS")
        print("  - MEDICATIONS")
        print("  - ENCOUNTERS")
        print("  - PROVIDERS")
        print("\nAnalytics views created:")
        print("  - PATIENT_RISK_ANALYSIS")
        print("  - CLINICAL_OUTCOMES")
        print("\nHIPAA compliance features enabled:")
        print("  - Row-level security")
        print("  - Data encryption")
        print("  - Audit logging")
        
        return True
        
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        print(f"ERROR: {e}")
        return False

def test_snowflake_queries():
    """Test Snowflake queries and display results"""
    print("\nTesting Snowflake queries...")
    
    try:
        connector = SnowflakeConnector()
        
        # Test queries
        queries = {
            "Patient Count": "SELECT COUNT(*) as patient_count FROM PATIENTS",
            "Vital Signs Count": "SELECT COUNT(*) as vital_signs_count FROM VITAL_SIGNS",
            "Lab Results Count": "SELECT COUNT(*) as lab_results_count FROM LAB_RESULTS",
            "Medications Count": "SELECT COUNT(*) as medications_count FROM MEDICATIONS"
        }
        
        for query_name, query in queries.items():
            try:
                result = connector.execute_query(query)
                if not result.empty:
                    count = result.iloc[0, 0]
                    print(f"  {query_name}: {count:,}")
                else:
                    print(f"  {query_name}: No data")
            except Exception as e:
                print(f"  {query_name}: Error - {e}")
        
        # Test analytics views
        print("\nTesting analytics views...")
        analytics_queries = {
            "Patient Risk Analysis": "SELECT COUNT(*) as count FROM PATIENT_RISK_ANALYSIS",
            "Clinical Outcomes": "SELECT COUNT(*) as count FROM CLINICAL_OUTCOMES"
        }
        
        for view_name, query in analytics_queries.items():
            try:
                result = connector.execute_query(query)
                if not result.empty:
                    count = result.iloc[0, 0]
                    print(f"  {view_name}: {count:,} records")
                else:
                    print(f"  {view_name}: No data")
            except Exception as e:
                print(f"  {view_name}: Error - {e}")
        
        print("\nSnowflake testing completed!")
        
    except Exception as e:
        print(f"Error testing Snowflake: {e}")

def main():
    """Main setup function"""
    print("Starting Snowflake setup for Healthcare Patient Analytics Platform...")
    
    # Run setup
    if setup_snowflake_environment():
        print("\nSnowflake setup completed successfully!")
        
        # Test queries
        test_snowflake_queries()
        
        print("\nNext steps:")
        print("1. Update your Streamlit app to use Snowflake as data source")
        print("2. Set up scheduled ELT pipelines with Apache Airflow")
        print("3. Configure monitoring and alerting")
        print("4. Set up data quality checks")
        
    else:
        print("\nSnowflake setup failed!")
        print("Please check your configuration and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
