#!/usr/bin/env python3
"""
Healthcare Kafka Consumer
=========================
Real-time data processing consumer for healthcare streaming data
including vital signs monitoring, lab results processing, and alert handling.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Callable
import logging
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import threading
import queue

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthcareKafkaConsumer:
    """Healthcare data streaming consumer for Kafka"""
    
    def __init__(self, bootstrap_servers='localhost:9092', group_id='healthcare_consumer_group'):
        """Initialize Kafka consumer"""
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer = None
        self.topics = {
            'vital_signs': 'healthcare.vital_signs',
            'lab_results': 'healthcare.lab_results',
            'medications': 'healthcare.medications',
            'patient_events': 'healthcare.patient_events',
            'alerts': 'healthcare.alerts'
        }
        self.data_queue = queue.Queue()
        self.running = False
        self.threads = []
        
    def connect(self):
        """Connect to Kafka cluster"""
        try:
            self.consumer = KafkaConsumer(
                *self.topics.values(),
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                key_deserializer=lambda k: k.decode('utf-8') if k else None,
                auto_offset_reset='latest',
                enable_auto_commit=True,
                auto_commit_interval_ms=1000
            )
            logger.info(f"Connected to Kafka at {self.bootstrap_servers}")
            return True
        except KafkaError as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            return False
    
    def process_vital_signs(self, data: Dict[str, Any]):
        """Process vital signs data"""
        patient_id = data['patient_id']
        heart_rate = data['heart_rate']
        blood_pressure_systolic = data['blood_pressure_systolic']
        temperature = data['temperature']
        oxygen_saturation = data['oxygen_saturation']
        
        # Check for critical values
        alerts = []
        
        if heart_rate > 120 or heart_rate < 60:
            alerts.append(f"Critical heart rate: {heart_rate} bpm")
        
        if blood_pressure_systolic > 180 or blood_pressure_systolic < 90:
            alerts.append(f"Critical blood pressure: {blood_pressure_systolic} mmHg")
        
        if temperature > 100.4 or temperature < 96.0:
            alerts.append(f"Critical temperature: {temperature}°F")
        
        if oxygen_saturation < 90:
            alerts.append(f"Low oxygen saturation: {oxygen_saturation}%")
        
        # Log vital signs
        logger.info(f"Vital signs for {patient_id}: HR={heart_rate}, BP={blood_pressure_systolic}, Temp={temperature}, O2={oxygen_saturation}")
        
        # Process alerts
        for alert in alerts:
            self.process_alert({
                'patient_id': patient_id,
                'alert_type': 'Critical Vital Signs',
                'severity': 'High',
                'message': alert,
                'timestamp': datetime.now().isoformat()
            })
    
    def process_lab_results(self, data: Dict[str, Any]):
        """Process lab results data"""
        patient_id = data['patient_id']
        test_name = data['test_name']
        test_value = data['test_value']
        critical_flag = data['critical_flag']
        
        # Log lab results
        logger.info(f"Lab result for {patient_id}: {test_name}={test_value} {data['test_unit']}")
        
        # Process critical lab results
        if critical_flag:
            self.process_alert({
                'patient_id': patient_id,
                'alert_type': 'Critical Lab Result',
                'severity': 'Critical',
                'message': f"Critical {test_name}: {test_value} {data['test_unit']}",
                'timestamp': datetime.now().isoformat()
            })
    
    def process_medications(self, data: Dict[str, Any]):
        """Process medication data"""
        patient_id = data['patient_id']
        medication_name = data['medication_name']
        status = data['status']
        
        # Log medication data
        logger.info(f"Medication for {patient_id}: {medication_name} - {status}")
        
        # Process missed medications
        if status == 'Missed':
            self.process_alert({
                'patient_id': patient_id,
                'alert_type': 'Missed Medication',
                'severity': 'Medium',
                'message': f"Missed medication: {medication_name}",
                'timestamp': datetime.now().isoformat()
            })
    
    def process_patient_event(self, data: Dict[str, Any]):
        """Process patient event data"""
        patient_id = data['patient_id']
        event_type = data['event_type']
        
        # Log patient events
        logger.info(f"Patient event for {patient_id}: {event_type}")
        
        # Process emergency events
        if event_type == 'Emergency':
            self.process_alert({
                'patient_id': patient_id,
                'alert_type': 'Emergency Event',
                'severity': 'Critical',
                'message': f"Emergency event: {event_type}",
                'timestamp': datetime.now().isoformat()
            })
    
    def process_alert(self, alert_data: Dict[str, Any]):
        """Process alert data"""
        patient_id = alert_data['patient_id']
        alert_type = alert_data['alert_type']
        severity = alert_data['severity']
        message = alert_data['message']
        
        # Log alerts
        logger.warning(f"ALERT for {patient_id}: {alert_type} - {message}")
        
        # Store alert in queue for further processing
        self.data_queue.put({
            'type': 'alert',
            'data': alert_data,
            'timestamp': datetime.now().isoformat()
        })
    
    def process_message(self, message):
        """Process incoming Kafka message"""
        try:
            topic = message.topic
            data = message.value
            patient_id = message.key
            
            # Route message to appropriate processor
            if topic == self.topics['vital_signs']:
                self.process_vital_signs(data)
            elif topic == self.topics['lab_results']:
                self.process_lab_results(data)
            elif topic == self.topics['medications']:
                self.process_medications(data)
            elif topic == self.topics['patient_events']:
                self.process_patient_event(data)
            elif topic == self.topics['alerts']:
                self.process_alert(data)
            
            # Store processed data
            self.data_queue.put({
                'type': 'processed_data',
                'topic': topic,
                'patient_id': patient_id,
                'data': data,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def start_consuming(self):
        """Start consuming messages from Kafka"""
        if not self.consumer:
            logger.error("Consumer not connected")
            return False
        
        self.running = True
        logger.info("Starting to consume healthcare data...")
        
        try:
            for message in self.consumer:
                if not self.running:
                    break
                
                self.process_message(message)
                
        except KeyboardInterrupt:
            logger.info("Consumer stopped by user")
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
        finally:
            self.running = False
    
    def start_background_consuming(self):
        """Start consuming in background thread"""
        if not self.consumer:
            logger.error("Consumer not connected")
            return False
        
        self.running = True
        consumer_thread = threading.Thread(target=self.start_consuming)
        consumer_thread.daemon = True
        consumer_thread.start()
        self.threads.append(consumer_thread)
        
        logger.info("Started background consumer thread")
        return True
    
    def get_processed_data(self, timeout=1):
        """Get processed data from queue"""
        try:
            return self.data_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def get_all_processed_data(self):
        """Get all processed data from queue"""
        data_list = []
        while not self.data_queue.empty():
            try:
                data = self.data_queue.get_nowait()
                data_list.append(data)
            except queue.Empty:
                break
        return data_list
    
    def stop_consuming(self):
        """Stop consuming messages"""
        self.running = False
        if self.consumer:
            self.consumer.close()
        logger.info("Consumer stopped")
    
    def get_consumer_stats(self):
        """Get consumer statistics"""
        if not self.consumer:
            return None
        
        return {
            'group_id': self.group_id,
            'topics': list(self.topics.values()),
            'queue_size': self.data_queue.qsize(),
            'running': self.running
        }

def main():
    """Main function to demonstrate healthcare data consumption"""
    print("Healthcare Kafka Consumer")
    print("=" * 30)
    
    # Initialize consumer
    consumer = HealthcareKafkaConsumer()
    
    # Connect to Kafka
    if not consumer.connect():
        print(" Failed to connect to Kafka")
        print("Please ensure Kafka is running on localhost:9092")
        return
    
    try:
        # Start consuming
        print(" Starting healthcare data consumption...")
        print("Press Ctrl+C to stop")
        
        consumer.start_consuming()
        
    except KeyboardInterrupt:
        print("\n Consumer stopped by user")
    except Exception as e:
        print(f" Error during consumption: {e}")
    finally:
        consumer.stop_consuming()

if __name__ == "__main__":
    main()
