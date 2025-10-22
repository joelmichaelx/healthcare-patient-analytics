"""
Medical Device Data Simulator for Healthcare Patient Analytics Platform
Simulates real-time data from medical devices for development and testing
"""

import random
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import pandas as pd
from kafka import KafkaProducer
import threading
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VitalSigns:
    """Vital signs data structure"""
    patient_id: str
    device_id: str
    timestamp: datetime
    heart_rate: int
    blood_pressure_systolic: int
    blood_pressure_diastolic: int
    temperature: float
    oxygen_saturation: int
    respiratory_rate: int
    device_status: str
    battery_level: int
    signal_quality: str

@dataclass
class LabResult:
    """Lab result data structure"""
    patient_id: str
    lab_id: str
    timestamp: datetime
    test_name: str
    test_value: float
    test_unit: str
    reference_range: str
    status: str
    critical_flag: bool

@dataclass
class MedicationEvent:
    """Medication administration event"""
    patient_id: str
    medication_id: str
    timestamp: datetime
    medication_name: str
    dosage: float
    unit: str
    route: str
    administered_by: str
    status: str

class MedicalDeviceSimulator:
    """
    Simulates medical devices generating real-time healthcare data
    Supports multiple device types and realistic data patterns
    """
    
    def __init__(self, kafka_bootstrap_servers: str = "localhost:9092"):
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.producer = None
        self.running = False
        self.devices = {}
        self.patients = {}
        
        # Initialize Kafka producer
        self._setup_kafka_producer()
        
        # Initialize patient data
        self._initialize_patients()
        
        # Initialize medical devices
        self._initialize_devices()
    
    def _setup_kafka_producer(self):
        """Set up Kafka producer for streaming data"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.kafka_bootstrap_servers,
                value_serializer=lambda x: json.dumps(x, default=str).encode('utf-8'),
                key_serializer=lambda x: x.encode('utf-8') if x else None
            )
            logger.info("Kafka producer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {str(e)}")
            self.producer = None
    
    def _initialize_patients(self):
        """Initialize patient data for simulation"""
        self.patients = {
            "P001": {
                "name": "John Smith",
                "age": 65,
                "gender": "Male",
                "condition": "Hypertension",
                "risk_level": "High",
                "baseline_vitals": {
                    "heart_rate": 75,
                    "blood_pressure_systolic": 140,
                    "blood_pressure_diastolic": 90,
                    "temperature": 98.6,
                    "oxygen_saturation": 98,
                    "respiratory_rate": 16
                }
            },
            "P002": {
                "name": "Sarah Johnson",
                "age": 45,
                "gender": "Female",
                "condition": "Diabetes",
                "risk_level": "Medium",
                "baseline_vitals": {
                    "heart_rate": 80,
                    "blood_pressure_systolic": 120,
                    "blood_pressure_diastolic": 80,
                    "temperature": 98.4,
                    "oxygen_saturation": 99,
                    "respiratory_rate": 14
                }
            },
            "P003": {
                "name": "Michael Brown",
                "age": 72,
                "gender": "Male",
                "condition": "Heart Disease",
                "risk_level": "Critical",
                "baseline_vitals": {
                    "heart_rate": 85,
                    "blood_pressure_systolic": 160,
                    "blood_pressure_diastolic": 95,
                    "temperature": 98.8,
                    "oxygen_saturation": 95,
                    "respiratory_rate": 18
                }
            },
            "P004": {
                "name": "Emily Davis",
                "age": 28,
                "gender": "Female",
                "condition": "Pregnancy",
                "risk_level": "Low",
                "baseline_vitals": {
                    "heart_rate": 70,
                    "blood_pressure_systolic": 110,
                    "blood_pressure_diastolic": 70,
                    "temperature": 98.2,
                    "oxygen_saturation": 99,
                    "respiratory_rate": 12
                }
            },
            "P005": {
                "name": "Robert Wilson",
                "age": 58,
                "gender": "Male",
                "condition": "COPD",
                "risk_level": "High",
                "baseline_vitals": {
                    "heart_rate": 90,
                    "blood_pressure_systolic": 130,
                    "blood_pressure_diastolic": 85,
                    "temperature": 98.5,
                    "oxygen_saturation": 92,
                    "respiratory_rate": 20
                }
            }
        }
    
    def _initialize_devices(self):
        """Initialize medical devices for simulation"""
        device_types = [
            "Vital Signs Monitor",
            "ECG Monitor",
            "Pulse Oximeter",
            "Blood Pressure Monitor",
            "Temperature Monitor",
            "Respiratory Monitor"
        ]
        
        for i, patient_id in enumerate(self.patients.keys()):
            device_id = f"DEV_{i+1:03d}"
            device_type = device_types[i % len(device_types)]
            
            self.devices[device_id] = {
                "device_id": device_id,
                "patient_id": patient_id,
                "device_type": device_type,
                "status": "Active",
                "battery_level": random.randint(80, 100),
                "signal_quality": "Good",
                "last_maintenance": datetime.now() - timedelta(days=random.randint(1, 30))
            }
    
    def _generate_vital_signs(self, patient_id: str, device_id: str) -> VitalSigns:
        """Generate realistic vital signs data for a patient"""
        patient = self.patients[patient_id]
        baseline = patient["baseline_vitals"]
        
        # Add realistic variations based on patient condition
        condition = patient["condition"]
        risk_level = patient["risk_level"]
        
        # Generate heart rate with condition-specific variations
        if condition == "Heart Disease":
            heart_rate = random.randint(60, 120)
        elif condition == "COPD":
            heart_rate = random.randint(80, 110)
        else:
            heart_rate = baseline["heart_rate"] + random.randint(-10, 10)
        
        # Generate blood pressure with condition-specific variations
        if condition == "Hypertension":
            bp_systolic = random.randint(140, 180)
            bp_diastolic = random.randint(90, 110)
        elif condition == "Heart Disease":
            bp_systolic = random.randint(120, 160)
            bp_diastolic = random.randint(80, 100)
        else:
            bp_systolic = baseline["blood_pressure_systolic"] + random.randint(-10, 10)
            bp_diastolic = baseline["blood_pressure_diastolic"] + random.randint(-5, 5)
        
        # Generate temperature with realistic variations
        temperature = baseline["temperature"] + random.uniform(-0.5, 0.5)
        
        # Generate oxygen saturation with condition-specific variations
        if condition == "COPD":
            oxygen_saturation = random.randint(88, 95)
        else:
            oxygen_saturation = random.randint(95, 100)
        
        # Generate respiratory rate with condition-specific variations
        if condition == "COPD":
            respiratory_rate = random.randint(18, 25)
        elif condition == "Pregnancy":
            respiratory_rate = random.randint(12, 16)
        else:
            respiratory_rate = baseline["respiratory_rate"] + random.randint(-2, 2)
        
        # Generate device status
        device_status = "Active" if random.random() > 0.05 else "Warning"
        battery_level = max(0, min(100, random.randint(70, 100)))
        signal_quality = random.choice(["Excellent", "Good", "Fair", "Poor"])
        
        return VitalSigns(
            patient_id=patient_id,
            device_id=device_id,
            timestamp=datetime.now(),
            heart_rate=heart_rate,
            blood_pressure_systolic=bp_systolic,
            blood_pressure_diastolic=bp_diastolic,
            temperature=round(temperature, 1),
            oxygen_saturation=oxygen_saturation,
            respiratory_rate=respiratory_rate,
            device_status=device_status,
            battery_level=battery_level,
            signal_quality=signal_quality
        )
    
    def _generate_lab_result(self, patient_id: str) -> LabResult:
        """Generate lab result data for a patient"""
        lab_tests = [
            {"name": "Glucose", "unit": "mg/dL", "range": "70-100", "critical": 300},
            {"name": "Hemoglobin", "unit": "g/dL", "range": "12-16", "critical": 8},
            {"name": "White Blood Cells", "unit": "K/uL", "range": "4.5-11.0", "critical": 20},
            {"name": "Creatinine", "unit": "mg/dL", "range": "0.6-1.2", "critical": 3.0},
            {"name": "Sodium", "unit": "mEq/L", "range": "136-145", "critical": 160},
            {"name": "Potassium", "unit": "mEq/L", "range": "3.5-5.0", "critical": 6.0}
        ]
        
        test = random.choice(lab_tests)
        
        # Generate realistic test values
        if test["name"] == "Glucose":
            value = random.uniform(80, 200)
        elif test["name"] == "Hemoglobin":
            value = random.uniform(10, 16)
        elif test["name"] == "White Blood Cells":
            value = random.uniform(4, 12)
        elif test["name"] == "Creatinine":
            value = random.uniform(0.8, 1.5)
        elif test["name"] == "Sodium":
            value = random.uniform(135, 145)
        else:  # Potassium
            value = random.uniform(3.5, 5.5)
        
        # Check for critical values
        critical_flag = value > test["critical"] if test["critical"] else False
        
        return LabResult(
            patient_id=patient_id,
            lab_id=f"LAB_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.now(),
            test_name=test["name"],
            test_value=round(value, 2),
            test_unit=test["unit"],
            reference_range=test["range"],
            status="Final",
            critical_flag=critical_flag
        )
    
    def _generate_medication_event(self, patient_id: str) -> MedicationEvent:
        """Generate medication administration event"""
        medications = [
            {"name": "Metformin", "dosage": 500, "unit": "mg", "route": "Oral"},
            {"name": "Lisinopril", "dosage": 10, "unit": "mg", "route": "Oral"},
            {"name": "Atorvastatin", "dosage": 20, "unit": "mg", "route": "Oral"},
            {"name": "Insulin", "dosage": 10, "unit": "units", "route": "Subcutaneous"},
            {"name": "Albuterol", "dosage": 2, "unit": "mg", "route": "Inhalation"},
            {"name": "Morphine", "dosage": 5, "unit": "mg", "route": "IV"}
        ]
        
        medication = random.choice(medications)
        
        return MedicationEvent(
            patient_id=patient_id,
            medication_id=f"MED_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.now(),
            medication_name=medication["name"],
            dosage=medication["dosage"],
            unit=medication["unit"],
            route=medication["route"],
            administered_by=random.choice(["Nurse_001", "Nurse_002", "Nurse_003"]),
            status="Administered"
        )
    
    def _send_to_kafka(self, topic: str, data: Any, key: str = None):
        """Send data to Kafka topic"""
        if not self.producer:
            logger.warning("Kafka producer not available")
            return
        
        try:
            # Convert dataclass to dictionary
            if hasattr(data, '__dataclass_fields__'):
                data_dict = asdict(data)
            else:
                data_dict = data
            
            # Send to Kafka
            self.producer.send(
                topic=topic,
                value=data_dict,
                key=key
            )
            
            logger.info(f"Sent data to Kafka topic: {topic}")
            
        except Exception as e:
            logger.error(f"Failed to send data to Kafka: {str(e)}")
    
    def start_vital_signs_simulation(self, interval_seconds: int = 30):
        """Start vital signs simulation for all devices"""
        def simulate_vital_signs():
            while self.running:
                try:
                    for device_id, device in self.devices.items():
                        if device["status"] == "Active":
                            # Generate vital signs
                            vital_signs = self._generate_vital_signs(
                                device["patient_id"], 
                                device_id
                            )
                            
                            # Send to Kafka
                            self._send_to_kafka(
                                topic="vital_signs",
                                data=vital_signs,
                                key=device["patient_id"]
                            )
                            
                            # Update device status
                            if vital_signs.device_status == "Warning":
                                device["status"] = "Warning"
                    
                    time.sleep(interval_seconds)
                    
                except Exception as e:
                    logger.error(f"Error in vital signs simulation: {str(e)}")
                    time.sleep(interval_seconds)
        
        # Start simulation thread
        self.running = True
        simulation_thread = threading.Thread(target=simulate_vital_signs)
        simulation_thread.daemon = True
        simulation_thread.start()
        
        logger.info("Vital signs simulation started")
    
    def start_lab_results_simulation(self, interval_seconds: int = 300):
        """Start lab results simulation"""
        def simulate_lab_results():
            while self.running:
                try:
                    # Generate lab results for random patients
                    patient_id = random.choice(list(self.patients.keys()))
                    lab_result = self._generate_lab_result(patient_id)
                    
                    # Send to Kafka
                    self._send_to_kafka(
                        topic="lab_results",
                        data=lab_result,
                        key=patient_id
                    )
                    
                    time.sleep(interval_seconds)
                    
                except Exception as e:
                    logger.error(f"Error in lab results simulation: {str(e)}")
                    time.sleep(interval_seconds)
        
        # Start simulation thread
        simulation_thread = threading.Thread(target=simulate_lab_results)
        simulation_thread.daemon = True
        simulation_thread.start()
        
        logger.info("Lab results simulation started")
    
    def start_medication_simulation(self, interval_seconds: int = 600):
        """Start medication administration simulation"""
        def simulate_medications():
            while self.running:
                try:
                    # Generate medication events for random patients
                    patient_id = random.choice(list(self.patients.keys()))
                    medication_event = self._generate_medication_event(patient_id)
                    
                    # Send to Kafka
                    self._send_to_kafka(
                        topic="medications",
                        data=medication_event,
                        key=patient_id
                    )
                    
                    time.sleep(interval_seconds)
                    
                except Exception as e:
                    logger.error(f"Error in medication simulation: {str(e)}")
                    time.sleep(interval_seconds)
        
        # Start simulation thread
        simulation_thread = threading.Thread(target=simulate_medications)
        simulation_thread.daemon = True
        simulation_thread.start()
        
        logger.info("Medication simulation started")
    
    def start_all_simulations(self):
        """Start all medical device simulations"""
        logger.info("Starting all medical device simulations...")
        
        # Start vital signs simulation (every 30 seconds)
        self.start_vital_signs_simulation(interval_seconds=30)
        
        # Start lab results simulation (every 5 minutes)
        self.start_lab_results_simulation(interval_seconds=300)
        
        # Start medication simulation (every 10 minutes)
        self.start_medication_simulation(interval_seconds=600)
        
        logger.info("All simulations started successfully")
    
    def stop_simulations(self):
        """Stop all simulations"""
        self.running = False
        logger.info("All simulations stopped")
    
    def get_device_status(self) -> Dict[str, Any]:
        """Get status of all medical devices"""
        return {
            "total_devices": len(self.devices),
            "active_devices": len([d for d in self.devices.values() if d["status"] == "Active"]),
            "warning_devices": len([d for d in self.devices.values() if d["status"] == "Warning"]),
            "devices": self.devices
        }
    
    def get_patient_summary(self) -> Dict[str, Any]:
        """Get summary of all patients"""
        return {
            "total_patients": len(self.patients),
            "patients": self.patients
        }
    
    def close(self):
        """Close the simulator and cleanup resources"""
        self.stop_simulations()
        
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed")
        
        logger.info("Medical device simulator closed")

# Example usage and testing
if __name__ == "__main__":
    # Create medical device simulator
    simulator = MedicalDeviceSimulator(kafka_bootstrap_servers="localhost:9092")
    
    try:
        # Start all simulations
        simulator.start_all_simulations()
        
        # Run for 5 minutes
        time.sleep(300)
        
        # Get status
        device_status = simulator.get_device_status()
        patient_summary = simulator.get_patient_summary()
        
        print(f"Device Status: {device_status}")
        print(f"Patient Summary: {patient_summary}")
        
    except KeyboardInterrupt:
        print("Simulation interrupted by user")
    
    finally:
        # Cleanup
        simulator.close()
        print("Simulation completed")
