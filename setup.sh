#!/bin/bash

echo "========================================"
echo "ChemVista Project Setup Script"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}ERROR: Python is not installed${NC}"
        echo "Please install Python 3.7+ from https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo -e "${GREEN}Python detected...${NC}"
$PYTHON_CMD --version

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}WARNING: Git is not installed${NC}"
    echo "You can download it from https://git-scm.com"
else
    echo -e "${GREEN}Git detected...${NC}"
    git --version
fi

echo
echo "========================================"
echo "Setting up ChemVista..."
echo "========================================"

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
$PYTHON_CMD -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Failed to create virtual environment${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Failed to activate virtual environment${NC}"
    exit 1
fi

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "${BLUE}Installing Python packages...${NC}"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Failed to install from requirements.txt, trying individual packages...${NC}"
    pip install Flask==2.3.3
    pip install Werkzeug==2.3.7
    pip install Jinja2==3.1.2
    pip install MarkupSafe==2.1.3
    pip install itsdangerous==2.1.2
    pip install click==8.1.7
    pip install blinker==1.6.3
fi

# Make scripts executable
chmod +x start.sh

echo
echo "========================================"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo "========================================"
echo
echo "To start the application:"
echo "1. Run: ./start.sh"
echo "2. Or manually:"
echo "   - source venv/bin/activate"
echo "   - python app.py"
echo
echo "The application will be available at:"
echo -e "${BLUE}http://localhost:5000${NC}"
echo

# Ask if user wants to start the app now
read -p "Would you like to start the application now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Starting ChemVista...${NC}"
    $PYTHON_CMD app.py
fi
