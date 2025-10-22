#!/usr/bin/env python3
"""
Healthcare API Startup Script
============================
Startup script for the Healthcare Patient Analytics REST API.
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

def main():
    """Start the Healthcare API server"""
    print("🏥 Starting Healthcare Patient Analytics API...")
    print("📡 API will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔧 Interactive API: http://localhost:8000/redoc")
    print("💚 Health Check: http://localhost:8000/health")
    print("\n🔑 Authentication Token: healthcare-api-token")
    print("\n" + "="*60)
    
    # Start the server
    uvicorn.run(
        "src.api.healthcare_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
