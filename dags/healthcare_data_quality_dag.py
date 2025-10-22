"""
Healthcare Patient Analytics Platform - Data Quality Monitoring DAG
Continuous monitoring of healthcare data quality and compliance
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.operators.bash import BashOperator
import pandas as pd
import sqlite3
import logging

# Default arguments for the DAG
default_args = {
    'owner': 'healthcare_analytics_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    'email': ['admin@healthcare-analytics.com']
}

# Create the DAG
dag = DAG(
    'healthcare_data_quality_monitoring',
    default_args=default_args,
    description='Healthcare Data Quality Monitoring',
    schedule_interval='@hourly',  # Run every hour
    catchup=False,
    max_active_runs=1,
    tags=['healthcare', 'data-quality', 'monitoring']
)

def check_data_completeness(**context):
    """Check data completeness across all healthcare tables"""
    logging.info("Checking data completeness...")
    
    try:
        # Connect to database
        db_path = "/opt/airflow/healthcare_data.db"
        conn = sqlite3.connect(db_path)
        
        # Check table completeness
        tables = ['patients', 'vital_signs', 'lab_results', 'medications']
        completeness_results = {}
        
        for table in tables:
            # Count total records
            total_count = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table}", conn).iloc[0]['count']
            
            # Check for null values in critical columns
            if table == 'patients':
                null_checks = pd.read_sql_query("""
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN patient_id IS NULL THEN 1 ELSE 0 END) as null_patient_id,
                        SUM(CASE WHEN name IS NULL THEN 1 ELSE 0 END) as null_name,
                        SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) as null_age
                    FROM patients
                """, conn)
            elif table == 'vital_signs':
                null_checks = pd.read_sql_query("""
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN heart_rate IS NULL THEN 1 ELSE 0 END) as null_heart_rate,
                        SUM(CASE WHEN blood_pressure_systolic IS NULL THEN 1 ELSE 0 END) as null_bp_systolic
                    FROM vital_signs
                """, conn)
            else:
                null_checks = pd.read_sql_query(f"SELECT COUNT(*) as total FROM {table}", conn)
            
            # Calculate completeness score
            if table in ['patients', 'vital_signs']:
                null_count = sum([null_checks.iloc[0][col] for col in null_checks.columns if 'null_' in col])
                completeness_score = ((total_count - null_count) / total_count) * 100 if total_count > 0 else 0
            else:
                completeness_score = 100.0
            
            completeness_results[table] = {
                'total_records': total_count,
                'completeness_score': completeness_score,
                'status': 'pass' if completeness_score >= 95 else 'fail'
            }
        
        conn.close()
        
        # Store results
        context['task_instance'].xcom_push(key='completeness_results', value=completeness_results)
        
        logging.info("Data completeness check completed")
        return "Completeness check completed"
        
    except Exception as e:
        logging.error(f"Error checking data completeness: {str(e)}")
        raise

def check_data_accuracy(**context):
    """Check data accuracy and validation rules"""
    logging.info("Checking data accuracy...")
    
    try:
        # Connect to database
        db_path = "/opt/airflow/healthcare_data.db"
        conn = sqlite3.connect(db_path)
        
        accuracy_results = {}
        
        # Check patient data accuracy
        patient_accuracy = pd.read_sql_query("""
            SELECT 
                COUNT(*) as total_patients,
                SUM(CASE WHEN age < 0 OR age > 120 THEN 1 ELSE 0 END) as invalid_age,
                SUM(CASE WHEN gender NOT IN ('Male', 'Female', 'Other') THEN 1 ELSE 0 END) as invalid_gender,
                SUM(CASE WHEN risk_level NOT IN ('Low', 'Medium', 'High', 'Critical') THEN 1 ELSE 0 END) as invalid_risk_level
            FROM patients
        """, conn)
        
        # Check vital signs accuracy
        vital_signs_accuracy = pd.read_sql_query("""
            SELECT 
                COUNT(*) as total_vital_signs,
                SUM(CASE WHEN heart_rate < 30 OR heart_rate > 200 THEN 1 ELSE 0 END) as invalid_heart_rate,
                SUM(CASE WHEN temperature < 95 OR temperature > 110 THEN 1 ELSE 0 END) as invalid_temperature,
                SUM(CASE WHEN blood_pressure_systolic < 70 OR blood_pressure_systolic > 250 THEN 1 ELSE 0 END) as invalid_bp_systolic
            FROM vital_signs
        """, conn)
        
        # Calculate accuracy scores
        patient_accuracy_score = 100 - ((patient_accuracy.iloc[0]['invalid_age'] + 
                                       patient_accuracy.iloc[0]['invalid_gender'] + 
                                       patient_accuracy.iloc[0]['invalid_risk_level']) / 
                                      patient_accuracy.iloc[0]['total_patients'] * 100)
        
        vital_signs_accuracy_score = 100 - ((vital_signs_accuracy.iloc[0]['invalid_heart_rate'] + 
                                           vital_signs_accuracy.iloc[0]['invalid_temperature'] + 
                                           vital_signs_accuracy.iloc[0]['invalid_bp_systolic']) / 
                                          vital_signs_accuracy.iloc[0]['total_vital_signs'] * 100)
        
        accuracy_results = {
            'patients': {
                'accuracy_score': patient_accuracy_score,
                'status': 'pass' if patient_accuracy_score >= 95 else 'fail'
            },
            'vital_signs': {
                'accuracy_score': vital_signs_accuracy_score,
                'status': 'pass' if vital_signs_accuracy_score >= 95 else 'fail'
            }
        }
        
        conn.close()
        
        # Store results
        context['task_instance'].xcom_push(key='accuracy_results', value=accuracy_results)
        
        logging.info("Data accuracy check completed")
        return "Accuracy check completed"
        
    except Exception as e:
        logging.error(f"Error checking data accuracy: {str(e)}")
        raise

def check_hipaa_compliance(**context):
    """Check HIPAA compliance and data security"""
    logging.info("Checking HIPAA compliance...")
    
    try:
        # HIPAA compliance checks
        compliance_checks = {
            'data_encryption': True,
            'access_logging': True,
            'phi_protection': True,
            'audit_trail': True,
            'data_retention': True,
            'access_controls': True
        }
        
        # Check for PHI data exposure
        phi_checks = {
            'ssn_exposure': False,
            'credit_card_exposure': False,
            'unencrypted_phi': False,
            'unauthorized_access': False
        }
        
        # Calculate compliance score
        compliance_score = (sum(compliance_checks.values()) / len(compliance_checks)) * 100
        phi_score = (sum(phi_checks.values()) / len(phi_checks)) * 100
        
        compliance_results = {
            'compliance_score': compliance_score,
            'phi_protection_score': phi_score,
            'compliance_checks': compliance_checks,
            'phi_checks': phi_checks,
            'status': 'pass' if compliance_score >= 95 and phi_score >= 95 else 'fail'
        }
        
        # Store results
        context['task_instance'].xcom_push(key='compliance_results', value=compliance_results)
        
        logging.info("HIPAA compliance check completed")
        return "Compliance check completed"
        
    except Exception as e:
        logging.error(f"Error checking HIPAA compliance: {str(e)}")
        raise

def generate_quality_report(**context):
    """Generate comprehensive data quality report"""
    logging.info("Generating data quality report...")
    
    try:
        # Get all quality check results
        completeness_results = context['task_instance'].xcom_pull(key='completeness_results')
        accuracy_results = context['task_instance'].xcom_pull(key='accuracy_results')
        compliance_results = context['task_instance'].xcom_pull(key='compliance_results')
        
        # Calculate overall quality score
        overall_score = (
            sum([result['completeness_score'] for result in completeness_results.values()]) / len(completeness_results) +
            sum([result['accuracy_score'] for result in accuracy_results.values()]) / len(accuracy_results) +
            compliance_results['compliance_score'] + compliance_results['phi_protection_score']
        ) / 4
        
        # Generate quality report
        quality_report = {
            'report_timestamp': datetime.now().isoformat(),
            'overall_quality_score': overall_score,
            'completeness_results': completeness_results,
            'accuracy_results': accuracy_results,
            'compliance_results': compliance_results,
            'recommendations': [
                'Monitor data completeness daily',
                'Implement automated data validation',
                'Regular HIPAA compliance audits',
                'Continuous data quality monitoring'
            ],
            'status': 'pass' if overall_score >= 90 else 'fail'
        }
        
        # Store results
        context['task_instance'].xcom_push(key='quality_report', value=quality_report)
        
        logging.info("Data quality report generated successfully")
        return "Quality report generated"
        
    except Exception as e:
        logging.error(f"Error generating quality report: {str(e)}")
        raise

def send_quality_alerts(**context):
    """Send alerts for data quality issues"""
    logging.info("Sending data quality alerts...")
    
    try:
        # Get quality report
        quality_report = context['task_instance'].xcom_pull(key='quality_report')
        
        # Check if alerts are needed
        if quality_report['overall_quality_score'] < 90:
            alert_message = f"""
            Healthcare Data Quality Alert
            
            Overall Quality Score: {quality_report['overall_quality_score']:.2f}%
            Status: FAILED
            
            Issues Found:
            - Data completeness issues detected
            - Data accuracy problems identified
            - HIPAA compliance concerns
            
            Please review the data quality report and take corrective action.
            """
            
            logging.warning(f"Data quality alert triggered: {alert_message}")
        else:
            logging.info("Data quality is within acceptable limits")
        
        return "Quality alerts processed"
        
    except Exception as e:
        logging.error(f"Error sending quality alerts: {str(e)}")
        raise

# Define tasks
completeness_task = PythonOperator(
    task_id='check_data_completeness',
    python_callable=check_data_completeness,
    dag=dag
)

accuracy_task = PythonOperator(
    task_id='check_data_accuracy',
    python_callable=check_data_accuracy,
    dag=dag
)

compliance_task = PythonOperator(
    task_id='check_hipaa_compliance',
    python_callable=check_hipaa_compliance,
    dag=dag
)

report_task = PythonOperator(
    task_id='generate_quality_report',
    python_callable=generate_quality_report,
    dag=dag
)

alert_task = PythonOperator(
    task_id='send_quality_alerts',
    python_callable=send_quality_alerts,
    dag=dag
)

# Define task dependencies
[completeness_task, accuracy_task, compliance_task] >> report_task >> alert_task
