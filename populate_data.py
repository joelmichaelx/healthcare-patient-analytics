#!/usr/bin/env python3
"""
Healthcare Patient Analytics Platform - Data Population Script
Populates the database with realistic healthcare data for demonstration
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid

def create_sample_patients():
    """Create sample patient data"""
    patients = [
        {
            "patient_id": "P001",
            "name": "John Smith",
            "age": 65,
            "gender": "Male",
            "condition": "Hypertension",
            "risk_level": "High",
            "admission_date": "2024-01-15",
            "room": "201A",
            "status": "Active"
        },
        {
            "patient_id": "P002",
            "name": "Sarah Johnson",
            "age": 45,
            "gender": "Female",
            "condition": "Diabetes",
            "risk_level": "Medium",
            "admission_date": "2024-01-16",
            "room": "202B",
            "status": "Active"
        },
        {
            "patient_id": "P003",
            "name": "Michael Brown",
            "age": 72,
            "gender": "Male",
            "condition": "Heart Disease",
            "risk_level": "Critical",
            "admission_date": "2024-01-14",
            "room": "ICU-1",
            "status": "Critical"
        },
        {
            "patient_id": "P004",
            "name": "Emily Davis",
            "age": 28,
            "gender": "Female",
            "condition": "Pregnancy",
            "risk_level": "Low",
            "admission_date": "2024-01-17",
            "room": "301A",
            "status": "Active"
        },
        {
            "patient_id": "P005",
            "name": "Robert Wilson",
            "age": 58,
            "gender": "Male",
            "condition": "COPD",
            "risk_level": "High",
            "admission_date": "2024-01-13",
            "room": "302B",
            "status": "Active"
        },
        {
            "patient_id": "P006",
            "name": "Lisa Anderson",
            "age": 52,
            "gender": "Female",
            "condition": "Cancer",
            "risk_level": "Critical",
            "admission_date": "2024-01-12",
            "room": "ICU-2",
            "status": "Critical"
        },
        {
            "patient_id": "P007",
            "name": "David Miller",
            "age": 38,
            "gender": "Male",
            "condition": "Pneumonia",
            "risk_level": "Medium",
            "admission_date": "2024-01-18",
            "room": "203A",
            "status": "Active"
        },
        {
            "patient_id": "P008",
            "name": "Jennifer Taylor",
            "age": 61,
            "gender": "Female",
            "condition": "Stroke",
            "risk_level": "High",
            "admission_date": "2024-01-11",
            "room": "303A",
            "status": "Active"
        },
        {
            "patient_id": "P009",
            "name": "James Garcia",
            "age": 47,
            "gender": "Male",
            "condition": "Kidney Disease",
            "risk_level": "High",
            "admission_date": "2024-01-19",
            "room": "204B",
            "status": "Active"
        },
        {
            "patient_id": "P010",
            "name": "Maria Rodriguez",
            "age": 34,
            "gender": "Female",
            "condition": "Appendicitis",
            "risk_level": "Medium",
            "admission_date": "2024-01-20",
            "room": "205A",
            "status": "Active"
        }
    ]
    return patients

def create_vital_signs_data(patient_ids, days=7):
    """Create realistic vital signs data for patients"""
    vital_signs = []
    
    for patient_id in patient_ids:
        # Get patient info for realistic vitals
        patient_info = {
            "P001": {"condition": "Hypertension", "age": 65, "baseline_hr": 75, "baseline_bp": 140},
            "P002": {"condition": "Diabetes", "age": 45, "baseline_hr": 80, "baseline_bp": 120},
            "P003": {"condition": "Heart Disease", "age": 72, "baseline_hr": 85, "baseline_bp": 160},
            "P004": {"condition": "Pregnancy", "age": 28, "baseline_hr": 70, "baseline_bp": 110},
            "P005": {"condition": "COPD", "age": 58, "baseline_hr": 90, "baseline_bp": 130},
            "P006": {"condition": "Cancer", "age": 52, "baseline_hr": 88, "baseline_bp": 125},
            "P007": {"condition": "Pneumonia", "age": 38, "baseline_hr": 95, "baseline_bp": 115},
            "P008": {"condition": "Stroke", "age": 61, "baseline_hr": 82, "baseline_bp": 135},
            "P009": {"condition": "Kidney Disease", "age": 47, "baseline_hr": 78, "baseline_bp": 145},
            "P010": {"condition": "Appendicitis", "age": 34, "baseline_hr": 72, "baseline_bp": 105}
        }
        
        info = patient_info.get(patient_id, {"condition": "General", "age": 50, "baseline_hr": 75, "baseline_bp": 120})
        
        # Generate data for the last 7 days, every 4 hours
        for day in range(days):
            for hour in range(0, 24, 4):
                timestamp = datetime.now() - timedelta(days=day, hours=hour)
                
                # Generate realistic vital signs based on condition
                if info["condition"] == "Hypertension":
                    heart_rate = random.randint(70, 100)
                    bp_systolic = random.randint(140, 180)
                    bp_diastolic = random.randint(90, 110)
                elif info["condition"] == "Heart Disease":
                    heart_rate = random.randint(60, 120)
                    bp_systolic = random.randint(120, 160)
                    bp_diastolic = random.randint(80, 100)
                elif info["condition"] == "COPD":
                    heart_rate = random.randint(80, 110)
                    bp_systolic = random.randint(130, 150)
                    bp_diastolic = random.randint(85, 95)
                    oxygen_saturation = random.randint(88, 95)
                elif info["condition"] == "Pneumonia":
                    heart_rate = random.randint(85, 115)
                    bp_systolic = random.randint(110, 140)
                    bp_diastolic = random.randint(70, 90)
                    temperature = random.uniform(99.0, 102.0)
                else:
                    heart_rate = random.randint(60, 100)
                    bp_systolic = random.randint(100, 140)
                    bp_diastolic = random.randint(60, 90)
                
                # Default values if not set above
                if 'heart_rate' not in locals():
                    heart_rate = random.randint(60, 100)
                if 'bp_systolic' not in locals():
                    bp_systolic = random.randint(100, 140)
                if 'bp_diastolic' not in locals():
                    bp_diastolic = random.randint(60, 90)
                if 'oxygen_saturation' not in locals():
                    oxygen_saturation = random.randint(95, 100)
                if 'temperature' not in locals():
                    temperature = random.uniform(97.0, 99.5)
                
                vital_signs.append({
                    "patient_id": patient_id,
                    "timestamp": timestamp.isoformat(),
                    "heart_rate": heart_rate,
                    "blood_pressure_systolic": bp_systolic,
                    "blood_pressure_diastolic": bp_diastolic,
                    "temperature": round(temperature, 1),
                    "oxygen_saturation": oxygen_saturation,
                    "respiratory_rate": random.randint(12, 20)
                })
    
    return vital_signs

def create_lab_results_data(patient_ids):
    """Create realistic lab results data"""
    lab_tests = [
        {"name": "Glucose", "unit": "mg/dL", "range": "70-100", "critical": 300},
        {"name": "Hemoglobin", "unit": "g/dL", "range": "12-16", "critical": 8},
        {"name": "White Blood Cells", "unit": "K/uL", "range": "4.5-11.0", "critical": 20},
        {"name": "Creatinine", "unit": "mg/dL", "range": "0.6-1.2", "critical": 3.0},
        {"name": "Sodium", "unit": "mEq/L", "range": "136-145", "critical": 160},
        {"name": "Potassium", "unit": "mEq/L", "range": "3.5-5.0", "critical": 6.0},
        {"name": "Cholesterol", "unit": "mg/dL", "range": "<200", "critical": 300},
        {"name": "Triglycerides", "unit": "mg/dL", "range": "<150", "critical": 500}
    ]
    
    lab_results = []
    
    for patient_id in patient_ids:
        for test in lab_tests:
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
            elif test["name"] == "Potassium":
                value = random.uniform(3.5, 5.5)
            elif test["name"] == "Cholesterol":
                value = random.uniform(150, 300)
            else:  # Triglycerides
                value = random.uniform(100, 400)
            
            # Check for critical values
            critical_flag = value > test["critical"] if test["critical"] else False
            
            lab_results.append({
                "patient_id": patient_id,
                "test_name": test["name"],
                "test_value": round(value, 2),
                "test_unit": test["unit"],
                "reference_range": test["range"],
                "critical_flag": critical_flag,
                "timestamp": (datetime.now() - timedelta(hours=random.randint(1, 48))).isoformat()
            })
    
    return lab_results

def create_medications_data(patient_ids):
    """Create realistic medication data"""
    medications = [
        {"name": "Metformin", "dosage": 500, "unit": "mg", "route": "Oral"},
        {"name": "Lisinopril", "dosage": 10, "unit": "mg", "route": "Oral"},
        {"name": "Atorvastatin", "dosage": 20, "unit": "mg", "route": "Oral"},
        {"name": "Insulin", "dosage": 10, "unit": "units", "route": "Subcutaneous"},
        {"name": "Albuterol", "dosage": 2, "unit": "mg", "route": "Inhalation"},
        {"name": "Morphine", "dosage": 5, "unit": "mg", "route": "IV"},
        {"name": "Aspirin", "dosage": 81, "unit": "mg", "route": "Oral"},
        {"name": "Warfarin", "dosage": 5, "unit": "mg", "route": "Oral"},
        {"name": "Furosemide", "dosage": 40, "unit": "mg", "route": "Oral"},
        {"name": "Digoxin", "dosage": 0.25, "unit": "mg", "route": "Oral"}
    ]
    
    medication_data = []
    
    for patient_id in patient_ids:
        # Assign 2-4 medications per patient
        num_meds = random.randint(2, 4)
        patient_meds = random.sample(medications, num_meds)
        
        for med in patient_meds:
            # Generate multiple administrations over the last 3 days
            for i in range(random.randint(3, 8)):
                medication_data.append({
                    "patient_id": patient_id,
                    "medication_name": med["name"],
                    "dosage": med["dosage"],
                    "unit": med["unit"],
                    "route": med["route"],
                    "administered_by": f"Nurse_{random.randint(1, 5):03d}",
                    "timestamp": (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat(),
                    "status": "Administered"
                })
    
    return medication_data

def populate_database():
    """Populate the database with sample data"""
    print("Healthcare Patient Analytics Platform - Data Population")
    print("=" * 55)
    
    # Connect to database
    conn = sqlite3.connect('healthcare_data.db')
    cursor = conn.cursor()
    
    # Clear existing data
    print("Clearing existing data...")
    cursor.execute("DELETE FROM medications")
    cursor.execute("DELETE FROM lab_results")
    cursor.execute("DELETE FROM vital_signs")
    cursor.execute("DELETE FROM patients")
    conn.commit()
    print(" Existing data cleared")
    
    # Create sample data
    print("Creating sample patients...")
    patients = create_sample_patients()
    patient_ids = [p["patient_id"] for p in patients]
    
    # Insert patients
    for patient in patients:
        cursor.execute("""
            INSERT INTO patients (patient_id, name, age, gender, condition, risk_level, admission_date, room, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient["patient_id"], patient["name"], patient["age"], patient["gender"],
            patient["condition"], patient["risk_level"], patient["admission_date"],
            patient["room"], patient["status"]
        ))
    print(f" {len(patients)} patients created")
    
    # Create vital signs data
    print("Creating vital signs data...")
    vital_signs = create_vital_signs_data(patient_ids)
    for vs in vital_signs:
        cursor.execute("""
            INSERT INTO vital_signs (patient_id, timestamp, heart_rate, blood_pressure_systolic, 
                                   blood_pressure_diastolic, temperature, oxygen_saturation, respiratory_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            vs["patient_id"], vs["timestamp"], vs["heart_rate"], vs["blood_pressure_systolic"],
            vs["blood_pressure_diastolic"], vs["temperature"], vs["oxygen_saturation"], vs["respiratory_rate"]
        ))
    print(f" {len(vital_signs)} vital signs records created")
    
    # Create lab results data
    print("Creating lab results data...")
    lab_results = create_lab_results_data(patient_ids)
    for lab in lab_results:
        cursor.execute("""
            INSERT INTO lab_results (patient_id, test_name, test_value, test_unit, reference_range, critical_flag, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            lab["patient_id"], lab["test_name"], lab["test_value"], lab["test_unit"],
            lab["reference_range"], lab["critical_flag"], lab["timestamp"]
        ))
    print(f" {len(lab_results)} lab results created")
    
    # Create medications data
    print("Creating medications data...")
    medications = create_medications_data(patient_ids)
    for med in medications:
        cursor.execute("""
            INSERT INTO medications (patient_id, medication_name, dosage, unit, route, administered_by, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            med["patient_id"], med["medication_name"], med["dosage"], med["unit"],
            med["route"], med["administered_by"], med["timestamp"], med["status"]
        ))
    print(f" {len(medications)} medication records created")
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("\n Database population complete!")
    print(f" Data Summary:")
    print(f"   • Patients: {len(patients)}")
    print(f"   • Vital Signs: {len(vital_signs)}")
    print(f"   • Lab Results: {len(lab_results)}")
    print(f"   • Medications: {len(medications)}")
    print(f"\n Your dashboard now has realistic healthcare data!")
    print(f"   Open: http://localhost:8501")

if __name__ == "__main__":
    populate_database()
