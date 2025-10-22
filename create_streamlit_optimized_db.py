#!/usr/bin/env python3
"""
Healthcare Patient Analytics Platform - Streamlit Cloud Optimized Database
Creates a smaller, optimized database for Streamlit Cloud deployment
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker

# Initialize Faker for realistic data generation
fake = Faker()

def create_optimized_patient_dataset(num_patients=100):
    """Create optimized patient dataset for Streamlit Cloud"""
    print(f"Creating {num_patients} patients for Streamlit Cloud...")
    
    patients = []
    conditions = [
        "Hypertension", "Diabetes", "Heart Disease", "COPD", "Cancer", 
        "Pneumonia", "Stroke", "Kidney Disease", "Appendicitis", "Pregnancy"
    ]
    
    risk_levels = ["Low", "Medium", "High", "Critical"]
    risk_weights = [0.4, 0.3, 0.2, 0.1]
    
    genders = ["Male", "Female", "Other"]
    statuses = ["Active", "Discharged", "Critical", "Recovering"]
    
    for i in range(num_patients):
        patient_id = f"P{i+1:03d}"
        age = random.randint(18, 95)
        gender = random.choices(genders, weights=[0.48, 0.48, 0.04])[0]
        condition = random.choice(conditions)
        risk_level = random.choices(risk_levels, weights=risk_weights)[0]
        status = random.choices(statuses, weights=[0.6, 0.2, 0.1, 0.1])[0]
        
        # Generate admission date between 2024 and now
        start_date = datetime(2024, 1, 1)
        end_date = datetime.now()
        admission_date = fake.date_between(start_date=start_date, end_date=end_date)
        
        # Generate room based on risk level
        if risk_level == "Critical":
            room = f"ICU-{random.randint(1, 5)}"
        elif risk_level == "High":
            room = f"{random.randint(200, 300)}-{random.choice(['A', 'B', 'C'])}"
        else:
            room = f"{random.randint(100, 200)}-{random.choice(['A', 'B', 'C'])}"
        
        patients.append({
            "patient_id": patient_id,
            "name": fake.name(),
            "age": age,
            "gender": gender,
            "condition": condition,
            "risk_level": risk_level,
            "admission_date": admission_date.strftime("%Y-%m-%d"),
            "room": room,
            "status": status
        })
    
    return pd.DataFrame(patients)

def create_optimized_vital_signs_dataset(patients_df, records_per_patient=50):
    """Create optimized vital signs dataset for Streamlit Cloud"""
    print(f"Creating vital signs records for Streamlit Cloud...")
    
    vital_signs = []
    patient_ids = patients_df['patient_id'].tolist()
    
    for patient_id in patient_ids:
        # Get patient info for realistic vitals
        patient_info = patients_df[patients_df['patient_id'] == patient_id].iloc[0]
        age = patient_info['age']
        condition = patient_info['condition']
        risk_level = patient_info['risk_level']
        
        # Generate vital signs over last 30 days
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        for i in range(records_per_patient):
            # Generate timestamp between start_date and end_date
            timestamp = fake.date_time_between(start_date=start_date, end_date=end_date)
            
            # Generate realistic vital signs based on condition and age
            if condition == "Hypertension":
                heart_rate = random.randint(70, 100)
                bp_systolic = random.randint(140, 180)
                bp_diastolic = random.randint(90, 110)
            elif condition == "Heart Disease":
                heart_rate = random.randint(60, 120)
                bp_systolic = random.randint(120, 160)
                bp_diastolic = random.randint(80, 100)
            elif condition == "COPD":
                heart_rate = random.randint(80, 110)
                bp_systolic = random.randint(130, 150)
                bp_diastolic = random.randint(85, 95)
                oxygen_saturation = random.randint(88, 95)
            elif condition == "Pneumonia":
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
            
            # Adjust for age
            if age > 70:
                heart_rate = max(50, heart_rate - 5)
                bp_systolic = min(200, bp_systolic + 10)
            
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
    
    return pd.DataFrame(vital_signs)

def create_optimized_lab_results_dataset(patients_df, records_per_patient=20):
    """Create optimized lab results dataset for Streamlit Cloud"""
    print(f"Creating lab results records for Streamlit Cloud...")
    
    lab_tests = [
        {"name": "Glucose", "unit": "mg/dL", "range": "70-100", "critical_low": 40, "critical_high": 300},
        {"name": "Hemoglobin", "unit": "g/dL", "range": "12-16", "critical_low": 6, "critical_high": 20},
        {"name": "White Blood Cells", "unit": "K/uL", "range": "4.5-11.0", "critical_low": 1, "critical_high": 25},
        {"name": "Creatinine", "unit": "mg/dL", "range": "0.6-1.2", "critical_low": 0.3, "critical_high": 4.0},
        {"name": "Sodium", "unit": "mEq/L", "range": "136-145", "critical_low": 120, "critical_high": 160}
    ]
    
    lab_results = []
    patient_ids = patients_df['patient_id'].tolist()
    
    for patient_id in patient_ids:
        # Get patient info
        patient_info = patients_df[patients_df['patient_id'] == patient_id].iloc[0]
        condition = patient_info['condition']
        age = patient_info['age']
        
        for test in lab_tests:
            for i in range(records_per_patient // len(lab_tests)):
                # Generate timestamp
                start_date = datetime.now() - timedelta(days=30)
                end_date = datetime.now()
                timestamp = fake.date_time_between(start_date=start_date, end_date=end_date)
                
                # Generate realistic test values based on condition
                if test["name"] == "Glucose":
                    if condition == "Diabetes":
                        value = random.uniform(120, 250)
                    else:
                        value = random.uniform(80, 120)
                elif test["name"] == "Hemoglobin":
                    if condition == "Cancer":
                        value = random.uniform(8, 12)
                    else:
                        value = random.uniform(12, 16)
                elif test["name"] == "White Blood Cells":
                    if condition == "Cancer":
                        value = random.uniform(2, 8)
                    else:
                        value = random.uniform(4, 12)
                elif test["name"] == "Creatinine":
                    if condition == "Kidney Disease":
                        value = random.uniform(1.5, 3.0)
                    else:
                        value = random.uniform(0.6, 1.2)
                else:
                    # Generate normal values for other tests
                    value = random.uniform(50, 200)
                
                # Check for critical values (only 5% should be critical)
                critical = random.random() < 0.05
                if critical:
                    if random.random() < 0.5:
                        value = random.uniform(test["critical_low"] - 10, test["critical_low"])
                    else:
                        value = random.uniform(test["critical_high"], test["critical_high"] + 20)
                
                lab_results.append({
                    "patient_id": patient_id,
                    "test_name": test["name"],
                    "test_value": round(value, 2),
                    "test_unit": test["unit"],
                    "reference_range": test["range"],
                    "critical_flag": critical,
                    "timestamp": timestamp.isoformat()
                })
    
    return pd.DataFrame(lab_results)

def create_optimized_medications_dataset(patients_df, records_per_patient=30):
    """Create optimized medications dataset for Streamlit Cloud"""
    print(f"Creating medication records for Streamlit Cloud...")
    
    medications_list = [
        {"name": "Metformin", "dosage": 500, "unit": "mg", "route": "Oral"},
        {"name": "Lisinopril", "dosage": 10, "unit": "mg", "route": "Oral"},
        {"name": "Atorvastatin", "dosage": 20, "unit": "mg", "route": "Oral"},
        {"name": "Insulin", "dosage": 10, "unit": "units", "route": "Subcutaneous"},
        {"name": "Albuterol", "dosage": 2, "unit": "mg", "route": "Inhalation"},
        {"name": "Aspirin", "dosage": 81, "unit": "mg", "route": "Oral"}
    ]
    
    medications = []
    patient_ids = patients_df['patient_id'].tolist()
    
    for patient_id in patient_ids:
        # Get patient info
        patient_info = patients_df[patients_df['patient_id'] == patient_id].iloc[0]
        condition = patient_info['condition']
        
        # Select relevant medications based on condition
        if condition == "Diabetes":
            relevant_meds = ["Metformin", "Insulin", "Aspirin"]
        elif condition == "Hypertension":
            relevant_meds = ["Lisinopril", "Aspirin"]
        elif condition == "Heart Disease":
            relevant_meds = ["Aspirin", "Atorvastatin"]
        elif condition == "COPD":
            relevant_meds = ["Albuterol"]
        else:
            relevant_meds = random.sample([med["name"] for med in medications_list], random.randint(2, 4))
        
        for med_name in relevant_meds:
            med_info = next(med for med in medications_list if med["name"] == med_name)
            
            # Generate multiple administrations over time
            for i in range(records_per_patient // len(relevant_meds)):
                medications.append({
                    "patient_id": patient_id,
                    "medication_name": med_info["name"],
                    "dosage": med_info["dosage"],
                    "unit": med_info["unit"],
                    "route": med_info["route"],
                    "administered_by": f"Nurse_{random.randint(1, 10):03d}",
                    "timestamp": fake.date_time_between(
                        start_date=datetime.now() - timedelta(days=30), 
                        end_date=datetime.now()
                    ).isoformat(),
                    "status": "Administered"
                })
    
    return pd.DataFrame(medications)

def create_streamlit_optimized_database():
    """Create optimized database for Streamlit Cloud deployment"""
    print("Healthcare Patient Analytics Platform - Streamlit Cloud Optimized Database")
    print("=" * 70)
    
    # Connect to database
    conn = sqlite3.connect('healthcare_data_streamlit.db')
    cursor = conn.cursor()
    
    # Create database schema
    print("Creating database schema...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            condition TEXT,
            risk_level TEXT,
            admission_date TEXT,
            room TEXT,
            status TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vital_signs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            timestamp TEXT,
            heart_rate INTEGER,
            blood_pressure_systolic INTEGER,
            blood_pressure_diastolic INTEGER,
            temperature REAL,
            oxygen_saturation INTEGER,
            respiratory_rate INTEGER,
            FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lab_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            test_name TEXT,
            test_value REAL,
            test_unit TEXT,
            reference_range TEXT,
            critical_flag BOOLEAN,
            timestamp TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            medication_name TEXT,
            dosage REAL,
            unit TEXT,
            route TEXT,
            administered_by TEXT,
            timestamp TEXT,
            status TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
        )
    """)
    
    # Clear existing data
    print("Clearing existing data...")
    cursor.execute("DELETE FROM medications")
    cursor.execute("DELETE FROM lab_results")
    cursor.execute("DELETE FROM vital_signs")
    cursor.execute("DELETE FROM patients")
    conn.commit()
    print(" Database schema created and existing data cleared")
    
    # Create optimized datasets
    print("\nCreating Streamlit Cloud optimized dataset...")
    
    # 1. Create 1000 patients for full dataset
    patients_df = create_optimized_patient_dataset(1000)
    
    # 2. Create vital signs (50 records per patient = 5,000 records)
    vital_signs_df = create_optimized_vital_signs_dataset(patients_df, 50)
    
    # 3. Create lab results (20 records per patient = 2,000 records)
    lab_results_df = create_optimized_lab_results_dataset(patients_df, 20)
    
    # 4. Create medications (30 records per patient = 3,000 records)
    medications_df = create_optimized_medications_dataset(patients_df, 30)
    
    # Insert data into database
    print("\nInserting data into database...")
    
    # Insert patients
    print("Inserting patients...")
    for _, patient in patients_df.iterrows():
        cursor.execute("""
            INSERT INTO patients (patient_id, name, age, gender, condition, risk_level, admission_date, room, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient["patient_id"], patient["name"], patient["age"], patient["gender"],
            patient["condition"], patient["risk_level"], patient["admission_date"],
            patient["room"], patient["status"]
        ))
    
    # Insert vital signs
    print("Inserting vital signs...")
    for _, vs in vital_signs_df.iterrows():
        cursor.execute("""
            INSERT INTO vital_signs (patient_id, timestamp, heart_rate, blood_pressure_systolic, 
                                   blood_pressure_diastolic, temperature, oxygen_saturation, respiratory_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            vs["patient_id"], vs["timestamp"], vs["heart_rate"], vs["blood_pressure_systolic"],
            vs["blood_pressure_diastolic"], vs["temperature"], vs["oxygen_saturation"], vs["respiratory_rate"]
        ))
    
    # Insert lab results
    print("Inserting lab results...")
    for _, lab in lab_results_df.iterrows():
        cursor.execute("""
            INSERT INTO lab_results (patient_id, test_name, test_value, test_unit, reference_range, critical_flag, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            lab["patient_id"], lab["test_name"], lab["test_value"], lab["test_unit"],
            lab["reference_range"], lab["critical_flag"], lab["timestamp"]
        ))
    
    # Insert medications
    print("Inserting medications...")
    for _, med in medications_df.iterrows():
        cursor.execute("""
            INSERT INTO medications (patient_id, medication_name, dosage, unit, route, administered_by, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            med["patient_id"], med["medication_name"], med["dosage"], med["unit"],
            med["route"], med["administered_by"], med["timestamp"], med["status"]
        ))
    
    # Commit and close
    conn.commit()
    conn.close()
    
    # Summary
    print("\n Streamlit Cloud Optimized Database Complete!")
    print("=" * 50)
    print(f" Optimized Dataset Summary:")
    print(f"   • Patients: {len(patients_df):,}")
    print(f"   • Vital Signs: {len(vital_signs_df):,}")
    print(f"   • Lab Results: {len(lab_results_df):,}")
    print(f"   • Medications: {len(medications_df):,}")
    print(f"   • Total Records: {len(patients_df) + len(vital_signs_df) + len(lab_results_df) + len(medications_df):,}")
    print(f"   • Time Range: Last 30 days")
    print(f"   • Database Size: Optimized for Streamlit Cloud")
    print(f"\n Your healthcare analytics platform is now optimized for Streamlit Cloud!")

if __name__ == "__main__":
    create_streamlit_optimized_database()
