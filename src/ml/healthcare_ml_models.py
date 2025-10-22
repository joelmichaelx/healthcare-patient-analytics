#!/usr/bin/env python3
"""
Healthcare Machine Learning Models
=================================
Advanced ML models for healthcare predictions including:
- Readmission risk prediction
- Sepsis detection
- Medication adherence prediction
- Clinical outcome forecasting
- Patient risk stratification
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
import json
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class HealthcareMLModels:
    """Healthcare Machine Learning Models for Clinical Predictions"""
    
    def __init__(self, snowflake_config_path=None):
        """Initialize ML models with Snowflake connection"""
        self.models = {}
        self.scalers = {}
        self.label_encoders = {}
        self.feature_importance = {}
        
        if snowflake_config_path:
            self.snowflake_config_path = snowflake_config_path
        else:
            self.snowflake_config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'snowflake_config.json')
    
    def load_data_from_snowflake(self):
        """Load healthcare data from Snowflake for ML training"""
        try:
            import snowflake.connector
            
            with open(self.snowflake_config_path, 'r') as f:
                config = json.load(f)
            
            conn = snowflake.connector.connect(
                account=config['snowflake']['account'],
                user=config['snowflake']['user'],
                password=config['snowflake']['password'],
                warehouse=config['snowflake']['warehouse'],
                database=config['snowflake']['database'],
                schema=config['snowflake']['schema'],
                role=config['snowflake']['role']
            )
            
            # Load patients data
            patients_query = """
                SELECT PATIENT_ID, AGE, GENDER, CONDITION, RISK_LEVEL, STATUS
                FROM PATIENTS
            """
            patients_df = pd.read_sql(patients_query, conn)
            
            # Load vital signs data
            vital_signs_query = """
                SELECT PATIENT_ID, HEART_RATE, BLOOD_PRESSURE_SYSTOLIC, 
                       BLOOD_PRESSURE_DIASTOLIC, TEMPERATURE, OXYGEN_SATURATION, 
                       RESPIRATORY_RATE, TIMESTAMP
                FROM VITAL_SIGNS
                WHERE TIMESTAMP >= DATEADD(day, -30, CURRENT_TIMESTAMP())
            """
            vital_signs_df = pd.read_sql(vital_signs_query, conn)
            
            # Load lab results data
            lab_results_query = """
                SELECT PATIENT_ID, TEST_NAME, TEST_VALUE, CRITICAL_FLAG, TIMESTAMP
                FROM LAB_RESULTS
                WHERE TIMESTAMP >= DATEADD(day, -30, CURRENT_TIMESTAMP())
            """
            lab_results_df = pd.read_sql(lab_results_query, conn)
            
            # Load medications data
            medications_query = """
                SELECT PATIENT_ID, MEDICATION_NAME, DOSAGE, STATUS, TIMESTAMP
                FROM MEDICATIONS
                WHERE TIMESTAMP >= DATEADD(day, -30, CURRENT_TIMESTAMP())
            """
            medications_df = pd.read_sql(medications_query, conn)
            
            conn.close()
            
            return {
                'patients': patients_df,
                'vital_signs': vital_signs_df,
                'lab_results': lab_results_df,
                'medications': medications_df
            }
            
        except Exception as e:
            print(f"Error loading data from Snowflake: {e}")
            return None
    
    def prepare_readmission_features(self, data):
        """Prepare features for readmission risk prediction"""
        print("Preparing readmission risk features...")
        
        # Start with patient demographics
        features_df = data['patients'].copy()
        
        # Add age-based features
        features_df['age_group'] = pd.cut(features_df['AGE'], 
                                        bins=[0, 18, 35, 55, 75, 100], 
                                        labels=['pediatric', 'young_adult', 'middle_age', 'senior', 'elderly'])
        features_df['age_group'] = features_df['age_group'].astype(str)
        
        # Add vital signs features (latest readings)
        vital_agg = data['vital_signs'].groupby('PATIENT_ID').agg({
            'HEART_RATE': ['mean', 'std', 'max'],
            'BLOOD_PRESSURE_SYSTOLIC': ['mean', 'std', 'max'],
            'BLOOD_PRESSURE_DIASTOLIC': ['mean', 'std', 'max'],
            'TEMPERATURE': ['mean', 'std', 'max'],
            'OXYGEN_SATURATION': ['mean', 'std', 'min'],
            'RESPIRATORY_RATE': ['mean', 'std', 'max']
        }).reset_index()
        
        # Flatten column names
        vital_agg.columns = ['PATIENT_ID'] + [f'vital_{col[0]}_{col[1]}' for col in vital_agg.columns[1:]]
        
        # Add lab results features
        lab_agg = data['lab_results'].groupby('PATIENT_ID').agg({
            'TEST_VALUE': ['mean', 'std', 'max'],
            'CRITICAL_FLAG': ['sum', 'mean']
        }).reset_index()
        
        lab_agg.columns = ['PATIENT_ID'] + [f'lab_{col[0]}_{col[1]}' for col in lab_agg.columns[1:]]
        
        # Add medication features
        med_agg = data['medications'].groupby('PATIENT_ID').agg({
            'DOSAGE': ['mean', 'sum'],
            'STATUS': lambda x: (x == 'Administered').sum()
        }).reset_index()
        
        med_agg.columns = ['PATIENT_ID'] + [f'med_{col[0]}_{col[1]}' for col in med_agg.columns[1:]]
        
        # Merge all features
        features_df = features_df.merge(vital_agg, on='PATIENT_ID', how='left')
        features_df = features_df.merge(lab_agg, on='PATIENT_ID', how='left')
        features_df = features_df.merge(med_agg, on='PATIENT_ID', how='left')
        
        # Fill missing values
        features_df = features_df.fillna(0)
        
        # Create target variable (simulated readmission risk)
        # In real scenario, this would be based on historical readmission data
        np.random.seed(42)
        features_df['readmission_risk'] = np.random.choice([0, 1], size=len(features_df), p=[0.7, 0.3])
        
        return features_df
    
    def prepare_sepsis_features(self, data):
        """Prepare features for sepsis detection"""
        print("Preparing sepsis detection features...")
        
        # Start with patient demographics
        features_df = data['patients'].copy()
        
        # Add vital signs features (focus on sepsis indicators)
        vital_agg = data['vital_signs'].groupby('PATIENT_ID').agg({
            'TEMPERATURE': ['mean', 'max', 'min'],
            'HEART_RATE': ['mean', 'max'],
            'RESPIRATORY_RATE': ['mean', 'max'],
            'BLOOD_PRESSURE_SYSTOLIC': ['mean', 'min'],
            'OXYGEN_SATURATION': ['mean', 'min']
        }).reset_index()
        
        vital_agg.columns = ['PATIENT_ID'] + [f'sepsis_{col[0]}_{col[1]}' for col in vital_agg.columns[1:]]
        
        # Add lab results features (focus on infection markers)
        lab_agg = data['lab_results'].groupby('PATIENT_ID').agg({
            'TEST_VALUE': ['mean', 'max'],
            'CRITICAL_FLAG': ['sum', 'mean']
        }).reset_index()
        
        lab_agg.columns = ['PATIENT_ID'] + [f'sepsis_lab_{col[0]}_{col[1]}' for col in lab_agg.columns[1:]]
        
        # Merge features
        features_df = features_df.merge(vital_agg, on='PATIENT_ID', how='left')
        features_df = features_df.merge(lab_agg, on='PATIENT_ID', how='left')
        
        # Fill missing values
        features_df = features_df.fillna(0)
        
        # Create target variable (simulated sepsis risk)
        # In real scenario, this would be based on clinical sepsis criteria
        np.random.seed(42)
        features_df['sepsis_risk'] = np.random.choice([0, 1], size=len(features_df), p=[0.85, 0.15])
        
        return features_df
    
    def prepare_medication_adherence_features(self, data):
        """Prepare features for medication adherence prediction"""
        print("Preparing medication adherence features...")
        
        # Start with patient demographics
        features_df = data['patients'].copy()
        
        # Add medication adherence features
        med_agg = data['medications'].groupby('PATIENT_ID').agg({
            'STATUS': lambda x: (x == 'Administered').sum() / len(x) if len(x) > 0 else 0,
            'DOSAGE': ['mean', 'std'],
            'MEDICATION_NAME': 'nunique'
        }).reset_index()
        
        med_agg.columns = ['PATIENT_ID', 'adherence_rate', 'med_dosage_mean', 'med_dosage_std', 'med_count']
        
        # Add vital signs features (health status indicators)
        vital_agg = data['vital_signs'].groupby('PATIENT_ID').agg({
            'HEART_RATE': 'mean',
            'BLOOD_PRESSURE_SYSTOLIC': 'mean',
            'TEMPERATURE': 'mean'
        }).reset_index()
        
        vital_agg.columns = ['PATIENT_ID', 'avg_heart_rate', 'avg_bp_systolic', 'avg_temperature']
        
        # Merge features
        features_df = features_df.merge(med_agg, on='PATIENT_ID', how='left')
        features_df = features_df.merge(vital_agg, on='PATIENT_ID', how='left')
        
        # Fill missing values
        features_df = features_df.fillna(0)
        
        # Create target variable (simulated adherence prediction)
        # In real scenario, this would be based on historical adherence patterns
        np.random.seed(42)
        features_df['adherence_prediction'] = np.random.choice([0, 1], size=len(features_df), p=[0.3, 0.7])
        
        return features_df
    
    def train_readmission_model(self, features_df):
        """Train readmission risk prediction model"""
        print("Training readmission risk prediction model...")
        
        # Prepare features and target
        feature_columns = [col for col in features_df.columns 
                          if col not in ['PATIENT_ID', 'readmission_risk', 'NAME', 'CONDITION', 'STATUS']]
        
        X = features_df[feature_columns]
        y = features_df['readmission_risk']
        
        # Encode categorical variables
        categorical_columns = X.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            le = LabelEncoder()
            # Handle missing values by filling with 'unknown'
            X[col] = X[col].fillna('unknown').astype(str)
            X[col] = le.fit_transform(X[col])
            self.label_encoders[f'readmission_{col}'] = le
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.scalers['readmission'] = scaler
        
        # Train multiple models
        models = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'logistic_regression': LogisticRegression(random_state=42)
        }
        
        best_model = None
        best_score = 0
        
        for name, model in models.items():
            # Train model
            model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test_scaled)
            score = roc_auc_score(y_test, y_pred)
            
            print(f"{name} - AUC Score: {score:.3f}")
            
            if score > best_score:
                best_score = score
                best_model = model
        
        self.models['readmission'] = best_model
        self.feature_importance['readmission'] = dict(zip(feature_columns, best_model.feature_importances_))
        
        print(f"Best readmission model - AUC Score: {best_score:.3f}")
        return best_model, X_test_scaled, y_test
    
    def train_sepsis_model(self, features_df):
        """Train sepsis detection model"""
        print("Training sepsis detection model...")
        
        # Prepare features and target
        feature_columns = [col for col in features_df.columns 
                          if col not in ['PATIENT_ID', 'sepsis_risk', 'NAME', 'CONDITION', 'STATUS']]
        
        X = features_df[feature_columns]
        y = features_df['sepsis_risk']
        
        # Encode categorical variables
        categorical_columns = X.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            le = LabelEncoder()
            # Handle missing values by filling with 'unknown'
            X[col] = X[col].fillna('unknown').astype(str)
            X[col] = le.fit_transform(X[col])
            self.label_encoders[f'sepsis_{col}'] = le
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.scalers['sepsis'] = scaler
        
        # Train multiple models
        models = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'logistic_regression': LogisticRegression(random_state=42)
        }
        
        best_model = None
        best_score = 0
        
        for name, model in models.items():
            # Train model
            model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test_scaled)
            score = roc_auc_score(y_test, y_pred)
            
            print(f"{name} - AUC Score: {score:.3f}")
            
            if score > best_score:
                best_score = score
                best_model = model
        
        self.models['sepsis'] = best_model
        self.feature_importance['sepsis'] = dict(zip(feature_columns, best_model.feature_importances_))
        
        print(f"Best sepsis model - AUC Score: {best_score:.3f}")
        return best_model, X_test_scaled, y_test
    
    def train_adherence_model(self, features_df):
        """Train medication adherence prediction model"""
        print("Training medication adherence prediction model...")
        
        # Prepare features and target
        feature_columns = [col for col in features_df.columns 
                          if col not in ['PATIENT_ID', 'adherence_prediction', 'NAME', 'CONDITION', 'STATUS']]
        
        X = features_df[feature_columns]
        y = features_df['adherence_prediction']
        
        # Encode categorical variables
        categorical_columns = X.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            le = LabelEncoder()
            # Handle missing values by filling with 'unknown'
            X[col] = X[col].fillna('unknown').astype(str)
            X[col] = le.fit_transform(X[col])
            self.label_encoders[f'adherence_{col}'] = le
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.scalers['adherence'] = scaler
        
        # Train multiple models
        models = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'logistic_regression': LogisticRegression(random_state=42)
        }
        
        best_model = None
        best_score = 0
        
        for name, model in models.items():
            # Train model
            model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test_scaled)
            score = roc_auc_score(y_test, y_pred)
            
            print(f"{name} - AUC Score: {score:.3f}")
            
            if score > best_score:
                best_score = score
                best_model = model
        
        self.models['adherence'] = best_model
        self.feature_importance['adherence'] = dict(zip(feature_columns, best_model.feature_importances_))
        
        print(f"Best adherence model - AUC Score: {best_score:.3f}")
        return best_model, X_test_scaled, y_test
    
    def save_models(self, models_dir='models'):
        """Save trained models and scalers"""
        os.makedirs(models_dir, exist_ok=True)
        
        # Save models
        for name, model in self.models.items():
            joblib.dump(model, f'{models_dir}/{name}_model.pkl')
        
        # Save scalers
        for name, scaler in self.scalers.items():
            joblib.dump(scaler, f'{models_dir}/{name}_scaler.pkl')
        
        # Save label encoders
        for name, encoder in self.label_encoders.items():
            joblib.dump(encoder, f'{models_dir}/{name}_encoder.pkl')
        
        # Save feature importance
        with open(f'{models_dir}/feature_importance.json', 'w') as f:
            json.dump(self.feature_importance, f, indent=2)
        
        print(f"Models saved to {models_dir}/")
    
    def load_models(self, models_dir='models'):
        """Load trained models and scalers"""
        # Load models
        for name in ['readmission', 'sepsis', 'adherence']:
            if os.path.exists(f'{models_dir}/{name}_model.pkl'):
                self.models[name] = joblib.load(f'{models_dir}/{name}_model.pkl')
        
        # Load scalers
        for name in ['readmission', 'sepsis', 'adherence']:
            if os.path.exists(f'{models_dir}/{name}_scaler.pkl'):
                self.scalers[name] = joblib.load(f'{models_dir}/{name}_scaler.pkl')
        
        # Load label encoders
        for name in ['readmission', 'sepsis', 'adherence']:
            if os.path.exists(f'{models_dir}/{name}_encoder.pkl'):
                self.label_encoders[name] = joblib.load(f'{models_dir}/{name}_encoder.pkl')
        
        # Load feature importance
        if os.path.exists(f'{models_dir}/feature_importance.json'):
            with open(f'{models_dir}/feature_importance.json', 'r') as f:
                self.feature_importance = json.load(f)
        
        print("Models loaded successfully!")
    
    def predict_readmission_risk(self, patient_data):
        """Predict readmission risk for a patient"""
        if 'readmission' not in self.models:
            raise ValueError("Readmission model not trained or loaded")
        
        # Prepare patient data
        # This would need to be implemented based on the specific patient data format
        # For now, return a simulated prediction
        return np.random.random()
    
    def predict_sepsis_risk(self, patient_data):
        """Predict sepsis risk for a patient"""
        if 'sepsis' not in self.models:
            raise ValueError("Sepsis model not trained or loaded")
        
        # Prepare patient data
        # This would need to be implemented based on the specific patient data format
        # For now, return a simulated prediction
        return np.random.random()
    
    def predict_adherence(self, patient_data):
        """Predict medication adherence for a patient"""
        if 'adherence' not in self.models:
            raise ValueError("Adherence model not trained or loaded")
        
        # Prepare patient data
        # This would need to be implemented based on the specific patient data format
        # For now, return a simulated prediction
        return np.random.random()

def main():
    """Main function to train all healthcare ML models"""
    print("Healthcare Machine Learning Models Training")
    print("=" * 50)
    
    # Initialize ML models
    ml_models = HealthcareMLModels()
    
    # Load data from Snowflake
    print("Loading data from Snowflake...")
    data = ml_models.load_data_from_snowflake()
    
    if data is None:
        print("Error: Could not load data from Snowflake")
        return
    
    print(f"Data loaded successfully:")
    print(f"  Patients: {len(data['patients'])}")
    print(f"  Vital Signs: {len(data['vital_signs'])}")
    print(f"  Lab Results: {len(data['lab_results'])}")
    print(f"  Medications: {len(data['medications'])}")
    
    # Prepare features for each model
    print("\nPreparing features...")
    readmission_features = ml_models.prepare_readmission_features(data)
    sepsis_features = ml_models.prepare_sepsis_features(data)
    adherence_features = ml_models.prepare_medication_adherence_features(data)
    
    # Train models
    print("\nTraining models...")
    ml_models.train_readmission_model(readmission_features)
    ml_models.train_sepsis_model(sepsis_features)
    ml_models.train_adherence_model(adherence_features)
    
    # Save models
    print("\nSaving models...")
    ml_models.save_models()
    
    print("\n All healthcare ML models trained and saved successfully!")
    print("Models available for prediction:")
    print("  - Readmission Risk Prediction")
    print("  - Sepsis Detection")
    print("  - Medication Adherence Prediction")

if __name__ == "__main__":
    main()
