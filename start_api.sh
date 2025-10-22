#!/bin/bash
# Healthcare API Startup Script

echo "🏥 Starting Healthcare Patient Analytics API..."
echo "📡 API will be available at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔧 Interactive API: http://localhost:8000/redoc"
echo "💚 Health Check: http://localhost:8000/health"
echo ""
echo "🔑 Authentication Token: healthcare-api-token"
echo ""
echo "============================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Install API requirements if not already installed
echo "📦 Installing API requirements..."
pip install -r requirements-api.txt

# Start the API
echo "🚀 Starting API server..."
python start_api.py
