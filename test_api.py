#!/usr/bin/env python3
"""
Healthcare API Test Script
========================
Test script for the Healthcare Patient Analytics REST API.
"""

import requests
import json
import time
from datetime import datetime

# API Configuration
BASE_URL = "http://localhost:8000"
API_TOKEN = "healthcare-api-token"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_patients():
    """Test patient endpoints"""
    print("\n👥 Testing patient endpoints...")
    
    # Get all patients
    try:
        response = requests.get(f"{BASE_URL}/api/v1/patients", headers=HEADERS)
        if response.status_code == 200:
            patients = response.json()
            print(f"✅ Retrieved {len(patients)} patients")
            if patients:
                print(f"   First patient: {patients[0]['first_name']} {patients[0]['last_name']}")
        else:
            print(f"❌ Failed to get patients: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting patients: {e}")
    
    # Get specific patient
    try:
        response = requests.get(f"{BASE_URL}/api/v1/patients/P001", headers=HEADERS)
        if response.status_code == 200:
            patient = response.json()
            print(f"✅ Retrieved patient P001: {patient['first_name']} {patient['last_name']}")
        else:
            print(f"❌ Failed to get patient P001: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting patient P001: {e}")

def test_vital_signs():
    """Test vital signs endpoints"""
    print("\n💓 Testing vital signs endpoints...")
    
    # Get vital signs for patient
    try:
        response = requests.get(f"{BASE_URL}/api/v1/patients/P001/vital-signs", headers=HEADERS)
        if response.status_code == 200:
            vital_signs = response.json()
            print(f"✅ Retrieved {len(vital_signs)} vital signs records")
            if vital_signs:
                vs = vital_signs[0]
                print(f"   Latest: HR={vs['heart_rate']}, BP={vs['blood_pressure_systolic']}/{vs['blood_pressure_diastolic']}")
        else:
            print(f"❌ Failed to get vital signs: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting vital signs: {e}")

def test_lab_results():
    """Test lab results endpoints"""
    print("\n🧪 Testing lab results endpoints...")
    
    # Get lab results for patient
    try:
        response = requests.get(f"{BASE_URL}/api/v1/patients/P001/lab-results", headers=HEADERS)
        if response.status_code == 200:
            lab_results = response.json()
            print(f"✅ Retrieved {len(lab_results)} lab results")
            if lab_results:
                lr = lab_results[0]
                print(f"   Latest: {lr['test_name']}={lr['test_value']} {lr['test_unit']}")
        else:
            print(f"❌ Failed to get lab results: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting lab results: {e}")

def test_medications():
    """Test medication endpoints"""
    print("\n💊 Testing medication endpoints...")
    
    # Get medications for patient
    try:
        response = requests.get(f"{BASE_URL}/api/v1/patients/P001/medications", headers=HEADERS)
        if response.status_code == 200:
            medications = response.json()
            print(f"✅ Retrieved {len(medications)} medications")
            if medications:
                med = medications[0]
                print(f"   Latest: {med['medication_name']} {med['dosage']}")
        else:
            print(f"❌ Failed to get medications: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting medications: {e}")

def test_ml_predictions():
    """Test ML predictions endpoints"""
    print("\n🤖 Testing ML predictions endpoints...")
    
    # Get ML predictions for patient
    try:
        response = requests.get(f"{BASE_URL}/api/v1/patients/P001/predictions", headers=HEADERS)
        if response.status_code == 200:
            predictions = response.json()
            print(f"✅ Retrieved {len(predictions)} predictions")
            for pred in predictions:
                print(f"   {pred['prediction_type']}: {pred['risk_score']:.2f} (confidence: {pred['confidence']:.2f})")
        else:
            print(f"❌ Failed to get predictions: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting predictions: {e}")

def test_alerts():
    """Test alerts endpoints"""
    print("\n🚨 Testing alerts endpoints...")
    
    # Get alerts
    try:
        response = requests.get(f"{BASE_URL}/api/v1/alerts", headers=HEADERS)
        if response.status_code == 200:
            alerts = response.json()
            print(f"✅ Retrieved {len(alerts)} alerts")
            for alert in alerts:
                print(f"   {alert['alert_type']}: {alert['message']} (severity: {alert['severity']})")
        else:
            print(f"❌ Failed to get alerts: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting alerts: {e}")

def test_analytics():
    """Test analytics endpoints"""
    print("\n📊 Testing analytics endpoints...")
    
    # Get patient summary
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analytics/patient-summary", headers=HEADERS)
        if response.status_code == 200:
            summary = response.json()
            print("✅ Retrieved patient summary")
            print(f"   Total patients: {summary['total_patients']}")
            print(f"   Critical patients: {summary['critical_patients']}")
            print(f"   Active patients: {summary['active_patients']}")
        else:
            print(f"❌ Failed to get patient summary: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting patient summary: {e}")
    
    # Get vital signs trends
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analytics/vital-signs-trends?patient_id=P001", headers=HEADERS)
        if response.status_code == 200:
            trends = response.json()
            print(f"✅ Retrieved vital signs trends for {trends['patient_id']}")
            print(f"   Trends count: {len(trends['trends'])}")
        else:
            print(f"❌ Failed to get vital signs trends: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting vital signs trends: {e}")

def test_streaming():
    """Test streaming endpoints"""
    print("\n📡 Testing streaming endpoints...")
    
    # Get streaming status
    try:
        response = requests.get(f"{BASE_URL}/api/v1/streaming/status", headers=HEADERS)
        if response.status_code == 200:
            status = response.json()
            print("✅ Retrieved streaming status")
            print(f"   Status: {status['status']}")
            print(f"   Kafka connected: {status['kafka_connected']}")
            print(f"   Topics: {', '.join(status['topics'])}")
        else:
            print(f"❌ Failed to get streaming status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting streaming status: {e}")
    
    # Get live data
    try:
        response = requests.get(f"{BASE_URL}/api/v1/streaming/live-data", headers=HEADERS)
        if response.status_code == 200:
            live_data = response.json()
            print(f"✅ Retrieved live data from topic: {live_data['topic']}")
            print(f"   Data points: {len(live_data['data'])}")
        else:
            print(f"❌ Failed to get live data: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting live data: {e}")

def test_authentication():
    """Test authentication"""
    print("\n🔐 Testing authentication...")
    
    # Test without token
    try:
        response = requests.get(f"{BASE_URL}/api/v1/patients")
        if response.status_code == 401:
            print("✅ Authentication required (no token)")
        else:
            print(f"❌ Expected 401, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing authentication: {e}")
    
    # Test with invalid token
    try:
        headers = {"Authorization": "Bearer invalid-token"}
        response = requests.get(f"{BASE_URL}/api/v1/patients", headers=headers)
        if response.status_code == 401:
            print("✅ Invalid token rejected")
        else:
            print(f"❌ Expected 401, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing invalid token: {e}")

def main():
    """Run all API tests"""
    print("🏥 Healthcare API Test Suite")
    print("=" * 50)
    print(f"Testing API at: {BASE_URL}")
    print(f"Using token: {API_TOKEN}")
    print("=" * 50)
    
    # Run all tests
    test_health_check()
    test_authentication()
    test_patients()
    test_vital_signs()
    test_lab_results()
    test_medications()
    test_ml_predictions()
    test_alerts()
    test_analytics()
    test_streaming()
    
    print("\n" + "=" * 50)
    print("✅ API testing completed!")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔧 Interactive API: http://localhost:8000/redoc")

if __name__ == "__main__":
    main()
