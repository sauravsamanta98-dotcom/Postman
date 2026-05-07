#!/bin/bash
# Daddy Expense Tracker - Setup Script for Linux/Mac

echo ""
echo "========================================="
echo "  Daddy - Expense Tracker Setup"
echo "========================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "[1/4] Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "Error creating virtual environment"
    exit 1
fi

echo "[2/4] Activating virtual environment..."
source venv/bin/activate

echo "[3/4] Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error installing dependencies"
    exit 1
fi

echo "[4/4] Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Environment file created. Please edit .env with your configuration."
else
    echo "Environment file already exists."
fi

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: python run.py"
echo "  3. Open browser: http://localhost:5000"
echo ""
