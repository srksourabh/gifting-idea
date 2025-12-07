#!/bin/bash

echo "🎁 GiftingGenie - Quick Start Guide"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

echo "✅ Using Python: $PYTHON_CMD"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✅ Dependencies installed successfully!"
echo ""
echo "🚀 Starting GiftingGenie server..."
echo ""
echo "=================================="
echo "📍 Web Interface: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo "=================================="
echo ""

# Start the server
$PYTHON_CMD app.py
