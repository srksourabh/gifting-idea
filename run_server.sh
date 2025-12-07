#!/bin/bash

# GiftingGenie API Server Startup Script

echo "🎁 Starting GiftingGenie API Server..."
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the server
echo "=================================="
echo "🚀 Starting FastAPI server..."
echo "API will be available at: http://localhost:8000"
echo "API Docs available at: http://localhost:8000/docs"
echo "=================================="

python app.py
