#!/bin/bash

# Check if virtual environment exists, if not create it
if [ ! -d "./venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source ./venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the FastAPI application
echo "Starting FastAPI application..."
uvicorn main:app --reload