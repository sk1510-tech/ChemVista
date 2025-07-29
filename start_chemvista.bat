@echo off
echo Starting ChemVista Chemistry Explorer...
echo.

cd /d "d:\freelance\ChemVista"

REM Activate virtual environment
call "venv\Scripts\activate.bat"

REM Run the application
echo Running Flask application...
python app.py

pause
