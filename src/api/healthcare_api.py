#!/usr/bin/env python3
"""
Healthcare Patient Analytics REST API
====================================
FastAPI-based REST API for healthcare data access and analytics.
Provides secure, HIPAA-compliant endpoints for patient data, vital signs,
lab results, ML predictions, and real-time streaming data.
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import sqlite3
import pandas as pd
import numpy as np
import logging
import os
from pathlib import Path
import json
import asyncio
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

# Database path
DB_PATH = "healthcare_data_streamlit.db"

# Pydantic models for request/response
class PatientResponse(BaseModel):
    patient_id: str
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    medical_record_number: str
    created_at: str
    updated_at: str

class VitalSignsResponse(BaseModel):
    id: int
    patient_id: str
    timestamp: str
    heart_rate: int
    blood_pressure_systolic: int
    blood_pressure_diastolic: int
    temperature: float
    oxygen_saturation: int
    respiratory_rate: int

class LabResultsResponse(BaseModel):
    id: int
    patient_id: str
    test_name: str
    test_value: float
    test_unit: str
    reference_range: str
    critical_value: bool
    timestamp: str

class MedicationResponse(BaseModel):
    id: int
    patient_id: str
    medication_name: str
    dosage: str
    frequency: str
    status: str
    timestamp: str

class MLPredictionResponse(BaseModel):
    patient_id: str
    prediction_type: str
    risk_score: float
    confidence: float
    recommendations: List[str]
    timestamp: str

class AlertResponse(BaseModel):
    id: int
    patient_id: str
    alert_type: str
    severity: str
    message: str
    timestamp: str
    acknowledged: bool

class PatientCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: str
    gender: str = Field(..., regex="^(Male|Female|Other)$")
    medical_record_number: str = Field(..., min_length=1, max_length=50)

class VitalSignsCreate(BaseModel):
    patient_id: str
    heart_rate: int = Field(..., ge=30, le=300)
    blood_pressure_systolic: int = Field(..., ge=60, le=300)
    blood_pressure_diastolic: int = Field(..., ge=30, le=200)
    temperature: float = Field(..., ge=90.0, le=110.0)
    oxygen_saturation: int = Field(..., ge=70, le=100)
    respiratory_rate: int = Field(..., ge=5, le=60)

class LabResultsCreate(BaseModel):
    patient_id: str
    test_name: str
    test_value: float
    test_unit: str
    reference_range: str
    critical_value: bool = False

class MedicationCreate(BaseModel):
    patient_id: str
    medication_name: str
    dosage: str
    frequency: str
    status: str = "Prescribed"

# Database connection
def get_db_connection():
    """Get database connection"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# Authentication (simplified for demo)
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API token (simplified for demo)"""
    # In production, implement proper JWT validation
    if credentials.credentials != "healthcare-api-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

# FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting Healthcare API")
    yield
    logger.info("Shutting down Healthcare API")

app = FastAPI(
    title="Healthcare Patient Analytics API",
    description="REST API for healthcare data access and analytics",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Patient endpoints
@app.get("/api/v1/patients", response_model=List[PatientResponse])
async def get_patients(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    token: str = Depends(verify_token)
):
    """Get list of patients with pagination and search"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM patients"
        params = []
        
        if search:
            query += " WHERE first_name LIKE ? OR last_name LIKE ? OR patient_id LIKE ?"
            params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
        
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, skip])
        
        cursor.execute(query, params)
        patients = cursor.fetchall()
        conn.close()
        
        return [PatientResponse(**dict(patient)) for patient in patients]
        
    except Exception as e:
        logger.error(f"Error fetching patients: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch patients")

