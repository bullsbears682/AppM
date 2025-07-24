#!/bin/bash

echo "🚀 Starting DevCost - Real-Time Development Cost Analytics"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/pyvenv.cfg" ] || ! pip show Flask > /dev/null 2>&1; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "⚠️  Warning: This directory is not a git repository."
    echo "   DevCost analyzes git commit history to calculate development costs."
    echo "   For best results, run this in a git repository with commit history."
    echo ""
fi

echo "🌐 Starting DevCost server..."
echo "📊 Dashboard will be available at: http://localhost:5000"
echo "🔄 Auto-refresh every 5 minutes"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================================="

# Start the Flask application
python app.py