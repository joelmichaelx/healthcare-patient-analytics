# Healthcare Patient Analytics API Documentation

## 📋 Overview

The Healthcare Patient Analytics API provides comprehensive REST endpoints for managing patient data, vital signs, lab results, medications, machine learning predictions, and system analytics. The API is built with FastAPI and provides real-time access to healthcare data with HIPAA compliance.

## 🔗 Base Information

- **Base URL**: `http://localhost:8000`
- **API Version**: `v1`
- **Authentication**: Bearer Token
- **Content Type**: `application/json`
- **Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

## 🔐 Authentication

All API endpoints require Bearer token authentication:

```http
Authorization: Bearer your-api-token
```

### Getting an API Token

Set the `HEALTHCARE_API_TOKEN` environment variable:
```bash
export HEALTHCARE_API_TOKEN="your-secure-api-token"
```

## 📊 API Endpoints

### Health Check

#### GET /health
Check API health status.

**Response:**
```json
{
  "status": "ok",
  "message": "Healthcare Analytics API is running"
}
```

---

### Patients

#### GET /api/v1/patients
Retrieve a list of all patients with pagination.

**Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "patient_id": "P001",
    "name": "John Doe",
    "age": 55,
    "gender": "Male",
    "condition": "Hypertension",
    "risk_level": "Medium",
    "admission_date": "2023-01-15T10:00:00",
    "room": "201-A",
    "status": "Active",
    "created_at": "2023-01-15T10:00:00",
    "updated_at": "2023-01-15T10:00:00"
  }
]
```

#### GET /api/v1/patients/{patient_id}
Retrieve details for a specific patient by their ID.

**Parameters:**
- `patient_id` (string): Patient ID (e.g., "P001")

**Response:**
```json
{
  "patient_id": "P001",
  "name": "John Doe",
  "age": 55,
  "gender": "Male",
  "condition": "Hypertension",
  "risk_level": "Medium",
  "admission_date": "2023-01-15T10:00:00",
  "room": "201-A",
  "status": "Active",
  "created_at": "2023-01-15T10:00:00",
  "updated_at": "2023-01-15T10:00:00"
}
```

#### POST /api/v1/patients
Create a new patient record.

**Request Body:**
```json
{
  "name": "John Doe",
  "age": 55,
  "gender": "Male",
  "condition": "Hypertension",
  "risk_level": "Medium",
  "admission_date": "2023-01-15T10:00:00",
  "room": "201-A",
  "status": "Active"
}
```

**Response:**
```json
{
  "patient_id": "P001",
  "name": "John Doe",
  "age": 55,
  "gender": "Male",
  "condition": "Hypertension",
  "risk_level": "Medium",
  "admission_date": "2023-01-15T10:00:00",
  "room": "201-A",
  "status": "Active",
  "created_at": "2023-01-15T10:00:00",
  "updated_at": "2023-01-15T10:00:00"
}
```

---

### Vital Signs

#### GET /api/v1/patients/{patient_id}/vital-signs
Retrieve vital signs records for a specific patient.

**Parameters:**
- `patient_id` (string): Patient ID
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "patient_id": "P001",
    "heart_rate": 75,
    "blood_pressure_systolic": 120,
    "blood_pressure_diastolic": 80,
    "temperature": 98.6,
    "oxygen_saturation": 98,
    "respiratory_rate": 16,
    "timestamp": "2023-10-26T14:30:00"
  }
]
```

#### POST /api/v1/patients/{patient_id}/vital-signs
Record new vital signs for a specific patient.

**Request Body:**
```json
{
  "heart_rate": 75,
  "blood_pressure_systolic": 120,
  "blood_pressure_diastolic": 80,
  "temperature": 98.6,
  "oxygen_saturation": 98,
  "respiratory_rate": 16,
  "timestamp": "2023-10-26T14:30:00"
}
```

**Response:**
```json
{
  "id": 1,
  "patient_id": "P001",
  "heart_rate": 75,
  "blood_pressure_systolic": 120,
  "blood_pressure_diastolic": 80,
  "temperature": 98.6,
  "oxygen_saturation": 98,
  "respiratory_rate": 16,
  "timestamp": "2023-10-26T14:30:00"
}
```

---