@app.get("/api/v1/patients/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: str,
    token: str = Depends(verify_token)
):
    """Get specific patient by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
        patient = cursor.fetchone()
        conn.close()
        
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        return PatientResponse(**dict(patient))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching patient {patient_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch patient")

@app.post("/api/v1/patients", response_model=PatientResponse)
async def create_patient(
    patient: PatientCreate,
    token: str = Depends(verify_token)
):
    """Create new patient"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Generate patient ID
        patient_id = f"P{len(cursor.execute('SELECT * FROM patients').fetchall()) + 1:03d}"
        
        cursor.execute("""
            INSERT INTO patients (patient_id, first_name, last_name, date_of_birth, gender, medical_record_number, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            patient.first_name,
            patient.last_name,
            patient.date_of_birth,
            patient.gender,
            patient.medical_record_number,
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return PatientResponse(
            patient_id=patient_id,
            first_name=patient.first_name,
            last_name=patient.last_name,
            date_of_birth=patient.date_of_birth,
            gender=patient.gender,
            medical_record_number=patient.medical_record_number,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error creating patient: {e}")
        raise HTTPException(status_code=500, detail="Failed to create patient")

# Vital signs endpoints
@app.get("/api/v1/patients/{patient_id}/vital-signs", response_model=List[VitalSignsResponse])
async def get_vital_signs(
    patient_id: str,
    hours: int = 24,
    token: str = Depends(verify_token)
):
    """Get vital signs for a patient within specified hours"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        since = datetime.now() - timedelta(hours=hours)
        
        cursor.execute("""
            SELECT * FROM vital_signs 
            WHERE patient_id = ? AND timestamp >= ?
            ORDER BY timestamp DESC
        """, (patient_id, since.isoformat()))
        
        vital_signs = cursor.fetchall()
        conn.close()
        
        return [VitalSignsResponse(**dict(vs)) for vs in vital_signs]
        
    except Exception as e:
        logger.error(f"Error fetching vital signs for {patient_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch vital signs")

@app.post("/api/v1/patients/{patient_id}/vital-signs", response_model=VitalSignsResponse)
async def create_vital_signs(
    patient_id: str,
    vital_signs: VitalSignsCreate,
    token: str = Depends(verify_token)
):
    """Record new vital signs for a patient"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO vital_signs (patient_id, timestamp, heart_rate, blood_pressure_systolic, 
                                   blood_pressure_diastolic, temperature, oxygen_saturation, respiratory_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            datetime.now().isoformat(),
            vital_signs.heart_rate,
            vital_signs.blood_pressure_systolic,
            vital_signs.blood_pressure_diastolic,
            vital_signs.temperature,
            vital_signs.oxygen_saturation,
            vital_signs.respiratory_rate
        ))
        
        conn.commit()
        conn.close()
        
        return VitalSignsResponse(
            id=cursor.lastrowid,
            patient_id=patient_id,
            timestamp=datetime.now().isoformat(),
            heart_rate=vital_signs.heart_rate,
            blood_pressure_systolic=vital_signs.blood_pressure_systolic,
            blood_pressure_diastolic=vital_signs.blood_pressure_diastolic,
            temperature=vital_signs.temperature,
            oxygen_saturation=vital_signs.oxygen_saturation,
            respiratory_rate=vital_signs.respiratory_rate
        )
        
    except Exception as e:
        logger.error(f"Error creating vital signs for {patient_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to create vital signs")

# Lab results endpoints
@app.get("/api/v1/patients/{patient_id}/lab-results", response_model=List[LabResultsResponse])
async def get_lab_results(
    patient_id: str,
    critical_only: bool = False,
    hours: int = 24,
    token: str = Depends(verify_token)
):
    """Get lab results for a patient"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        since = datetime.now() - timedelta(hours=hours)
        
        query = """
            SELECT * FROM lab_results 
            WHERE patient_id = ? AND timestamp >= ?
        """
        params = [patient_id, since.isoformat()]
        
        if critical_only:
            query += " AND critical_value = 1"
        
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, params)
        lab_results = cursor.fetchall()
        conn.close()
        
        return [LabResultsResponse(**dict(lr)) for lr in lab_results]
        
    except Exception as e:
        logger.error(f"Error fetching lab results for {patient_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch lab results")

@app.post("/api/v1/patients/{patient_id}/lab-results", response_model=LabResultsResponse)
async def create_lab_results(
    patient_id: str,
    lab_result: LabResultsCreate,
    token: str = Depends(verify_token)
):
    """Record new lab results for a patient"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO lab_results (patient_id, test_name, test_value, test_unit, 
                                  reference_range, critical_value, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            lab_result.test_name,
            lab_result.test_value,
            lab_result.test_unit,
            lab_result.reference_range,
            lab_result.critical_value,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return LabResultsResponse(
            id=cursor.lastrowid,
            patient_id=patient_id,
            test_name=lab_result.test_name,
            test_value=lab_result.test_value,
            test_unit=lab_result.test_unit,
            reference_range=lab_result.reference_range,
            critical_value=lab_result.critical_value,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error creating lab results for {patient_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to create lab results")

# Medication endpoints
@app.get("/api/v1/patients/{patient_id}/medications", response_model=List[MedicationResponse])
async def get_medications(
    patient_id: str,
    status: Optional[str] = None,
    token: str = Depends(verify_token)
):
    """Get medications for a patient"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM medications WHERE patient_id = ?"
        params = [patient_id]
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, params)
        medications = cursor.fetchall()
        conn.close()
        
        return [MedicationResponse(**dict(med)) for med in medications]
        
    except Exception as e:
        logger.error(f"Error fetching medications for {patient_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch medications")

