@echo off
title ChemVista - Interactive Chemistry Explorer

echo ========================================
echo Starting ChemVista...
echo ========================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found!
    echo Please run setup.bat first to set up the project.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if Flask is installed
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo Flask not found! Installing dependencies...
    pip install -r requirements.txt
)

REM Start the application
echo.
echo ========================================
echo ChemVista is starting...
echo ========================================
echo Application will be available at:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================

python app.py

echo.
echo ChemVista has stopped.
pause
