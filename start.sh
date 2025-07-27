#!/bin/bash

echo "Starting ChemVista Application..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt
echo

# Start the application
echo "Starting Flask application..."
echo "Open your browser and go to: http://localhost:5000"
echo "Press Ctrl+C to stop the application"
echo
python app.py