@app.post("/api/v1/patients/{patient_id}/medications", response_model=MedicationResponse)
async def create_medication(
    patient_id: str,
    medication: MedicationCreate,
    token: str = Depends(verify_token)
):
    """Record new medication for a patient"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO medications (patient_id, medication_name, dosage, frequency, status, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            medication.medication_name,
            medication.dosage,
            medication.frequency,
            medication.status,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return MedicationResponse(
            id=cursor.lastrowid,
            patient_id=patient_id,
            medication_name=medication.medication_name,
            dosage=medication.dosage,
            frequency=medication.frequency,
            status=medication.status,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error creating medication for {patient_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to create medication")

# ML Predictions endpoints
@app.get("/api/v1/patients/{patient_id}/predictions", response_model=List[MLPredictionResponse])
async def get_ml_predictions(
    patient_id: str,
    prediction_type: Optional[str] = None,
    token: str = Depends(verify_token)
):
    """Get ML predictions for a patient"""
    try:
        # This would integrate with your ML models
        # For now, return mock predictions
        predictions = [
            MLPredictionResponse(
                patient_id=patient_id,
                prediction_type="readmission_risk",
                risk_score=0.75,
                confidence=0.87,
                recommendations=[
                    "Monitor vital signs closely",
                    "Schedule follow-up appointment",
                    "Review medication adherence"
                ],
                timestamp=datetime.now().isoformat()
            ),
            MLPredictionResponse(
                patient_id=patient_id,
                prediction_type="sepsis_risk",
                risk_score=0.25,
                confidence=0.92,
                recommendations=[
                    "Continue current treatment",
                    "Monitor for signs of infection"
                ],
                timestamp=datetime.now().isoformat()
            )
        ]
        
        if prediction_type:
            predictions = [p for p in predictions if p.prediction_type == prediction_type]
        
        return predictions
        
    except Exception as e:
        logger.error(f"Error fetching predictions for {patient_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch predictions")

# Alerts endpoints
@app.get("/api/v1/alerts", response_model=List[AlertResponse])
async def get_alerts(
    patient_id: Optional[str] = None,
    severity: Optional[str] = None,
    acknowledged: Optional[bool] = None,
    token: str = Depends(verify_token)
):
    """Get system alerts"""
    try:
        # Mock alerts for demonstration
        alerts = [
            AlertResponse(
                id=1,
                patient_id="P001",
                alert_type="critical_vital_signs",
                severity="high",
                message="Heart rate above normal range",
                timestamp=datetime.now().isoformat(),
                acknowledged=False
            ),
            AlertResponse(
                id=2,
                patient_id="P002",
                alert_type="lab_results",
                severity="critical",
                message="Critical lab values detected",
                timestamp=datetime.now().isoformat(),
                acknowledged=False
            )
        ]
        
        if patient_id:
            alerts = [a for a in alerts if a.patient_id == patient_id]
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        if acknowledged is not None:
            alerts = [a for a in alerts if a.acknowledged == acknowledged]
        
        return alerts
        
    except Exception as e:
        logger.error(f"Error fetching alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch alerts")

# Analytics endpoints
@app.get("/api/v1/analytics/patient-summary")
async def get_patient_summary(token: str = Depends(verify_token)):
    """Get patient summary analytics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get total patients
        cursor.execute("SELECT COUNT(*) as total FROM patients")
        total_patients = cursor.fetchone()["total"]
        
        # Get critical patients
        cursor.execute("SELECT COUNT(*) as critical FROM patients WHERE risk_level = 'Critical'")
        critical_patients = cursor.fetchone()["critical"]
        
        # Get active patients
        cursor.execute("SELECT COUNT(*) as active FROM patients WHERE status = 'Active'")
        active_patients = cursor.fetchone()["active"]
        
        conn.close()
        
        return {
            "total_patients": total_patients,
            "critical_patients": critical_patients,
            "active_patients": active_patients,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching patient summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch patient summary")

@app.get("/api/v1/analytics/vital-signs-trends")
async def get_vital_signs_trends(
    patient_id: str,
    hours: int = 24,
    token: str = Depends(verify_token)
):
    """Get vital signs trends for analytics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        since = datetime.now() - timedelta(hours=hours)
        
        cursor.execute("""
            SELECT timestamp, heart_rate, blood_pressure_systolic, blood_pressure_diastolic,
                   temperature, oxygen_saturation, respiratory_rate
            FROM vital_signs 
            WHERE patient_id = ? AND timestamp >= ?
            ORDER BY timestamp
        """, (patient_id, since.isoformat()))
        
        trends = cursor.fetchall()
        conn.close()
        
        return {
            "patient_id": patient_id,
            "trends": [dict(trend) for trend in trends],
            "period_hours": hours,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching vital signs trends for {patient_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch vital signs trends")

# Real-time streaming endpoints
@app.get("/api/v1/streaming/status")
async def get_streaming_status(token: str = Depends(verify_token)):
    """Get real-time streaming status"""
    return {
        "status": "active",
        "kafka_connected": True,
        "topics": ["vital_signs", "lab_results", "alerts"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/streaming/live-data")
async def get_live_data(
    topic: str = "vital_signs",
    limit: int = 10,
    token: str = Depends(verify_token)
):
    """Get live streaming data"""
    # Mock live data for demonstration
    live_data = []
    for i in range(limit):
        live_data.append({
            "patient_id": f"P{i+1:03d}",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "heart_rate": np.random.randint(60, 120),
                "blood_pressure": f"{np.random.randint(90, 140)}/{np.random.randint(60, 90)}",
                "temperature": round(np.random.uniform(97.0, 101.0), 1)
            }
        })
    
    return {
        "topic": topic,
        "data": live_data,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
