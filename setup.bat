@echo off
echo ========================================
echo ChemVista Project Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Python detected...
python --version

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Git is not installed
    echo You can download it from https://git-scm.com
) else (
    echo Git detected...
    git --version
)

echo.
echo ========================================
echo Setting up ChemVista...
echo ========================================

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing Python packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install requirements
    echo Trying to install packages individually...
    pip install Flask==2.3.3
    pip install Werkzeug==2.3.7
    pip install Jinja2==3.1.2
    pip install MarkupSafe==2.1.3
    pip install itsdangerous==2.1.2
    pip install click==8.1.7
    pip install blinker==1.6.3
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To start the application:
echo 1. Run: start_app.bat
echo 2. Or manually:
echo    - venv\Scripts\activate
echo    - python app.py
echo.
echo The application will be available at:
echo http://localhost:5000
echo.
echo Press any key to start the application now...
pause >nul

REM Start the application
echo Starting ChemVista...
python app.py
