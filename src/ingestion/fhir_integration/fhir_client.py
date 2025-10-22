"""
FHIR Integration Client for Healthcare Patient Analytics Platform
Handles FHIR API connections and data retrieval for healthcare data
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
from dataclasses import dataclass
from fhirclient import client
from fhirclient.models import patient, observation, encounter, medication

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FHIRConfig:
    """FHIR server configuration"""
    base_url: str
    client_id: str
    client_secret: str
    scope: str
    token_url: str
    timeout: int = 30

class FHIRClient:
    """
    FHIR client for healthcare data integration
    Handles authentication, data retrieval, and error handling
    """
    
    def __init__(self, config: FHIRConfig):
        self.config = config
        self.session = requests.Session()
        self.access_token = None
        self.token_expires_at = None
        
    def authenticate(self) -> bool:
        """
        Authenticate with FHIR server using OAuth2
        Returns True if successful, False otherwise
        """
        try:
            auth_data = {
                'grant_type': 'client_credentials',
                'client_id': self.config.client_id,
                'client_secret': self.config.client_secret,
                'scope': self.config.scope
            }
            
            response = self.session.post(
                self.config.token_url,
                data=auth_data,
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                expires_in = token_data.get('expires_in', 3600)
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                
                # Set authorization header
                self.session.headers.update({
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/fhir+json',
                    'Accept': 'application/fhir+json'
                })
                
                logger.info("FHIR authentication successful")
                return True
            else:
                logger.error(f"FHIR authentication failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"FHIR authentication error: {str(e)}")
            return False
    
    def _check_token_validity(self) -> bool:
        """Check if access token is still valid"""
        if not self.access_token or not self.token_expires_at:
            return False
        
        # Refresh token if it expires in the next 5 minutes
        if datetime.now() >= (self.token_expires_at - timedelta(minutes=5)):
            return self.authenticate()
        
        return True
    
    def get_patients(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Retrieve patient data from FHIR server
        Args:
            limit: Maximum number of patients to retrieve
            offset: Number of patients to skip
        Returns:
            List of patient dictionaries
        """
        if not self._check_token_validity():
            logger.error("Invalid or expired token")
            return []
        
        try:
            url = f"{self.config.base_url}/Patient"
            params = {
                '_count': limit,
                '_offset': offset,
                '_sort': 'birthdate'
            }
            
            response = self.session.get(url, params=params, timeout=self.config.timeout)
            
            if response.status_code == 200:
                data = response.json()
                patients = data.get('entry', [])
                
                # Extract patient information
                patient_list = []
                for entry in patients:
                    patient_data = self._extract_patient_data(entry['resource'])
                    patient_list.append(patient_data)
                
                logger.info(f"Retrieved {len(patient_list)} patients")
                return patient_list
            else:
                logger.error(f"Failed to retrieve patients: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error retrieving patients: {str(e)}")
            return []
    
    def get_patient_by_id(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve specific patient by ID
        Args:
            patient_id: FHIR patient ID
        Returns:
            Patient dictionary or None if not found
        """
        if not self._check_token_validity():
            logger.error("Invalid or expired token")
            return None
        
        try:
            url = f"{self.config.base_url}/Patient/{patient_id}"
            response = self.session.get(url, timeout=self.config.timeout)
            
            if response.status_code == 200:
                patient_data = self._extract_patient_data(response.json())
                logger.info(f"Retrieved patient {patient_id}")
                return patient_data
            else:
                logger.error(f"Failed to retrieve patient {patient_id}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving patient {patient_id}: {str(e)}")
            return None
    
    def get_observations(self, patient_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve patient observations (vital signs, lab results)
        Args:
            patient_id: FHIR patient ID
            limit: Maximum number of observations to retrieve
        Returns:
            List of observation dictionaries
        """
        if not self._check_token_validity():
            logger.error("Invalid or expired token")
            return []
        
        try:
            url = f"{self.config.base_url}/Observation"
            params = {
                'patient': patient_id,
                '_count': limit,
                '_sort': '-date'
            }
            
            response = self.session.get(url, params=params, timeout=self.config.timeout)
            
            if response.status_code == 200:
                data = response.json()
                observations = data.get('entry', [])
                
                # Extract observation information
                observation_list = []
                for entry in observations:
                    obs_data = self._extract_observation_data(entry['resource'])
                    observation_list.append(obs_data)
                
                logger.info(f"Retrieved {len(observation_list)} observations for patient {patient_id}")
                return observation_list
            else:
                logger.error(f"Failed to retrieve observations: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error retrieving observations: {str(e)}")
            return []
    
    def get_encounters(self, patient_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve patient encounters (visits, admissions)
        Args:
            patient_id: FHIR patient ID
            limit: Maximum number of encounters to retrieve
        Returns:
            List of encounter dictionaries
        """
        if not self._check_token_validity():
            logger.error("Invalid or expired token")
            return []
        
        try:
            url = f"{self.config.base_url}/Encounter"
            params = {
                'patient': patient_id,
                '_count': limit,
                '_sort': '-date'
            }
            
            response = self.session.get(url, params=params, timeout=self.config.timeout)
            
            if response.status_code == 200:
                data = response.json()
                encounters = data.get('entry', [])
                
                # Extract encounter information
                encounter_list = []
                for entry in encounters:
                    enc_data = self._extract_encounter_data(entry['resource'])
                    encounter_list.append(enc_data)
                
                logger.info(f"Retrieved {len(encounter_list)} encounters for patient {patient_id}")
                return encounter_list
            else:
                logger.error(f"Failed to retrieve encounters: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error retrieving encounters: {str(e)}")
            return []
    
    def _extract_patient_data(self, patient_resource: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant patient data from FHIR patient resource
        Args:
            patient_resource: FHIR patient resource
        Returns:
            Extracted patient data dictionary
        """
        try:
            patient_data = {
                'patient_id': patient_resource.get('id'),
                'name': self._extract_name(patient_resource.get('name', [])),
                'gender': patient_resource.get('gender'),
                'birth_date': patient_resource.get('birthDate'),
                'address': self._extract_address(patient_resource.get('address', [])),
                'telecom': self._extract_telecom(patient_resource.get('telecom', [])),
                'marital_status': self._extract_marital_status(patient_resource.get('maritalStatus')),
                'created': patient_resource.get('meta', {}).get('lastUpdated')
            }
            
            return patient_data
            
        except Exception as e:
            logger.error(f"Error extracting patient data: {str(e)}")
            return {}
    
    def _extract_observation_data(self, observation_resource: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant observation data from FHIR observation resource
        Args:
            observation_resource: FHIR observation resource
        Returns:
            Extracted observation data dictionary
        """
        try:
            observation_data = {
                'observation_id': observation_resource.get('id'),
                'patient_id': self._extract_patient_reference(observation_resource.get('subject', {})),
                'code': self._extract_code(observation_resource.get('code', {})),
                'value': self._extract_value(observation_resource.get('valueQuantity', {})),
                'unit': self._extract_unit(observation_resource.get('valueQuantity', {})),
                'date': observation_resource.get('effectiveDateTime'),
                'status': observation_resource.get('status'),
                'category': self._extract_category(observation_resource.get('category', []))
            }
            
            return observation_data
            
        except Exception as e:
            logger.error(f"Error extracting observation data: {str(e)}")
            return {}
    
    def _extract_encounter_data(self, encounter_resource: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant encounter data from FHIR encounter resource
        Args:
            encounter_resource: FHIR encounter resource
        Returns:
            Extracted encounter data dictionary
        """
        try:
            encounter_data = {
                'encounter_id': encounter_resource.get('id'),
                'patient_id': self._extract_patient_reference(encounter_resource.get('subject', {})),
                'status': encounter_resource.get('status'),
                'class': self._extract_class(encounter_resource.get('class', {})),
                'type': self._extract_type(encounter_resource.get('type', [])),
                'start_date': encounter_resource.get('period', {}).get('start'),
                'end_date': encounter_resource.get('period', {}).get('end'),
                'length': self._calculate_encounter_length(encounter_resource.get('period', {}))
            }
            
            return encounter_data
            
        except Exception as e:
            logger.error(f"Error extracting encounter data: {str(e)}")
            return {}
    
    def _extract_name(self, name_list: List[Dict[str, Any]]) -> str:
        """Extract patient name from FHIR name list"""
        if not name_list:
            return ""
        
        name = name_list[0]
        given = " ".join(name.get('given', []))
        family = name.get('family', '')
        
        return f"{given} {family}".strip()
    
    def _extract_address(self, address_list: List[Dict[str, Any]]) -> Dict[str, str]:
        """Extract patient address from FHIR address list"""
        if not address_list:
            return {}
        
        address = address_list[0]
        return {
            'line': ", ".join(address.get('line', [])),
            'city': address.get('city', ''),
            'state': address.get('state', ''),
            'postal_code': address.get('postalCode', ''),
            'country': address.get('country', '')
        }
    
    def _extract_telecom(self, telecom_list: List[Dict[str, Any]]) -> Dict[str, str]:
        """Extract patient contact information from FHIR telecom list"""
        telecom_data = {}
        
        for telecom in telecom_list:
            system = telecom.get('system', '')
            value = telecom.get('value', '')
            
            if system == 'phone':
                telecom_data['phone'] = value
            elif system == 'email':
                telecom_data['email'] = value
        
        return telecom_data
    
    def _extract_marital_status(self, marital_status: Dict[str, Any]) -> str:
        """Extract marital status from FHIR marital status"""
        if not marital_status:
            return ""
        
        return marital_status.get('text', '')
    
    def _extract_patient_reference(self, subject: Dict[str, Any]) -> str:
        """Extract patient ID from FHIR reference"""
        if not subject:
            return ""
        
        reference = subject.get('reference', '')
        if 'Patient/' in reference:
            return reference.split('Patient/')[-1]
        
        return reference
    
    def _extract_code(self, code: Dict[str, Any]) -> str:
        """Extract observation code from FHIR code"""
        if not code:
            return ""
        
        return code.get('text', '')
    
    def _extract_value(self, value_quantity: Dict[str, Any]) -> float:
        """Extract observation value from FHIR value quantity"""
        if not value_quantity:
            return 0.0
        
        return float(value_quantity.get('value', 0.0))
    
    def _extract_unit(self, value_quantity: Dict[str, Any]) -> str:
        """Extract observation unit from FHIR value quantity"""
        if not value_quantity:
            return ""
        
        return value_quantity.get('unit', '')
    
    def _extract_category(self, category_list: List[Dict[str, Any]]) -> str:
        """Extract observation category from FHIR category list"""
        if not category_list:
            return ""
        
        category = category_list[0]
        return category.get('text', '')
    
    def _extract_class(self, class_info: Dict[str, Any]) -> str:
        """Extract encounter class from FHIR class"""
        if not class_info:
            return ""
        
        return class_info.get('code', '')
    
    def _extract_type(self, type_list: List[Dict[str, Any]]) -> str:
        """Extract encounter type from FHIR type list"""
        if not type_list:
            return ""
        
        encounter_type = type_list[0]
        return encounter_type.get('text', '')
    
    def _calculate_encounter_length(self, period: Dict[str, Any]) -> int:
        """Calculate encounter length in hours"""
        if not period or not period.get('start') or not period.get('end'):
            return 0
        
        try:
            start_date = datetime.fromisoformat(period['start'].replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(period['end'].replace('Z', '+00:00'))
            duration = end_date - start_date
            return int(duration.total_seconds() / 3600)
        except Exception:
            return 0
    
    def close(self):
        """Close the FHIR client session"""
        if self.session:
            self.session.close()
            logger.info("FHIR client session closed")

# Example usage and testing
if __name__ == "__main__":
    # Example configuration
    config = FHIRConfig(
        base_url="https://hapi.fhir.org/baseR4",
        client_id="your_client_id",
        client_secret="your_client_secret",
        scope="fhir",
        token_url="https://hapi.fhir.org/baseR4/oauth/token"
    )
    
    # Create FHIR client
    fhir_client = FHIRClient(config)
    
    # Authenticate
    if fhir_client.authenticate():
        print("FHIR authentication successful")
        
        # Retrieve patients
        patients = fhir_client.get_patients(limit=10)
        print(f"Retrieved {len(patients)} patients")
        
        # Close client
        fhir_client.close()
    else:
        print("FHIR authentication failed")
