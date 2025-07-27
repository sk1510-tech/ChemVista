# ChemVista Deployment Guide

## Quick Start (5 minutes)

### Windows Users
1. Double-click `start.bat` file
2. Wait for automatic setup to complete
3. Open browser to http://localhost:5000

### macOS/Linux Users
1. Open terminal in project directory
2. Run: `./start.sh`
3. Open browser to http://localhost:5000

---

## Manual Installation

### Step 1: Prerequisites
- Python 3.7+ installed
- Git (optional, for cloning)
- Modern web browser

### Step 2: Download/Clone Project
```bash
# Option A: Clone from Git
git clone https://github.com/sk1510-tech/ChemVista.git
cd ChemVista

# Option B: Download and extract ZIP
# Extract to desired folder and open terminal there
```

### Step 3: Set Up Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run Application
```bash
python app.py
```

### Step 6: Access Application
Open browser and go to: http://localhost:5000

---

## Production Deployment

### Using Gunicorn (Recommended for Linux/macOS)
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Waitress (Windows Compatible)
```bash
# Install Waitress
pip install waitress

# Run with Waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

### Environment Variables
Set these for production:
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
```

---

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Build and Run
```bash
docker build -t chemvista .
docker run -p 5000:5000 chemvista
```

---

## Troubleshooting

### Common Issues

#### "Module not found" errors
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

#### Port already in use
- Use different port: `python app.py --port 8000`
- Or stop other services using port 5000

#### Permission denied on Linux/macOS
- Make start script executable: `chmod +x start.sh`

#### Python not found
- Install Python from python.org
- Ensure Python is in system PATH

### Browser Issues
- Clear browser cache
- Try different browser
- Check if JavaScript is enabled
- Ensure modern browser (Chrome 80+, Firefox 75+)

### Performance Issues
- Close unnecessary browser tabs
- Check available system memory
- Restart application if needed

---

## Configuration

### Customizing Data
- Edit `data/elements.json` for element information
- Edit `data/compounds.json` for compound data
- Restart application after changes

### Styling Changes
- Modify `static/css/style.css`
- Update colors in CSS variables
- Changes apply immediately (refresh browser)

### Port Configuration
Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8000)
```

---

## Network Access

### Local Network Access
Application is accessible on local network:
- Find your IP: `ipconfig` (Windows) or `ifconfig` (macOS/Linux)
- Access via: http://[YOUR_IP]:5000

### Firewall Configuration
Allow port 5000 through firewall:
- Windows: Windows Defender Firewall settings
- macOS: System Preferences > Security & Privacy
- Linux: `sudo ufw allow 5000`

---

## Updates and Maintenance

### Updating Application
```bash
# Pull latest changes (if using Git)
git pull origin main

# Restart application
python app.py
```

### Backup Data
Important files to backup:
- `data/elements.json`
- `data/compounds.json`
- `static/css/style.css` (if customized)

### Log Files
Check application logs for errors:
- Console output shows real-time logs
- Use logging in production deployment

---

## Support

### Getting Help
1. Check this deployment guide
2. Review README.md for features
3. Check GitHub Issues for known problems
4. Submit new issue with error details

### System Requirements
- **RAM**: 256MB minimum, 512MB recommended
- **Storage**: 50MB for application files
- **Network**: Local network or internet for external access
- **Browser**: Modern browser with JavaScript enabled

---

*Successfully deployed? Visit http://localhost:5000 to start exploring chemistry!* 🧪
