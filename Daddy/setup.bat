@echo off
REM Daddy Expense Tracker - Setup Script for Windows

echo.
echo =========================================
echo   Daddy - Expense Tracker Setup
echo =========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error creating virtual environment
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies
    pause
    exit /b 1
)

echo [4/4] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Environment file created. Please edit .env with your configuration.
) else (
    echo Environment file already exists.
)

echo.
echo =========================================
echo   Setup Complete!
echo =========================================
echo.
echo To run the application:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run the app: python run.py
echo   3. Open browser: http://localhost:5000
echo.
pause
setup.batsetup.bat