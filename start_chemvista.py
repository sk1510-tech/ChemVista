#!/usr/bin/env python3
"""
ChemVista Launcher
Simple script to start the ChemVista Flask application
"""

import sys
import os
import subprocess

def main():
    """Launch the ChemVista application"""
    print("🧪 ChemVista - Interactive Chemistry Explorer")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found. Please run from the ChemVista directory.")
        return False
    
    try:
        print("🚀 Starting ChemVista server...")
        print("📍 Open your browser and go to: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Start the Flask application
        result = subprocess.run([sys.executable, "app.py"], check=True)
        return True
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
