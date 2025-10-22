"""
Healthcare Data Validator
Validates healthcare data for accuracy, completeness, and compliance
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
from dataclasses import dataclass
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Data validation result"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    score: float  # 0-100 validation score

class HealthcareDataValidator:
    """
    Validates healthcare data for clinical accuracy and compliance
    Implements medical data quality rules and HIPAA compliance checks
    """
    
    def __init__(self):
        self.validation_rules = self._initialize_validation_rules()
        self.compliance_rules = self._initialize_compliance_rules()
    
    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """Initialize medical data validation rules"""
        return {
            "patient_id": {
                "required": True,
                "format": r"^P\d{3}$",
                "description": "Patient ID must be in format P###"
            },
            "age": {
                "min": 0,
                "max": 120,
                "required": True,
                "description": "Age must be between 0 and 120"
            },
            "gender": {
                "allowed_values": ["Male", "Female", "Other", "Unknown"],
                "required": True,
                "description": "Gender must be one of the allowed values"
            },
            "heart_rate": {
                "min": 30,
                "max": 220,
                "critical_low": 40,
                "critical_high": 150,
                "description": "Heart rate in BPM"
            },
            "blood_pressure_systolic": {
                "min": 70,
                "max": 250,
                "critical_low": 70,
                "critical_high": 200,
                "description": "Systolic blood pressure in mmHg"
            },
            "blood_pressure_diastolic": {
                "min": 40,
                "max": 150,
                "critical_low": 40,
                "critical_high": 120,
                "description": "Diastolic blood pressure in mmHg"
            },
            "temperature": {
                "min": 95.0,
                "max": 110.0,
                "critical_low": 97.0,
                "critical_high": 104.0,
                "description": "Temperature in Fahrenheit"
            },
            "oxygen_saturation": {
                "min": 70,
                "max": 100,
                "critical_low": 90,
                "description": "Oxygen saturation percentage"
            },
            "respiratory_rate": {
                "min": 8,
                "max": 40,
                "critical_low": 12,
                "critical_high": 25,
                "description": "Respiratory rate per minute"
            }
        }
    
    def _initialize_compliance_rules(self) -> Dict[str, Any]:
        """Initialize HIPAA compliance rules"""
        return {
            "phi_fields": [
                "patient_id", "name", "date_of_birth", "address", 
                "phone", "email", "ssn", "medical_record_number"
            ],
            "required_audit_fields": [
                "timestamp", "user_id", "action", "ip_address"
            ],
            "data_retention_years": {
                "patient_records": 7,
                "vital_signs": 3,
                "lab_results": 5,
                "imaging": 7
            },
            "encryption_required": True,
            "access_logging_required": True
        }
    
    def validate_patient_data(self, patient_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate patient demographic data
        Args:
            patient_data: Patient information dictionary
        Returns:
            ValidationResult with validation status and issues
        """
        errors = []
        warnings = []
        
        try:
            # Validate required fields
            required_fields = ["patient_id", "name", "age", "gender"]
            for field in required_fields:
                if field not in patient_data or patient_data[field] is None:
                    errors.append(f"Missing required field: {field}")
            
            # Validate patient ID format
            if "patient_id" in patient_data:
                if not re.match(self.validation_rules["patient_id"]["format"], patient_data["patient_id"]):
                    errors.append(f"Invalid patient ID format: {patient_data['patient_id']}")
            
            # Validate age
            if "age" in patient_data:
                age = patient_data["age"]
                if not isinstance(age, (int, float)) or age < 0 or age > 120:
                    errors.append(f"Invalid age: {age}")
                elif age < 18:
                    warnings.append("Patient is under 18 - verify consent")
            
            # Validate gender
            if "gender" in patient_data:
                gender = patient_data["gender"]
                if gender not in self.validation_rules["gender"]["allowed_values"]:
                    errors.append(f"Invalid gender: {gender}")
            
            # Validate date of birth if provided
            if "date_of_birth" in patient_data:
                dob = patient_data["date_of_birth"]
                if isinstance(dob, str):
                    try:
                        dob_date = datetime.strptime(dob, "%Y-%m-%d")
                        if dob_date > datetime.now():
                            errors.append("Date of birth cannot be in the future")
                        elif dob_date < datetime.now() - timedelta(days=120*365):
                            warnings.append("Patient age over 120 years - verify data")
                    except ValueError:
                        errors.append(f"Invalid date format: {dob}")
            
            # Check for PHI compliance
            phi_violations = self._check_phi_compliance(patient_data)
            if phi_violations:
                errors.extend(phi_violations)
            
            # Calculate validation score
            total_checks = len(required_fields) + 3  # Additional checks
            error_count = len(errors)
            score = max(0, ((total_checks - error_count) / total_checks) * 100)
            
            return ValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                score=score
            )
            
        except Exception as e:
            logger.error(f"Error validating patient data: {str(e)}")
            return ValidationResult(
                is_valid=False,
                errors=[f"Validation error: {str(e)}"],
                warnings=[],
                score=0
            )
    
    def validate_vital_signs(self, vital_signs: Dict[str, Any]) -> ValidationResult:
        """
        Validate vital signs data for clinical accuracy
        Args:
            vital_signs: Vital signs data dictionary
        Returns:
            ValidationResult with validation status and issues
        """
        errors = []
        warnings = []
        
        try:
            # Validate each vital sign
            vital_fields = [
                "heart_rate", "blood_pressure_systolic", "blood_pressure_diastolic",
                "temperature", "oxygen_saturation", "respiratory_rate"
            ]
            
            for field in vital_fields:
                if field in vital_signs:
                    value = vital_signs[field]
                    rule = self.validation_rules.get(field)
                    
                    if rule and value is not None:
                        # Check range
                        if "min" in rule and value < rule["min"]:
                            errors.append(f"{field} too low: {value} (min: {rule['min']})")
                        elif "max" in rule and value > rule["max"]:
                            errors.append(f"{field} too high: {value} (max: {rule['max']})")
                        
                        # Check critical values
                        if "critical_low" in rule and value < rule["critical_low"]:
                            warnings.append(f"CRITICAL: {field} critically low: {value}")
                        elif "critical_high" in rule and value > rule["critical_high"]:
                            warnings.append(f"CRITICAL: {field} critically high: {value}")
            
            # Validate blood pressure relationship
            if "blood_pressure_systolic" in vital_signs and "blood_pressure_diastolic" in vital_signs:
                systolic = vital_signs["blood_pressure_systolic"]
                diastolic = vital_signs["blood_pressure_diastolic"]
                
                if systolic <= diastolic:
                    errors.append("Systolic pressure must be higher than diastolic")
                elif systolic - diastolic < 20:
                    warnings.append("Narrow pulse pressure - may indicate cardiac issues")
            
            # Validate timestamp
            if "timestamp" in vital_signs:
                timestamp = vital_signs["timestamp"]
                if isinstance(timestamp, str):
                    try:
                        timestamp_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        if timestamp_date > datetime.now():
                            errors.append("Vital signs timestamp cannot be in the future")
                        elif timestamp_date < datetime.now() - timedelta(days=7):
                            warnings.append("Vital signs data is over 7 days old")
                    except ValueError:
                        errors.append(f"Invalid timestamp format: {timestamp}")
            
            # Calculate validation score
            total_checks = len(vital_fields) + 2  # Additional checks
            error_count = len(errors)
            score = max(0, ((total_checks - error_count) / total_checks) * 100)
            
            return ValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                score=score
            )
            
        except Exception as e:
            logger.error(f"Error validating vital signs: {str(e)}")
            return ValidationResult(
                is_valid=False,
                errors=[f"Validation error: {str(e)}"],
                warnings=[],
                score=0
            )
    
    def validate_lab_results(self, lab_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate laboratory results for clinical accuracy
        Args:
            lab_data: Laboratory results data dictionary
        Returns:
            ValidationResult with validation status and issues
        """
        errors = []
        warnings = []
        
        try:
            # Validate required fields
            required_fields = ["patient_id", "test_name", "test_value", "test_unit", "timestamp"]
            for field in required_fields:
                if field not in lab_data or lab_data[field] is None:
                    errors.append(f"Missing required field: {field}")
            
            # Validate test value
            if "test_value" in lab_data:
                value = lab_data["test_value"]
                if not isinstance(value, (int, float)):
                    errors.append(f"Test value must be numeric: {value}")
                elif value < 0:
                    warnings.append(f"Negative test value: {value}")
            
            # Validate test name
            if "test_name" in lab_data:
                test_name = lab_data["test_name"]
                valid_tests = [
                    "Glucose", "Hemoglobin", "White Blood Cells", "Creatinine",
                    "Sodium", "Potassium", "Cholesterol", "Triglycerides"
                ]
                if test_name not in valid_tests:
                    warnings.append(f"Unknown test name: {test_name}")
            
            # Validate critical flag
            if "critical_flag" in lab_data:
                if lab_data["critical_flag"] and "test_value" in lab_data:
                    warnings.append(f"CRITICAL LAB VALUE: {lab_data['test_name']} = {lab_data['test_value']}")
            
            # Validate timestamp
            if "timestamp" in lab_data:
                timestamp = lab_data["timestamp"]
                if isinstance(timestamp, str):
                    try:
                        timestamp_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        if timestamp_date > datetime.now():
                            errors.append("Lab results timestamp cannot be in the future")
                        elif timestamp_date < datetime.now() - timedelta(days=30):
                            warnings.append("Lab results data is over 30 days old")
                    except ValueError:
                        errors.append(f"Invalid timestamp format: {timestamp}")
            
            # Calculate validation score
            total_checks = len(required_fields) + 2  # Additional checks
            error_count = len(errors)
            score = max(0, ((total_checks - error_count) / total_checks) * 100)
            
            return ValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                score=score
            )
            
        except Exception as e:
            logger.error(f"Error validating lab results: {str(e)}")
            return ValidationResult(
                is_valid=False,
                errors=[f"Validation error: {str(e)}"],
                warnings=score=0
            )
    
    def validate_medication_data(self, medication_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate medication administration data
        Args:
            medication_data: Medication data dictionary
        Returns:
            ValidationResult with validation status and issues
        """
        errors = []
        warnings = []
        
        try:
            # Validate required fields
            required_fields = ["patient_id", "medication_name", "dosage", "unit", "route", "timestamp"]
            for field in required_fields:
                if field not in medication_data or medication_data[field] is None:
                    errors.append(f"Missing required field: {field}")
            
            # Validate dosage
            if "dosage" in medication_data:
                dosage = medication_data["dosage"]
                if not isinstance(dosage, (int, float)) or dosage <= 0:
                    errors.append(f"Invalid dosage: {dosage}")
                elif dosage > 1000:
                    warnings.append(f"High dosage: {dosage} - verify prescription")
            
            # Validate route
            if "route" in medication_data:
                route = medication_data["route"]
                valid_routes = ["Oral", "IV", "IM", "Subcutaneous", "Inhalation", "Topical"]
                if route not in valid_routes:
                    warnings.append(f"Uncommon administration route: {route}")
            
            # Validate medication name
            if "medication_name" in medication_data:
                med_name = medication_data["medication_name"]
                if len(med_name) < 2:
                    errors.append(f"Medication name too short: {med_name}")
            
            # Validate timestamp
            if "timestamp" in medication_data:
                timestamp = medication_data["timestamp"]
                if isinstance(timestamp, str):
                    try:
                        timestamp_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        if timestamp_date > datetime.now():
                            errors.append("Medication timestamp cannot be in the future")
                        elif timestamp_date < datetime.now() - timedelta(days=7):
                            warnings.append("Medication data is over 7 days old")
                    except ValueError:
                        errors.append(f"Invalid timestamp format: {timestamp}")
            
            # Calculate validation score
            total_checks = len(required_fields) + 2  # Additional checks
            error_count = len(errors)
            score = max(0, ((total_checks - error_count) / total_checks) * 100)
            
            return ValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                score=score
            )
            
        except Exception as e:
            logger.error(f"Error validating medication data: {str(e)}")
            return ValidationResult(
                is_valid=False,
                errors=[f"Validation error: {str(e)}"],
                warnings=[],
                score=0
            )
    
    def _check_phi_compliance(self, data: Dict[str, Any]) -> List[str]:
        """
        Check PHI compliance for data
        Args:
            data: Data dictionary to check
        Returns:
            List of PHI compliance violations
        """
        violations = []
        
        # Check for PHI fields
        phi_fields = self.compliance_rules["phi_fields"]
        for field in phi_fields:
            if field in data and data[field] is not None:
                # Check if PHI is properly masked in non-production
                if not self._is_phi_masked(data[field]):
                    violations.append(f"PHI field {field} not properly masked")
        
        return violations
    
    def _is_phi_masked(self, value: Any) -> bool:
        """
        Check if PHI value is properly masked
        Args:
            value: Value to check
        Returns:
            True if properly masked, False otherwise
        """
        if isinstance(value, str):
            # Check if value contains asterisks or is hashed
            return "*" in value or len(value) < 4 or value.startswith("HASH_")
        return False
    
    def validate_batch_data(self, data_list: List[Dict[str, Any]], data_type: str) -> Dict[str, Any]:
        """
        Validate a batch of healthcare data
        Args:
            data_list: List of data dictionaries
            data_type: Type of data (patient, vital_signs, lab_results, medications)
        Returns:
            Batch validation results
        """
        results = {
            "total_records": len(data_list),
            "valid_records": 0,
            "invalid_records": 0,
            "total_errors": 0,
            "total_warnings": 0,
            "average_score": 0,
            "validation_details": []
        }
        
        scores = []
        
        for i, data in enumerate(data_list):
            if data_type == "patient":
                validation_result = self.validate_patient_data(data)
            elif data_type == "vital_signs":
                validation_result = self.validate_vital_signs(data)
            elif data_type == "lab_results":
                validation_result = self.validate_lab_results(data)
            elif data_type == "medications":
                validation_result = self.validate_medication_data(data)
            else:
                continue
            
            if validation_result.is_valid:
                results["valid_records"] += 1
            else:
                results["invalid_records"] += 1
            
            results["total_errors"] += len(validation_result.errors)
            results["total_warnings"] += len(validation_result.warnings)
            scores.append(validation_result.score)
            
            results["validation_details"].append({
                "record_index": i,
                "is_valid": validation_result.is_valid,
                "score": validation_result.score,
                "errors": validation_result.errors,
                "warnings": validation_result.warnings
            })
        
        if scores:
            results["average_score"] = sum(scores) / len(scores)
        
        return results

# Example usage and testing
if __name__ == "__main__":
    # Create validator
    validator = HealthcareDataValidator()
    
    # Test patient data validation
    patient_data = {
        "patient_id": "P001",
        "name": "John Smith",
        "age": 65,
        "gender": "Male",
        "date_of_birth": "1959-01-15"
    }
    
    result = validator.validate_patient_data(patient_data)
    print(f"Patient validation result: {result}")
    
    # Test vital signs validation
    vital_signs = {
        "patient_id": "P001",
        "heart_rate": 75,
        "blood_pressure_systolic": 140,
        "blood_pressure_diastolic": 90,
        "temperature": 98.6,
        "oxygen_saturation": 98,
        "respiratory_rate": 16,
        "timestamp": datetime.now().isoformat()
    }
    
    result = validator.validate_vital_signs(vital_signs)
    print(f"Vital signs validation result: {result}")
    
    # Test lab results validation
    lab_data = {
        "patient_id": "P001",
        "test_name": "Glucose",
        "test_value": 95.5,
        "test_unit": "mg/dL",
        "reference_range": "70-100",
        "critical_flag": False,
        "timestamp": datetime.now().isoformat()
    }
    
    result = validator.validate_lab_results(lab_data)
    print(f"Lab results validation result: {result}")