### Lab Results

#### GET /api/v1/patients/{patient_id}/lab-results
Retrieve lab results records for a specific patient.

**Parameters:**
- `patient_id` (string): Patient ID
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "patient_id": "P001",
    "test_name": "Glucose",
    "test_value": 120.5,
    "test_unit": "mg/dL",
    "reference_range": "70-100",
    "critical_flag": true,
    "timestamp": "2023-10-26T10:00:00"
  }
]
```

#### POST /api/v1/patients/{patient_id}/lab-results
Record new lab results for a specific patient.

**Request Body:**
```json
{
  "test_name": "Glucose",
  "test_value": 120.5,
  "test_unit": "mg/dL",
  "reference_range": "70-100",
  "critical_flag": true,
  "timestamp": "2023-10-26T10:00:00"
}
```

**Response:**
```json
{
  "id": 1,
  "patient_id": "P001",
  "test_name": "Glucose",
  "test_value": 120.5,
  "test_unit": "mg/dL",
  "reference_range": "70-100",
  "critical_flag": true,
  "timestamp": "2023-10-26T10:00:00"
}
```

---

### Medications

#### GET /api/v1/patients/{patient_id}/medications
Retrieve medication records for a specific patient.

**Parameters:**
- `patient_id` (string): Patient ID
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "patient_id": "P001",
    "medication_name": "Lisinopril",
    "dosage": 10.0,
    "unit": "mg",
    "route": "Oral",
    "administered_by": "Nurse Jane",
    "timestamp": "2023-10-26T08:00:00",
    "status": "Administered",
    "created_at": "2023-10-26T08:00:00"
  }
]
```

#### POST /api/v1/patients/{patient_id}/medications
Record new medication administration for a specific patient.

**Request Body:**
```json
{
  "medication_name": "Lisinopril",
  "dosage": 10.0,
  "unit": "mg",
  "route": "Oral",
  "administered_by": "Nurse Jane",
  "timestamp": "2023-10-26T08:00:00",
  "status": "Administered"
}
```

**Response:**
```json
{
  "id": 1,
  "patient_id": "P001",
  "medication_name": "Lisinopril",
  "dosage": 10.0,
  "unit": "mg",
  "route": "Oral",
  "administered_by": "Nurse Jane",
  "timestamp": "2023-10-26T08:00:00",
  "status": "Administered",
  "created_at": "2023-10-26T08:00:00"
}
```

---

### Machine Learning Predictions

#### GET /api/v1/patients/{patient_id}/predictions
Retrieve machine learning predictions for a specific patient.

**Parameters:**
- `patient_id` (string): Patient ID

**Response:**
```json
{
  "readmission_risk": 0.15,
  "sepsis_detection": 0.05,
  "medication_adherence": 0.92,
  "timestamp": "2023-10-26T15:00:00"
}
```

**Prediction Models:**
- **Readmission Risk**: Probability of readmission (0-1)
- **Sepsis Detection**: Probability of sepsis (0-1)
- **Medication Adherence**: Probability of medication adherence (0-1)

---

### Analytics

#### GET /api/v1/analytics/patient-summary
Retrieve patient summary analytics.

**Response:**
```json
{
  "total_patients": 1000,
  "active_patients": 850,
  "critical_patients": 25,
  "average_age": 65.5,
  "most_common_condition": "Hypertension"
}
```

#### GET /api/v1/analytics/vital-signs-trends
Retrieve vital signs trends over a specified period.

**Parameters:**
- `patient_id` (string, optional): Patient ID (if not provided, returns aggregate trends)
- `days` (int, optional): Number of days to analyze (default: 7)

**Response:**
```json
[
  {
    "timestamp": "2023-10-26T00:00:00",
    "heart_rate_avg": 75.2,
    "blood_pressure_systolic_avg": 120.5,
    "blood_pressure_diastolic_avg": 80.3,
    "temperature_avg": 98.6,
    "oxygen_saturation_avg": 97.8,
    "respiratory_rate_avg": 16.1
  }
]
```

---

### Alerts

#### GET /api/v1/alerts
Retrieve a list of all active alerts.

**Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "patient_id": "P001",
    "alert_type": "Critical Vital Sign",
    "message": "Patient P001 has critically high heart rate.",
    "timestamp": "2023-10-26T15:05:00",
    "severity": "High",
    "resolved": false
  }
]
```

---

### Streaming

#### GET /api/v1/streaming/status
Retrieve the current status of the real-time data streaming system.

**Response:**
```json
{
  "kafka_connected": true,
  "producer_active": true,
  "consumer_active": true,
  "last_message_time": "2023-10-26T15:00:00"
}
```

#### GET /api/v1/streaming/live-data
Retrieve a sample of live streaming data.

**Response:**
```json
[
  {
    "patient_id": "P001",
    "data_type": "heart_rate",
    "value": 72,
    "timestamp": "2023-10-26T15:00:00"
  },
  {
    "patient_id": "P002",
    "data_type": "temperature",
    "value": 98.1,
    "timestamp": "2023-10-26T15:00:00"
  }
]
```

---

## 📝 Data Models

### Patient Model
```json
{
  "patient_id": "string",
  "name": "string",
  "age": "integer",
  "gender": "string",
  "condition": "string",
  "risk_level": "string",
  "admission_date": "datetime",
  "room": "string",
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Vital Signs Model
```json
{
  "id": "integer",
  "patient_id": "string",
  "heart_rate": "integer",
  "blood_pressure_systolic": "integer",
  "blood_pressure_diastolic": "integer",
  "temperature": "float",
  "oxygen_saturation": "integer",
  "respiratory_rate": "integer",
  "timestamp": "datetime"
}
```

### Lab Results Model
```json
{
  "id": "integer",
  "patient_id": "string",
  "test_name": "string",
  "test_value": "float",
  "test_unit": "string",
  "reference_range": "string",
  "critical_flag": "boolean",
  "timestamp": "datetime"
}
```

### Medication Model
```json
{
  "id": "integer",
  "patient_id": "string",
  "medication_name": "string",
  "dosage": "float",
  "unit": "string",
  "route": "string",
  "administered_by": "string",
  "timestamp": "datetime",
  "status": "string",
  "created_at": "datetime"
}
```

### Alert Model
```json
{
  "id": "integer",
  "patient_id": "string",
  "alert_type": "string",
  "message": "string",
  "timestamp": "datetime",
  "severity": "string",
  "resolved": "boolean"
}
```

---

## 🚨 Error Responses

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Invalid authentication |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |
| 503 | Service Unavailable - Service temporarily unavailable |

### Error Response Format
```json
{
  "detail": "Error message description"
}
```

### Common Error Examples

#### 400 Bad Request
```json
{
  "detail": "Invalid request data. Please check your input parameters."
}
```

#### 401 Unauthorized
```json
{
  "detail": "Invalid authentication credentials"
}
```

#### 404 Not Found
```json
{
  "detail": "Patient not found"
}
```

#### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error. Please try again later."
}
```

---

## 🔧 Rate Limiting

### Rate Limits
- **Default**: 100 requests per minute per IP
- **Authenticated**: 1000 requests per minute per token
- **Burst**: 10 requests per second

### Rate Limit Headers
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

### Rate Limit Exceeded
```json
{
  "detail": "Rate limit exceeded. Please try again later."
}
```

---

## 📊 Pagination

### Pagination Parameters
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100, max: 1000)

### Pagination Response
```json
{
  "data": [...],
  "pagination": {
    "skip": 0,
    "limit": 100,
    "total": 1000,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## 🔍 Filtering and Sorting

### Filtering
Most endpoints support filtering by common fields:

```http
GET /api/v1/patients?status=Active&risk_level=Critical
GET /api/v1/patients/{patient_id}/vital-signs?start_date=2023-10-01&end_date=2023-10-31
```

### Sorting
Sort by any field with `sort` parameter:

```http
GET /api/v1/patients?sort=name
GET /api/v1/patients?sort=-admission_date  # Descending order
```

---

## 📱 SDK Examples

### Python SDK Example
```python
import requests

# Set up API client
API_BASE = "http://localhost:8000"
API_TOKEN = "your-api-token"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# Get all patients
response = requests.get(f"{API_BASE}/api/v1/patients", headers=HEADERS)
patients = response.json()

# Create a new patient
patient_data = {
    "name": "John Doe",
    "age": 55,
    "gender": "Male",
    "condition": "Hypertension",
    "risk_level": "Medium",
    "admission_date": "2023-01-15T10:00:00",
    "room": "201-A",
    "status": "Active"
}
response = requests.post(f"{API_BASE}/api/v1/patients", json=patient_data, headers=HEADERS)
new_patient = response.json()

# Get ML predictions
response = requests.get(f"{API_BASE}/api/v1/patients/P001/predictions", headers=HEADERS)
predictions = response.json()
```

### JavaScript SDK Example
```javascript
const API_BASE = 'http://localhost:8000';
const API_TOKEN = 'your-api-token';

// Set up fetch with authentication
const apiCall = async (endpoint, options = {}) => {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${API_TOKEN}`,
      'Content-Type': 'application/json',
      ...options.headers
    }
  });
  return response.json();
};

