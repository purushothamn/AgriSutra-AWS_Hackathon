@echo off
REM AgriSutra Setup Script for Windows
REM This script sets up the Python virtual environment and installs dependencies

echo Setting up AgriSutra Farm Intelligence System...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env file with your AWS credentials
)

echo Setup complete!
echo To activate the virtual environment, run: venv\Scripts\activate.bat
echo To run tests, use: pytest
echo To run the Streamlit app, use: streamlit run app.py
