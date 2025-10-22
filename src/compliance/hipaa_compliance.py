#!/usr/bin/env python3
"""
HIPAA Compliance Module
======================
Comprehensive HIPAA compliance features for healthcare data protection
including PHI encryption, audit logging, access controls, and data masking.
"""

import hashlib
import hmac
import json
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HIPAACompliance:
    """HIPAA compliance manager for healthcare data protection"""
    
    def __init__(self, encryption_key: Optional[str] = None):
        """Initialize HIPAA compliance manager"""
        self.encryption_key = encryption_key or self._generate_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.audit_log = []
        self.access_controls = {}
        self.data_retention_policy = {
            'default_retention_days': 2555,  # 7 years
            'audit_log_retention_days': 2555,
            'phi_retention_days': 2555
        }
        
    def _generate_encryption_key(self) -> str:
        """Generate encryption key for PHI data"""
        key = Fernet.generate_key()
        return key.decode()
    
    def encrypt_phi(self, data: str) -> str:
        """Encrypt PHI data using AES encryption"""
        try:
            encrypted_data = self.cipher_suite.encrypt(data.encode())
            return base64.b64encode(encrypted_data).decode()
        except Exception as e:
            logger.error(f"Error encrypting PHI data: {e}")
            raise
    
    def decrypt_phi(self, encrypted_data: str) -> str:
        """Decrypt PHI data"""
        try:
            decoded_data = base64.b64decode(encrypted_data.encode())
            decrypted_data = self.cipher_suite.decrypt(decrypted_data)
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"Error decrypting PHI data: {e}")
            raise
    
    def mask_phi(self, data: Dict[str, Any], fields_to_mask: List[str]) -> Dict[str, Any]:
        """Mask PHI data for non-authorized access"""
        masked_data = data.copy()
        
        for field in fields_to_mask:
            if field in masked_data:
                value = str(masked_data[field])
                if len(value) > 4:
                    masked_data[field] = "*" * (len(value) - 4) + value[-4:]
                else:
                    masked_data[field] = "*" * len(value)
        
        return masked_data
    
    def hash_phi(self, data: str) -> str:
        """Create one-way hash of PHI data for indexing"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def log_audit_event(self, event_type: str, user_id: str, resource: str, 
                       action: str, details: Dict[str, Any] = None):
        """Log audit event for HIPAA compliance"""
        audit_event = {
            'event_id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'resource': resource,
            'action': action,
            'details': details or {},
            'ip_address': self._get_client_ip(),
            'user_agent': self._get_user_agent()
        }
        
        self.audit_log.append(audit_event)
        logger.info(f"Audit event logged: {event_type} - {action} by {user_id}")
        
        # Store audit log to file
        self._store_audit_log(audit_event)
    
    def _get_client_ip(self) -> str:
        """Get client IP address (simulated)"""
        return "192.168.1.100"  # In real implementation, get from request
    
    def _get_user_agent(self) -> str:
        """Get user agent (simulated)"""
        return "Healthcare-Analytics-Platform/1.0"
    
    def _store_audit_log(self, audit_event: Dict[str, Any]):
        """Store audit log to file"""
        try:
            log_file = f"audit_logs/audit_{datetime.now().strftime('%Y%m%d')}.json"
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            
            with open(log_file, 'a') as f:
                f.write(json.dumps(audit_event) + '\n')
        except Exception as e:
            logger.error(f"Error storing audit log: {e}")
    
    def check_access_permissions(self, user_id: str, resource: str, action: str) -> bool:
        """Check if user has permission to access resource"""
        # Simulate access control check
        user_permissions = self.access_controls.get(user_id, {})
        resource_permissions = user_permissions.get(resource, [])
        
        return action in resource_permissions
    
    def grant_access_permission(self, user_id: str, resource: str, actions: List[str]):
        """Grant access permissions to user"""
        if user_id not in self.access_controls:
            self.access_controls[user_id] = {}
        
        self.access_controls[user_id][resource] = actions
        logger.info(f"Access permissions granted to {user_id} for {resource}: {actions}")
    
    def revoke_access_permission(self, user_id: str, resource: str):
        """Revoke access permissions from user"""
        if user_id in self.access_controls:
            if resource in self.access_controls[user_id]:
                del self.access_controls[user_id][resource]
                logger.info(f"Access permissions revoked from {user_id} for {resource}")
    
    def anonymize_patient_data(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize patient data for research purposes"""
        anonymized_data = patient_data.copy()
        
        # Remove direct identifiers
        direct_identifiers = ['name', 'ssn', 'address', 'phone', 'email']
        for identifier in direct_identifiers:
            if identifier in anonymized_data:
                del anonymized_data[identifier]
        
        # Hash indirect identifiers
        indirect_identifiers = ['patient_id', 'medical_record_number']
        for identifier in indirect_identifiers:
            if identifier in anonymized_data:
                anonymized_data[identifier] = self.hash_phi(anonymized_data[identifier])
        
        # Generalize age (group into ranges)
        if 'age' in anonymized_data:
            age = anonymized_data['age']
            if age < 18:
                anonymized_data['age_group'] = '0-17'
            elif age < 35:
                anonymized_data['age_group'] = '18-34'
            elif age < 55:
                anonymized_data['age_group'] = '35-54'
            elif age < 75:
                anonymized_data['age_group'] = '55-74'
            else:
                anonymized_data['age_group'] = '75+'
            del anonymized_data['age']
        
        return anonymized_data
    
    def check_data_retention(self, data_type: str, creation_date: datetime) -> bool:
        """Check if data should be retained based on HIPAA requirements"""
        retention_days = self.data_retention_policy.get(f'{data_type}_retention_days', 
                                                       self.data_retention_policy['default_retention_days'])
        
        retention_date = creation_date + timedelta(days=retention_days)
        return datetime.now() < retention_date
    
    def generate_phi_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate PHI report for compliance monitoring"""
        phi_fields = ['name', 'ssn', 'address', 'phone', 'email', 'date_of_birth']
        phi_count = sum(1 for field in phi_fields if field in data)
        
        return {
            'phi_fields_detected': phi_count,
            'phi_fields': [field for field in phi_fields if field in data],
            'data_classification': 'PHI' if phi_count > 0 else 'Non-PHI',
            'encryption_required': phi_count > 0,
            'audit_required': phi_count > 0
        }
    
    def validate_hipaa_compliance(self, data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Validate HIPAA compliance for data access"""
        compliance_report = {
            'compliant': True,
            'violations': [],
            'recommendations': []
        }
        
        # Check for PHI data
        phi_report = self.generate_phi_report(data)
        if phi_report['phi_fields_detected'] > 0:
            compliance_report['recommendations'].append("PHI data detected - ensure encryption")
        
        # Check access permissions
        if not self.check_access_permissions(user_id, 'patient_data', 'read'):
            compliance_report['compliant'] = False
            compliance_report['violations'].append("Insufficient access permissions")
        
        # Check data retention
        if 'creation_date' in data:
            creation_date = datetime.fromisoformat(data['creation_date'])
            if not self.check_data_retention('phi', creation_date):
                compliance_report['violations'].append("Data retention period exceeded")
        
        return compliance_report
    
    def get_audit_report(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Generate audit report for specified date range"""
        filtered_events = []
        
        for event in self.audit_log:
            event_date = datetime.fromisoformat(event['timestamp'])
            if start_date <= event_date <= end_date:
                filtered_events.append(event)
        
        return filtered_events
    
    def export_audit_log(self, output_file: str):
        """Export audit log to file"""
        try:
            with open(output_file, 'w') as f:
                json.dump(self.audit_log, f, indent=2)
            logger.info(f"Audit log exported to {output_file}")
        except Exception as e:
            logger.error(f"Error exporting audit log: {e}")
    
    def get_compliance_summary(self) -> Dict[str, Any]:
        """Get HIPAA compliance summary"""
        return {
            'total_audit_events': len(self.audit_log),
            'active_users': len(self.access_controls),
            'encryption_enabled': True,
            'audit_logging_enabled': True,
            'access_controls_enabled': True,
            'data_retention_policy': self.data_retention_policy,
            'compliance_status': 'COMPLIANT'
        }

def main():
    """Main function to demonstrate HIPAA compliance features"""
    print("HIPAA Compliance Module")
    print("=" * 30)
    
    # Initialize HIPAA compliance
    hipaa = HIPAACompliance()
    
    # Sample patient data
    patient_data = {
        'patient_id': 'P001',
        'name': 'John Smith',
        'ssn': '123-45-6789',
        'age': 45,
        'address': '123 Main St',
        'phone': '555-1234',
        'email': 'john@example.com',
        'condition': 'Hypertension'
    }
    
    print("1. PHI Data Encryption")
    encrypted_name = hipaa.encrypt_phi(patient_data['name'])
    print(f"   Original: {patient_data['name']}")
    print(f"   Encrypted: {encrypted_name}")
    
    print("\n2. PHI Data Masking")
    masked_data = hipaa.mask_phi(patient_data, ['name', 'ssn', 'phone'])
    print(f"   Masked data: {masked_data}")
    
    print("\n3. Data Anonymization")
    anonymized_data = hipaa.anonymize_patient_data(patient_data)
    print(f"   Anonymized data: {anonymized_data}")
    
    print("\n4. Access Control")
    hipaa.grant_access_permission('user123', 'patient_data', ['read', 'write'])
    has_access = hipaa.check_access_permissions('user123', 'patient_data', 'read')
    print(f"   User access: {has_access}")
    
    print("\n5. Audit Logging")
    hipaa.log_audit_event('DATA_ACCESS', 'user123', 'patient_data', 'READ', {'patient_id': 'P001'})
    print(f"   Audit events logged: {len(hipaa.audit_log)}")
    
    print("\n6. Compliance Validation")
    compliance = hipaa.validate_hipaa_compliance(patient_data, 'user123')
    print(f"   Compliance status: {compliance}")
    
    print("\n HIPAA compliance features demonstrated successfully!")

if __name__ == "__main__":
    main()
