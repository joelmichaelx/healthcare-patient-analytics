#!/usr/bin/env python3
"""
Healthcare Kafka Producer
=========================
Real-time data streaming producer for healthcare data
including vital signs, lab results, and patient events.
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import uuid
import os
from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthcareKafkaProducer:
    """Healthcare data streaming producer for Kafka"""
    
    def __init__(self, bootstrap_servers='localhost:9092'):
        """Initialize Kafka producer"""
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.topics = {
            'vital_signs': 'healthcare.vital_signs',
            'lab_results': 'healthcare.lab_results',
            'medications': 'healthcare.medications',
            'patient_events': 'healthcare.patient_events',
            'alerts': 'healthcare.alerts'
        }
        
    def connect(self):
        """Connect to Kafka cluster"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',
                retries=3,
                retry_backoff_ms=100,
                request_timeout_ms=30000
            )
            logger.info(f"Connected to Kafka at {self.bootstrap_servers}")
            return True
        except KafkaError as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            return False
    
    def create_vital_signs_data(self, patient_id: str) -> Dict[str, Any]:
        """Create realistic vital signs data"""
        return {
            'patient_id': patient_id,
            'timestamp': datetime.now().isoformat(),
            'heart_rate': random.randint(60, 120),
            'blood_pressure_systolic': random.randint(100, 180),
            'blood_pressure_diastolic': random.randint(60, 110),
            'temperature': round(random.uniform(97.0, 100.0), 1),
            'oxygen_saturation': random.randint(90, 100),
            'respiratory_rate': random.randint(12, 25),
            'device_id': f"VS_{random.randint(1000, 9999)}",
            'nurse_id': f"N{random.randint(100, 999)}"
        }
    
    def create_lab_results_data(self, patient_id: str) -> Dict[str, Any]:
        """Create realistic lab results data"""
        lab_tests = [
            {'name': 'Glucose', 'unit': 'mg/dL', 'normal_range': (70, 100)},
            {'name': 'Hemoglobin', 'unit': 'g/dL', 'normal_range': (12, 16)},
            {'name': 'White Blood Cells', 'unit': 'K/uL', 'normal_range': (4.5, 11.0)},
            {'name': 'Creatinine', 'unit': 'mg/dL', 'normal_range': (0.6, 1.2)},
            {'name': 'Sodium', 'unit': 'mEq/L', 'normal_range': (136, 145)},
            {'name': 'Potassium', 'unit': 'mEq/L', 'normal_range': (3.5, 5.0)}
        ]
        
        test = random.choice(lab_tests)
        value = random.uniform(test['normal_range'][0], test['normal_range'][1] * 1.2)
        critical = value > test['normal_range'][1] * 1.5 or value < test['normal_range'][0] * 0.8
        
        return {
            'patient_id': patient_id,
            'test_name': test['name'],
            'test_value': round(value, 2),
            'test_unit': test['unit'],
            'reference_range': f"{test['normal_range'][0]}-{test['normal_range'][1]}",
            'critical_flag': critical,
            'timestamp': datetime.now().isoformat(),
            'lab_id': f"LAB_{random.randint(1000, 9999)}",
            'technician_id': f"T{random.randint(100, 999)}"
        }
    
    def create_medication_data(self, patient_id: str) -> Dict[str, Any]:
        """Create realistic medication data"""
        medications = [
            {'name': 'Metformin', 'dosage': 500, 'unit': 'mg', 'route': 'Oral'},
            {'name': 'Lisinopril', 'dosage': 10, 'unit': 'mg', 'route': 'Oral'},
            {'name': 'Atorvastatin', 'dosage': 20, 'unit': 'mg', 'route': 'Oral'},
            {'name': 'Insulin', 'dosage': 10, 'unit': 'units', 'route': 'Subcutaneous'},
            {'name': 'Albuterol', 'dosage': 2, 'unit': 'mg', 'route': 'Inhalation'},
            {'name': 'Morphine', 'dosage': 5, 'unit': 'mg', 'route': 'IV'}
        ]
        
        med = random.choice(medications)
        statuses = ['Administered', 'Scheduled', 'Missed', 'Delayed']
        
        return {
            'patient_id': patient_id,
            'medication_name': med['name'],
            'dosage': med['dosage'],
            'unit': med['unit'],
            'route': med['route'],
            'administration_time': datetime.now().isoformat(),
            'nurse_id': f"N{random.randint(100, 999)}",
            'status': random.choice(statuses),
            'medication_id': f"MED_{random.randint(1000, 9999)}"
        }
    
    def create_patient_event_data(self, patient_id: str) -> Dict[str, Any]:
        """Create patient event data"""
        events = [
            'Admission', 'Discharge', 'Transfer', 'Procedure', 'Consultation',
            'Emergency', 'Surgery', 'Therapy', 'Assessment', 'Follow-up'
        ]
        
        return {
            'patient_id': patient_id,
            'event_type': random.choice(events),
            'event_timestamp': datetime.now().isoformat(),
            'location': f"Room {random.randint(100, 999)}",
            'staff_id': f"S{random.randint(100, 999)}",
            'event_id': str(uuid.uuid4()),
            'description': f"Patient {patient_id} - {random.choice(events)} event"
        }
    
    def create_alert_data(self, patient_id: str) -> Dict[str, Any]:
        """Create clinical alert data"""
        alert_types = [
            'Critical Vital Signs', 'Medication Overdue', 'Lab Results Critical',
            'Patient Fall Risk', 'Infection Risk', 'Readmission Risk',
            'Sepsis Alert', 'Medication Interaction'
        ]
        
        severity_levels = ['Low', 'Medium', 'High', 'Critical']
        severity = random.choice(severity_levels)
        
        return {
            'patient_id': patient_id,
            'alert_type': random.choice(alert_types),
            'severity': severity,
            'timestamp': datetime.now().isoformat(),
            'alert_id': str(uuid.uuid4()),
            'message': f"Alert for patient {patient_id}: {random.choice(alert_types)}",
            'requires_immediate_action': severity in ['High', 'Critical'],
            'assigned_to': f"Dr.{random.choice(['Smith', 'Johnson', 'Williams', 'Brown'])}"
        }
    
    def send_vital_signs(self, patient_id: str):
        """Send vital signs data to Kafka"""
        if not self.producer:
            logger.error("Producer not connected")
            return False
        
        try:
            data = self.create_vital_signs_data(patient_id)
            self.producer.send(
                self.topics['vital_signs'],
                key=patient_id,
                value=data
            )
            logger.info(f"Sent vital signs for patient {patient_id}")
            return True
        except KafkaError as e:
            logger.error(f"Failed to send vital signs: {e}")
            return False
    
    def send_lab_results(self, patient_id: str):
        """Send lab results data to Kafka"""
        if not self.producer:
            logger.error("Producer not connected")
            return False
        
        try:
            data = self.create_lab_results_data(patient_id)
            self.producer.send(
                self.topics['lab_results'],
                key=patient_id,
                value=data
            )
            logger.info(f"Sent lab results for patient {patient_id}")
            return True
        except KafkaError as e:
            logger.error(f"Failed to send lab results: {e}")
            return False
    
    def send_medications(self, patient_id: str):
        """Send medication data to Kafka"""
        if not self.producer:
            logger.error("Producer not connected")
            return False
        
        try:
            data = self.create_medication_data(patient_id)
            self.producer.send(
                self.topics['medications'],
                key=patient_id,
                value=data
            )
            logger.info(f"Sent medication data for patient {patient_id}")
            return True
        except KafkaError as e:
            logger.error(f"Failed to send medication data: {e}")
            return False
    
    def send_patient_event(self, patient_id: str):
        """Send patient event data to Kafka"""
        if not self.producer:
            logger.error("Producer not connected")
            return False
        
        try:
            data = self.create_patient_event_data(patient_id)
            self.producer.send(
                self.topics['patient_events'],
                key=patient_id,
                value=data
            )
            logger.info(f"Sent patient event for patient {patient_id}")
            return True
        except KafkaError as e:
            logger.error(f"Failed to send patient event: {e}")
            return False
    
    def send_alert(self, patient_id: str):
        """Send alert data to Kafka"""
        if not self.producer:
            logger.error("Producer not connected")
            return False
        
        try:
            data = self.create_alert_data(patient_id)
            self.producer.send(
                self.topics['alerts'],
                key=patient_id,
                value=data
            )
            logger.info(f"Sent alert for patient {patient_id}")
            return True
        except KafkaError as e:
            logger.error(f"Failed to send alert: {e}")
            return False
    
    def stream_healthcare_data(self, patient_ids: List[str], duration_minutes: int = 5):
        """Stream healthcare data for multiple patients"""
        logger.info(f"Starting healthcare data streaming for {len(patient_ids)} patients")
        logger.info(f"Duration: {duration_minutes} minutes")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        while time.time() < end_time:
            for patient_id in patient_ids:
                # Send different types of data with different frequencies
                if random.random() < 0.7:  # 70% chance for vital signs
                    self.send_vital_signs(patient_id)
                
                if random.random() < 0.3:  # 30% chance for lab results
                    self.send_lab_results(patient_id)
                
                if random.random() < 0.4:  # 40% chance for medications
                    self.send_medications(patient_id)
                
                if random.random() < 0.1:  # 10% chance for patient events
                    self.send_patient_event(patient_id)
                
                if random.random() < 0.05:  # 5% chance for alerts
                    self.send_alert(patient_id)
            
            # Flush producer to ensure messages are sent
            self.producer.flush()
            
            # Wait before next batch
            time.sleep(2)
        
        logger.info("Healthcare data streaming completed")
    
    def close(self):
        """Close Kafka producer"""
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed")

def main():
    """Main function to demonstrate healthcare data streaming"""
    print("Healthcare Kafka Producer")
    print("=" * 30)
    
    # Initialize producer
    producer = HealthcareKafkaProducer()
    
    # Connect to Kafka
    if not producer.connect():
        print(" Failed to connect to Kafka")
        print("Please ensure Kafka is running on localhost:9092")
        return
    
    # Sample patient IDs
    patient_ids = [f"P{i:03d}" for i in range(1, 11)]  # P001 to P010
    
    try:
        # Stream data for 2 minutes
        producer.stream_healthcare_data(patient_ids, duration_minutes=2)
        print(" Healthcare data streaming completed successfully!")
        
    except KeyboardInterrupt:
        print("\n Streaming stopped by user")
    except Exception as e:
        print(f" Error during streaming: {e}")
    finally:
        producer.close()

if __name__ == "__main__":
    main()
