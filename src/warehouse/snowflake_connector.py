"""
Healthcare Patient Analytics Platform - Snowflake Connector
Handles connections and operations with Snowflake data warehouse
"""

import snowflake.connector
import pandas as pd
from typing import Dict, List, Optional, Any
import logging
from contextlib import contextmanager
from config.snowflake_config import SnowflakeConfigManager, get_healthcare_snowflake_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SnowflakeConnector:
    """Handles Snowflake connections and operations"""
    
    def __init__(self, config_manager: Optional[SnowflakeConfigManager] = None):
        self.config_manager = config_manager or SnowflakeConfigManager()
        self.config = self.config_manager.config
        self.healthcare_config = get_healthcare_snowflake_config()
    
    @contextmanager
    def get_connection(self):
        """Context manager for Snowflake connections"""
        conn = None
        try:
            conn = snowflake.connector.connect(
                account=self.config.account,
                user=self.config.user,
                password=self.config.password,
                warehouse=self.config.warehouse,
                database=self.config.database,
                schema=self.config.schema,
                role=self.config.role,
                region=self.config.region
            )
            yield conn
        except Exception as e:
            logger.error(f"Snowflake connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def test_connection(self) -> bool:
        """Test Snowflake connection"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT CURRENT_VERSION()")
                version = cursor.fetchone()[0]
                logger.info(f"Connected to Snowflake version: {version}")
                return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def create_warehouse(self, warehouse_name: str = "HEALTHCARE_WH") -> bool:
        """Create Snowflake warehouse for healthcare data"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create warehouse
                create_warehouse_sql = f"""
                CREATE WAREHOUSE IF NOT EXISTS {warehouse_name}
                WITH
                    WAREHOUSE_SIZE = '{self.healthcare_config['settings']['warehouse_size']}'
                    AUTO_SUSPEND = {self.healthcare_config['settings']['auto_suspend']}
                    AUTO_RESUME = {self.healthcare_config['settings']['auto_resume']}
                    STATEMENT_TIMEOUT_IN_SECONDS = {self.healthcare_config['settings']['statement_timeout']}
                    COMMENT = 'Healthcare Analytics Data Warehouse'
                """
                
                cursor.execute(create_warehouse_sql)
                logger.info(f"Warehouse {warehouse_name} created successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error creating warehouse: {e}")
            return False
    
    def create_database(self, database_name: str = "HEALTHCARE_DB") -> bool:
        """Create Snowflake database for healthcare data"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create database
                create_db_sql = f"""
                CREATE DATABASE IF NOT EXISTS {database_name}
                DATA_RETENTION_TIME_IN_DAYS = {self.healthcare_config['compliance']['data_retention_time_in_days']}
                COMMENT = 'Healthcare Patient Analytics Database'
                """
                
                cursor.execute(create_db_sql)
                logger.info(f"Database {database_name} created successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error creating database: {e}")
            return False
    
    def create_healthcare_tables(self) -> bool:
        """Create healthcare data tables in Snowflake"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Use healthcare database
                cursor.execute(f"USE DATABASE {self.config.database}")
                cursor.execute(f"USE SCHEMA {self.config.schema}")
                
                # Create patients table
                patients_table_sql = """
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
                """
                cursor.execute(patients_table_sql)
                
                # Create vital signs table
                vital_signs_sql = """
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
                """
                cursor.execute(vital_signs_sql)
                
                # Create lab results table
                lab_results_sql = """
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
                """
                cursor.execute(lab_results_sql)
                
                # Create medications table
                medications_sql = """
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
                """
                cursor.execute(medications_sql)
                
                # Create encounters table
                encounters_sql = """
                CREATE TABLE IF NOT EXISTS ENCOUNTERS (
                    ENCOUNTER_ID VARCHAR(50) PRIMARY KEY,
                    PATIENT_ID VARCHAR(50),
                    PROVIDER_ID VARCHAR(50),
                    ENCOUNTER_TYPE VARCHAR(100),
                    START_DATE TIMESTAMP,
                    END_DATE TIMESTAMP,
                    DIAGNOSIS VARCHAR(255),
                    STATUS VARCHAR(50),
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
                    FOREIGN KEY (PATIENT_ID) REFERENCES PATIENTS(PATIENT_ID)
                )
                """
                cursor.execute(encounters_sql)
                
                # Create providers table
                providers_sql = """
                CREATE TABLE IF NOT EXISTS PROVIDERS (
                    PROVIDER_ID VARCHAR(50) PRIMARY KEY,
                    NAME VARCHAR(255),
                    SPECIALTY VARCHAR(100),
                    DEPARTMENT VARCHAR(100),
                    LICENSE_NUMBER VARCHAR(50),
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
                )
                """
                cursor.execute(providers_sql)
                
                logger.info("All healthcare tables created successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            return False
    
    def setup_row_level_security(self) -> bool:
        """Set up row-level security for HIPAA compliance"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create RLS policies for patient data
                rls_policies = [
                    """
                    CREATE OR REPLACE ROW ACCESS POLICY patient_access_policy AS
                    (patient_id VARCHAR) RETURNS BOOLEAN ->
                    CURRENT_ROLE() IN ('HEALTHCARE_ADMIN', 'HEALTHCARE_ANALYST')
                    """,
                    """
                    CREATE OR REPLACE ROW ACCESS POLICY vital_signs_access_policy AS
                    (patient_id VARCHAR) RETURNS BOOLEAN ->
                    CURRENT_ROLE() IN ('HEALTHCARE_ADMIN', 'HEALTHCARE_ANALYST')
                    """,
                    """
                    CREATE OR REPLACE ROW ACCESS POLICY lab_results_access_policy AS
                    (patient_id VARCHAR) RETURNS BOOLEAN ->
                    CURRENT_ROLE() IN ('HEALTHCARE_ADMIN', 'HEALTHCARE_ANALYST')
                    """
                ]
                
                for policy in rls_policies:
                    cursor.execute(policy)
                
                # Apply RLS to tables
                cursor.execute("ALTER TABLE PATIENTS ADD ROW ACCESS POLICY patient_access_policy ON (PATIENT_ID)")
                cursor.execute("ALTER TABLE VITAL_SIGNS ADD ROW ACCESS POLICY vital_signs_access_policy ON (PATIENT_ID)")
                cursor.execute("ALTER TABLE LAB_RESULTS ADD ROW ACCESS POLICY lab_results_access_policy ON (PATIENT_ID)")
                
                logger.info("Row-level security policies created successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error setting up RLS: {e}")
            return False
    
    def load_data_from_sqlite(self, sqlite_db_path: str) -> bool:
        """Load data from SQLite database to Snowflake"""
        try:
            import sqlite3
            
            # Connect to SQLite database
            sqlite_conn = sqlite3.connect(sqlite_db_path)
            
            # Load data from SQLite
            patients_df = pd.read_sql_query("SELECT * FROM patients", sqlite_conn)
            vital_signs_df = pd.read_sql_query("SELECT * FROM vital_signs", sqlite_conn)
            lab_results_df = pd.read_sql_query("SELECT * FROM lab_results", sqlite_conn)
            medications_df = pd.read_sql_query("SELECT * FROM medications", sqlite_conn)
            
            sqlite_conn.close()
            
            # Load data to Snowflake
            with self.get_connection() as conn:
                # Load patients
                patients_df.to_sql('PATIENTS', conn, if_exists='append', index=False, method='multi')
                logger.info(f"Loaded {len(patients_df)} patients to Snowflake")
                
                # Load vital signs
                vital_signs_df.to_sql('VITAL_SIGNS', conn, if_exists='append', index=False, method='multi')
                logger.info(f"Loaded {len(vital_signs_df)} vital signs to Snowflake")
                
                # Load lab results
                lab_results_df.to_sql('LAB_RESULTS', conn, if_exists='append', index=False, method='multi')
                logger.info(f"Loaded {len(lab_results_df)} lab results to Snowflake")
                
                # Load medications
                medications_df.to_sql('MEDICATIONS', conn, if_exists='append', index=False, method='multi')
                logger.info(f"Loaded {len(medications_df)} medications to Snowflake")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading data to Snowflake: {e}")
            return False
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame"""
        try:
            with self.get_connection() as conn:
                return pd.read_sql(query, conn)
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return pd.DataFrame()
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get information about a table"""
        try:
            query = f"DESCRIBE TABLE {table_name}"
            result = self.execute_query(query)
            return result.to_dict('records')
        except Exception as e:
            logger.error(f"Error getting table info: {e}")
            return {}
    
    def get_table_count(self, table_name: str) -> int:
        """Get row count for a table"""
        try:
            query = f"SELECT COUNT(*) as count FROM {table_name}"
            result = self.execute_query(query)
            return result['COUNT'].iloc[0] if not result.empty else 0
        except Exception as e:
            logger.error(f"Error getting table count: {e}")
            return 0
