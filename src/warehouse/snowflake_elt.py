"""
Healthcare Patient Analytics Platform - Snowflake ELT Pipelines
Extract, Load, Transform pipelines for healthcare data in Snowflake
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
from snowflake_connector import SnowflakeConnector
from config.snowflake_config import SnowflakeConfigManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SnowflakeELT:
    """Handles ELT operations for healthcare data in Snowflake"""
    
    def __init__(self, connector: Optional[SnowflakeConnector] = None):
        self.connector = connector or SnowflakeConnector()
    
    def extract_from_sources(self) -> Dict[str, pd.DataFrame]:
        """Extract data from various healthcare sources"""
        logger.info("Starting data extraction from healthcare sources...")
        
        try:
            # Simulate data extraction from different sources
            # In production, this would connect to EHR systems, FHIR APIs, etc.
            
            extraction_results = {
                'patients': self._extract_patients(),
                'vital_signs': self._extract_vital_signs(),
                'lab_results': self._extract_lab_results(),
                'medications': self._extract_medications(),
                'encounters': self._extract_encounters(),
                'providers': self._extract_providers()
            }
            
            logger.info("Data extraction completed successfully")
            return extraction_results
            
        except Exception as e:
            logger.error(f"Error during data extraction: {e}")
            return {}
    
    def _extract_patients(self) -> pd.DataFrame:
        """Extract patient data from source systems"""
        # Simulate patient data extraction
        # In production, this would query EHR systems
        query = """
        SELECT 
            PATIENT_ID,
            NAME,
            AGE,
            GENDER,
            CONDITION,
            RISK_LEVEL,
            ADMISSION_DATE,
            ROOM,
            STATUS,
            CREATED_AT,
            UPDATED_AT
        FROM PATIENTS
        WHERE UPDATED_AT >= CURRENT_DATE() - 1
        """
        return self.connector.execute_query(query)
    
    def _extract_vital_signs(self) -> pd.DataFrame:
        """Extract vital signs data from medical devices"""
        query = """
        SELECT 
            PATIENT_ID,
            TIMESTAMP,
            HEART_RATE,
            BLOOD_PRESSURE_SYSTOLIC,
            BLOOD_PRESSURE_DIASTOLIC,
            TEMPERATURE,
            OXYGEN_SATURATION,
            RESPIRATORY_RATE
        FROM VITAL_SIGNS
        WHERE TIMESTAMP >= CURRENT_TIMESTAMP() - INTERVAL '24 HOURS'
        """
        return self.connector.execute_query(query)
    
    def _extract_lab_results(self) -> pd.DataFrame:
        """Extract lab results from laboratory systems"""
        query = """
        SELECT 
            PATIENT_ID,
            TEST_NAME,
            TEST_VALUE,
            TEST_UNIT,
            REFERENCE_RANGE,
            CRITICAL_FLAG,
            TIMESTAMP
        FROM LAB_RESULTS
        WHERE TIMESTAMP >= CURRENT_TIMESTAMP() - INTERVAL '7 DAYS'
        """
        return self.connector.execute_query(query)
    
    def _extract_medications(self) -> pd.DataFrame:
        """Extract medication data from pharmacy systems"""
        query = """
        SELECT 
            PATIENT_ID,
            MEDICATION_NAME,
            DOSAGE,
            UNIT,
            ROUTE,
            ADMINISTERED_BY,
            TIMESTAMP,
            STATUS
        FROM MEDICATIONS
        WHERE TIMESTAMP >= CURRENT_TIMESTAMP() - INTERVAL '30 DAYS'
        """
        return self.connector.execute_query(query)
    
    def _extract_encounters(self) -> pd.DataFrame:
        """Extract encounter data from EHR systems"""
        query = """
        SELECT 
            ENCOUNTER_ID,
            PATIENT_ID,
            PROVIDER_ID,
            ENCOUNTER_TYPE,
            START_DATE,
            END_DATE,
            DIAGNOSIS,
            STATUS
        FROM ENCOUNTERS
        WHERE START_DATE >= CURRENT_DATE() - 30
        """
        return self.connector.execute_query(query)
    
    def _extract_providers(self) -> pd.DataFrame:
        """Extract provider data from HR systems"""
        query = """
        SELECT 
            PROVIDER_ID,
            NAME,
            SPECIALTY,
            DEPARTMENT,
            LICENSE_NUMBER
        FROM PROVIDERS
        """
        return self.connector.execute_query(query)
    
    def transform_healthcare_data(self, data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """Transform healthcare data for analytics"""
        logger.info("Starting data transformation...")
        
        try:
            transformed_data = {}
            
            # Transform patient data
            if 'patients' in data and not data['patients'].empty:
                transformed_data['patients'] = self._transform_patients(data['patients'])
            
            # Transform vital signs data
            if 'vital_signs' in data and not data['vital_signs'].empty:
                transformed_data['vital_signs'] = self._transform_vital_signs(data['vital_signs'])
            
            # Transform lab results data
            if 'lab_results' in data and not data['lab_results'].empty:
                transformed_data['lab_results'] = self._transform_lab_results(data['lab_results'])
            
            # Transform medications data
            if 'medications' in data and not data['medications'].empty:
                transformed_data['medications'] = self._transform_medications(data['medications'])
            
            # Create analytics views
            transformed_data['patient_analytics'] = self._create_patient_analytics_view(transformed_data)
            transformed_data['clinical_metrics'] = self._create_clinical_metrics_view(transformed_data)
            
            logger.info("Data transformation completed successfully")
            return transformed_data
            
        except Exception as e:
            logger.error(f"Error during data transformation: {e}")
            return {}
    
    def _transform_patients(self, patients_df: pd.DataFrame) -> pd.DataFrame:
        """Transform patient data"""
        df = patients_df.copy()
        
        # Add calculated fields
        df['age_group'] = pd.cut(df['AGE'], bins=[0, 18, 35, 50, 65, 100], 
                               labels=['Pediatric', 'Young Adult', 'Adult', 'Middle Age', 'Senior'])
        
        # Risk score calculation
        risk_scores = {
            'Low': 1,
            'Medium': 2,
            'High': 3,
            'Critical': 4
        }
        df['risk_score'] = df['RISK_LEVEL'].map(risk_scores)
        
        # Add data quality flags
        df['has_complete_demographics'] = (
            df['NAME'].notna() & 
            df['AGE'].notna() & 
            df['GENDER'].notna()
        )
        
        return df
    
    def _transform_vital_signs(self, vital_signs_df: pd.DataFrame) -> pd.DataFrame:
        """Transform vital signs data"""
        df = vital_signs_df.copy()
        
        # Add vital signs categories
        df['heart_rate_category'] = pd.cut(
            df['HEART_RATE'], 
            bins=[0, 60, 100, 150, 300], 
            labels=['Low', 'Normal', 'High', 'Critical']
        )
        
        df['blood_pressure_category'] = pd.cut(
            df['BLOOD_PRESSURE_SYSTOLIC'],
            bins=[0, 90, 120, 140, 300],
            labels=['Low', 'Normal', 'High', 'Critical']
        )
        
        df['temperature_category'] = pd.cut(
            df['TEMPERATURE'],
            bins=[0, 95, 97, 100, 110],
            labels=['Hypothermia', 'Normal', 'Fever', 'Hyperthermia']
        )
        
        # Add critical vital signs flag
        df['critical_vitals'] = (
            (df['HEART_RATE'] < 50) | (df['HEART_RATE'] > 150) |
            (df['BLOOD_PRESSURE_SYSTOLIC'] < 80) | (df['BLOOD_PRESSURE_SYSTOLIC'] > 180) |
            (df['TEMPERATURE'] < 95) | (df['TEMPERATURE'] > 103)
        )
        
        return df
    
    def _transform_lab_results(self, lab_results_df: pd.DataFrame) -> pd.DataFrame:
        """Transform lab results data"""
        df = lab_results_df.copy()
        
        # Add lab result categories
        df['result_category'] = np.where(
            df['CRITICAL_FLAG'], 'Critical',
            np.where(df['TEST_VALUE'] > df['REFERENCE_RANGE'].str.split('-').str[1].astype(float), 'High',
            np.where(df['TEST_VALUE'] < df['REFERENCE_RANGE'].str.split('-').str[0].astype(float), 'Low', 'Normal'))
        )
        
        # Add trending analysis
        df['trending_up'] = df.groupby(['PATIENT_ID', 'TEST_NAME'])['TEST_VALUE'].diff() > 0
        df['trending_down'] = df.groupby(['PATIENT_ID', 'TEST_NAME'])['TEST_VALUE'].diff() < 0
        
        return df
    
    def _transform_medications(self, medications_df: pd.DataFrame) -> pd.DataFrame:
        """Transform medication data"""
        df = medications_df.copy()
        
        # Add medication categories
        medication_categories = {
            'Metformin': 'Diabetes',
            'Insulin': 'Diabetes',
            'Lisinopril': 'Cardiovascular',
            'Atorvastatin': 'Cardiovascular',
            'Albuterol': 'Respiratory',
            'Aspirin': 'Cardiovascular'
        }
        df['medication_category'] = df['MEDICATION_NAME'].map(medication_categories)
        
        # Add adherence tracking
        df['adherence_score'] = np.where(df['STATUS'] == 'Administered', 1, 0)
        
        return df
    
    def _create_patient_analytics_view(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Create patient analytics view"""
        if 'patients' not in data or data['patients'].empty:
            return pd.DataFrame()
        
        patients = data['patients']
        
        # Create analytics summary
        analytics = {
            'total_patients': len(patients),
            'average_age': patients['AGE'].mean(),
            'risk_distribution': patients['RISK_LEVEL'].value_counts().to_dict(),
            'condition_distribution': patients['CONDITION'].value_counts().to_dict(),
            'age_group_distribution': patients['age_group'].value_counts().to_dict()
        }
        
        return pd.DataFrame([analytics])
    
    def _create_clinical_metrics_view(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Create clinical metrics view"""
        metrics = {}
        
        if 'vital_signs' in data and not data['vital_signs'].empty:
            vital_signs = data['vital_signs']
            metrics.update({
                'critical_vitals_count': vital_signs['critical_vitals'].sum(),
                'average_heart_rate': vital_signs['HEART_RATE'].mean(),
                'average_temperature': vital_signs['TEMPERATURE'].mean()
            })
        
        if 'lab_results' in data and not data['lab_results'].empty:
            lab_results = data['lab_results']
            metrics.update({
                'critical_labs_count': lab_results['CRITICAL_FLAG'].sum(),
                'total_lab_tests': len(lab_results)
            })
        
        return pd.DataFrame([metrics])
    
    def load_to_analytics_tables(self, transformed_data: Dict[str, pd.DataFrame]) -> bool:
        """Load transformed data to analytics tables"""
        logger.info("Loading transformed data to analytics tables...")
        
        try:
            with self.connector.get_connection() as conn:
                # Load patient analytics
                if 'patient_analytics' in transformed_data:
                    transformed_data['patient_analytics'].to_sql(
                        'PATIENT_ANALYTICS', conn, if_exists='replace', index=False
                    )
                
                # Load clinical metrics
                if 'clinical_metrics' in transformed_data:
                    transformed_data['clinical_metrics'].to_sql(
                        'CLINICAL_METRICS', conn, if_exists='replace', index=False
                    )
                
                logger.info("Analytics tables loaded successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error loading analytics tables: {e}")
            return False
    
    def create_analytics_views(self) -> bool:
        """Create analytics views in Snowflake"""
        try:
            with self.connector.get_connection() as conn:
                cursor = conn.cursor()
                
                # Patient risk analysis view
                risk_analysis_view = """
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
                """
                cursor.execute(risk_analysis_view)
                
                # Clinical outcomes view
                outcomes_view = """
                CREATE OR REPLACE VIEW CLINICAL_OUTCOMES AS
                SELECT 
                    p.PATIENT_ID,
                    p.CONDITION,
                    p.RISK_LEVEL,
                    COUNT(DISTINCT e.ENCOUNTER_ID) as encounter_count,
                    COUNT(CASE WHEN lr.CRITICAL_FLAG = TRUE THEN 1 END) as critical_events,
                    AVG(vs.HEART_RATE) as avg_heart_rate,
                    MAX(vs.TIMESTAMP) as last_vital_check
                FROM PATIENTS p
                LEFT JOIN ENCOUNTERS e ON p.PATIENT_ID = e.PATIENT_ID
                LEFT JOIN LAB_RESULTS lr ON p.PATIENT_ID = lr.PATIENT_ID
                LEFT JOIN VITAL_SIGNS vs ON p.PATIENT_ID = vs.PATIENT_ID
                GROUP BY p.PATIENT_ID, p.CONDITION, p.RISK_LEVEL
                """
                cursor.execute(outcomes_view)
                
                logger.info("Analytics views created successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error creating analytics views: {e}")
            return False
    
    def run_full_elt_pipeline(self) -> bool:
        """Run complete ELT pipeline"""
        logger.info("Starting full ELT pipeline...")
        
        try:
            # Extract data
            extracted_data = self.extract_from_sources()
            if not extracted_data:
                logger.error("Data extraction failed")
                return False
            
            # Transform data
            transformed_data = self.transform_healthcare_data(extracted_data)
            if not transformed_data:
                logger.error("Data transformation failed")
                return False
            
            # Load to analytics tables
            if not self.load_to_analytics_tables(transformed_data):
                logger.error("Loading to analytics tables failed")
                return False
            
            # Create analytics views
            if not self.create_analytics_views():
                logger.error("Creating analytics views failed")
                return False
            
            logger.info("Full ELT pipeline completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"ELT pipeline failed: {e}")
            return False
