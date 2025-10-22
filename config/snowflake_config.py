"""
Healthcare Patient Analytics Platform - Snowflake Configuration
Configuration and connection management for Snowflake data warehouse
"""

import os
from typing import Dict, Optional
from dataclasses import dataclass
import json

@dataclass
class SnowflakeConfig:
    """Snowflake configuration class"""
    account: str
    user: str
    password: str
    warehouse: str
    database: str
    schema: str
    role: Optional[str] = None
    region: Optional[str] = None
    
    def to_dict(self) -> Dict[str, str]:
        """Convert config to dictionary"""
        return {
            'account': self.account,
            'user': self.user,
            'password': self.password,
            'warehouse': self.warehouse,
            'database': self.database,
            'schema': self.schema,
            'role': self.role or 'ACCOUNTADMIN',
            'region': self.region or 'us-east-1'
        }

class SnowflakeConfigManager:
    """Manages Snowflake configuration and connections"""
    
    def __init__(self, config_file: str = "config/snowflake_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> SnowflakeConfig:
        """Load Snowflake configuration from file or environment"""
        
        # Try to load from file first
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                return SnowflakeConfig(**config_data)
            except Exception as e:
                print(f"Warning: Could not load config from {self.config_file}: {e}")
        
        # Fallback to environment variables
        return SnowflakeConfig(
            account=os.getenv('SNOWFLAKE_ACCOUNT', 'your_account.region'),
            user=os.getenv('SNOWFLAKE_USER', 'your_username'),
            password=os.getenv('SNOWFLAKE_PASSWORD', 'your_password'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE', 'HEALTHCARE_WH'),
            database=os.getenv('SNOWFLAKE_DATABASE', 'HEALTHCARE_DB'),
            schema=os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC'),
            role=os.getenv('SNOWFLAKE_ROLE', 'ACCOUNTADMIN'),
            region=os.getenv('SNOWFLAKE_REGION', 'us-east-1')
        )
    
    def get_connection_string(self) -> str:
        """Get Snowflake connection string"""
        config = self.config.to_dict()
        return (
            f"snowflake://{config['user']}:{config['password']}@"
            f"{config['account']}/{config['database']}/{config['schema']}"
            f"?warehouse={config['warehouse']}&role={config['role']}"
        )
    
    def save_config(self, config: SnowflakeConfig):
        """Save configuration to file"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config.to_dict(), f, indent=2)
        print(f"Configuration saved to {self.config_file}")
    
    def create_sample_config(self):
        """Create a sample configuration file"""
        sample_config = SnowflakeConfig(
            account="your_account.region",
            user="your_username",
            password="your_password",
            warehouse="HEALTHCARE_WH",
            database="HEALTHCARE_DB",
            schema="PUBLIC",
            role="ACCOUNTADMIN",
            region="us-east-1"
        )
        self.save_config(sample_config)
        print("Sample configuration created. Please update with your actual Snowflake credentials.")

# Healthcare-specific Snowflake settings
HEALTHCARE_SNOWFLAKE_SETTINGS = {
    'warehouse_size': 'MEDIUM',
    'auto_suspend': 300,  # 5 minutes
    'auto_resume': True,
    'statement_timeout': 3600,  # 1 hour
    'query_tag': 'HEALTHCARE_ANALYTICS',
    'timezone': 'UTC'
}

# HIPAA compliance settings
HIPAA_COMPLIANCE_SETTINGS = {
    'data_retention_time_in_days': 2555,  # 7 years
    'enable_encryption': True,
    'enable_audit_logging': True,
    'enable_data_masking': True,
    'enable_row_level_security': True
}

def get_healthcare_snowflake_config() -> Dict:
    """Get healthcare-specific Snowflake configuration"""
    return {
        'settings': HEALTHCARE_SNOWFLAKE_SETTINGS,
        'compliance': HIPAA_COMPLIANCE_SETTINGS,
        'tables': {
            'patients': 'HEALTHCARE.PUBLIC.PATIENTS',
            'vital_signs': 'HEALTHCARE.PUBLIC.VITAL_SIGNS',
            'lab_results': 'HEALTHCARE.PUBLIC.LAB_RESULTS',
            'medications': 'HEALTHCARE.PUBLIC.MEDICATIONS',
            'encounters': 'HEALTHCARE.PUBLIC.ENCOUNTERS',
            'providers': 'HEALTHCARE.PUBLIC.PROVIDERS'
        }
    }
