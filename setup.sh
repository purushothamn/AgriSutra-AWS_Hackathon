#!/bin/bash

# AgriSutra Setup Script
# This script sets up the Python virtual environment and installs dependencies

echo "Setting up AgriSutra Farm Intelligence System..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your AWS credentials"
fi

echo "Setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"
echo "To run tests, use: pytest"
echo "To run the Streamlit app, use: streamlit run app.py"
