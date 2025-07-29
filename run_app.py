#!/usr/bin/env python3
"""
Test script to run ChemVista Flask application
"""

import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the Flask app
try:
    from app import app
    print("✅ Flask app imported successfully!")
    print("🚀 Starting ChemVista on http://localhost:5000")
    print("📊 Available routes:")
    
    # List all routes
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
        print(f"   {rule.rule:<30} [{methods}]")
    
    print("\n" + "="*50)
    print("🧪 ChemVista is ready! Open http://localhost:5000 in your browser")
    print("="*50)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error running app: {e}")
    sys.exit(1)