// Get all patients
const patients = await apiCall('/api/v1/patients');

// Create a new patient
const newPatient = await apiCall('/api/v1/patients', {
  method: 'POST',
  body: JSON.stringify({
    name: 'John Doe',
    age: 55,
    gender: 'Male',
    condition: 'Hypertension',
    risk_level: 'Medium',
    admission_date: '2023-01-15T10:00:00',
    room: '201-A',
    status: 'Active'
  })
});

// Get ML predictions
const predictions = await apiCall('/api/v1/patients/P001/predictions');
```

### cURL Examples
```bash
# Get all patients
curl -X GET "http://localhost:8000/api/v1/patients" \
  -H "Authorization: Bearer your-api-token"

# Create a new patient
curl -X POST "http://localhost:8000/api/v1/patients" \
  -H "Authorization: Bearer your-api-token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 55,
    "gender": "Male",
    "condition": "Hypertension",
    "risk_level": "Medium",
    "admission_date": "2023-01-15T10:00:00",
    "room": "201-A",
    "status": "Active"
  }'

# Get ML predictions
curl -X GET "http://localhost:8000/api/v1/patients/P001/predictions" \
  -H "Authorization: Bearer your-api-token"
```

---

## 🔒 Security

### Authentication
- **Bearer Token**: JWT-based authentication
- **API Keys**: API key authentication
- **Rate Limiting**: Request rate limiting
- **CORS**: Cross-origin resource sharing

### Data Protection
- **HTTPS**: Encrypted data transmission
- **Input Validation**: Request data validation
- **SQL Injection Protection**: Parameterized queries
- **XSS Protection**: Cross-site scripting protection

### HIPAA Compliance
- **Data Encryption**: Data encryption at rest and in transit
- **Access Controls**: Role-based access control
- **Audit Logging**: Comprehensive audit trail
- **Data Anonymization**: Patient data anonymization

---

## 📈 Performance

### Response Times
- **Average Response Time**: < 200ms
- **95th Percentile**: < 500ms
- **99th Percentile**: < 1000ms

### Throughput
- **Requests per Second**: 1000+ RPS
- **Concurrent Users**: 500+ concurrent users
- **Data Processing**: Real-time data processing

### Optimization
- **Caching**: Response caching
- **Database Optimization**: Query optimization
- **Connection Pooling**: Database connection pooling
- **Load Balancing**: Application load balancing

---

## 🧪 Testing

### Test Environment
- **Base URL**: `http://localhost:8000`
- **Test Data**: Pre-populated test data
- **Mock Services**: Mock external services

### Test Coverage
- **Unit Tests**: 90%+ code coverage
- **Integration Tests**: API endpoint testing
- **Performance Tests**: Load testing
- **Security Tests**: Security vulnerability testing

---

## 📞 Support

### Documentation
- **API Documentation**: https://api.healthcare-analytics.com/docs
- **Interactive Docs**: https://api.healthcare-analytics.com/redoc
- **Postman Collection**: Available in repository

### Contact
- **GitHub Issues**: https://github.com/joelmichaelx/healthcare-patient-analytics/issues
- **Email**: support@healthcare-analytics.com
- **Documentation**: https://docs.healthcare-analytics.com

---

**This API documentation provides comprehensive information about the Healthcare Patient Analytics API. For additional support or questions, please refer to the contact information above.**