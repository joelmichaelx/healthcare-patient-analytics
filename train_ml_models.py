#!/usr/bin/env python3
"""
Train Healthcare ML Models
==========================
Script to train all healthcare machine learning models
for readmission risk, sepsis detection, and medication adherence.
"""

import os
import sys
import json
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ml.healthcare_ml_models import HealthcareMLModels

def main():
    """Main function to train all healthcare ML models"""
    print("Healthcare Machine Learning Models Training")
    print("=" * 60)
    print(f"Training started at: {datetime.now()}")
    print()
    
    try:
        # Initialize ML models
        print("Initializing ML models...")
        ml_models = HealthcareMLModels()
        
        # Load data from Snowflake
        print("Loading data from Snowflake...")
        data = ml_models.load_data_from_snowflake()
        
        if data is None:
            print(" Error: Could not load data from Snowflake")
            print("Please check your Snowflake connection and credentials.")
            return
        
        print(" Data loaded successfully:")
        print(f"   Patients: {len(data['patients'])}")
        print(f"   Vital Signs: {len(data['vital_signs'])}")
        print(f"   Lab Results: {len(data['lab_results'])}")
        print(f"   Medications: {len(data['medications'])}")
        print()
        
        # Prepare features for each model
        print("Preparing features for ML models...")
        print("   Readmission risk features...")
        readmission_features = ml_models.prepare_readmission_features(data)
        print(f"     {len(readmission_features)} patients with readmission features")
        
        print("   Sepsis detection features...")
        sepsis_features = ml_models.prepare_sepsis_features(data)
        print(f"     {len(sepsis_features)} patients with sepsis features")
        
        print("   Medication adherence features...")
        adherence_features = ml_models.prepare_medication_adherence_features(data)
        print(f"     {len(adherence_features)} patients with adherence features")
        print()
        
        # Train models
        print("Training ML models...")
        print("   Training readmission risk model...")
        readmission_model, X_test, y_test = ml_models.train_readmission_model(readmission_features)
        print("     Readmission model trained successfully")
        
        print("   Training sepsis detection model...")
        sepsis_model, X_test, y_test = ml_models.train_sepsis_model(sepsis_features)
        print("     Sepsis model trained successfully")
        
        print("   Training medication adherence model...")
        adherence_model, X_test, y_test = ml_models.train_adherence_model(adherence_features)
        print("     Adherence model trained successfully")
        print()
        
        # Save models
        print("Saving trained models...")
        ml_models.save_models()
        print("   Models saved to models/ directory")
        print("   Scalers saved to models/ directory")
        print("   Label encoders saved to models/ directory")
        print("   Feature importance saved to models/feature_importance.json")
        print()
        
        # Display model summary
        print(" ML Model Training Summary")
        print("=" * 40)
        print(" Readmission Risk Prediction Model")
        print("   - Predicts patient readmission risk")
        print("   - Uses patient demographics, vital signs, lab results")
        print("   - Helps identify high-risk patients")
        print()
        print(" Sepsis Detection Model")
        print("   - Detects early signs of sepsis")
        print("   - Uses vital signs and lab values")
        print("   - Critical for patient safety")
        print()
        print(" Medication Adherence Model")
        print("   - Predicts medication adherence patterns")
        print("   - Uses patient history and medication data")
        print("   - Helps improve treatment outcomes")
        print()
        print(" All healthcare ML models are now ready for prediction!")
        print("   - Use the ML dashboard to make predictions")
        print("   - Models are integrated with Snowflake data")
        print("   - Real-time predictions available")
        print()
        print(f"Training completed at: {datetime.now()}")
        
    except Exception as e:
        print(f" Error during training: {e}")
        print("Please check your environment and try again.")
        return

if __name__ == "__main__":
    main()
