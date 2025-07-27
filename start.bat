@echo off
echo Starting ChemVista Application...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Start the application
echo Starting Flask application...
echo Open your browser and go to: http://localhost:5000
echo Press Ctrl+C to stop the application
echo.
python app.py

pause
