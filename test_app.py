#!/usr/bin/env python3
"""
Healthcare Patient Analytics Platform - Test Script
Tests the application components
"""

import sys
import os
sys.path.append('.')

def test_imports():
    """Test if all required packages can be imported"""
    try:
        import streamlit
        import pandas
        import plotly
        import numpy
        import sklearn
        print(" All required packages imported successfully")
        return True
    except ImportError as e:
        print(f" Import error: {e}")
        return False

def test_database():
    """Test database connection"""
    try:
        import sqlite3
        conn = sqlite3.connect('healthcare_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f" Database connected. Tables: {[table[0] for table in tables]}")
        conn.close()
        return True
    except Exception as e:
        print(f" Database error: {e}")
        return False

def test_streamlit_app():
    """Test Streamlit app import"""
    try:
        from dashboards.healthcare_streamlit_app import HealthcareDashboard
        print(" Streamlit app imports successfully")
        return True
    except Exception as e:
        print(f" Streamlit app error: {e}")
        return False

def main():
    """Run all tests"""
    print("Healthcare Patient Analytics Platform - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Database Connection", test_database),
        ("Streamlit App", test_streamlit_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f" {test_name} failed")
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print(" All tests passed! Your healthcare analytics platform is ready.")
        print("\nNext steps:")
        print("1. Run: ./start_dashboard.sh")
        print("2. Open: http://localhost:8501")
        print("3. Explore the dashboard features")
    else:
        print("  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
