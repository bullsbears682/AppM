#!/usr/bin/env python3
"""
Business ROI Calculator - Startup Script
Quick way to run the application
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if required packages are installed"""
    try:
        import flask
        print("✅ Flask is installed")
        return True
    except ImportError:
        print("❌ Flask not found. Installing requirements...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install requirements")
            return False

def main():
    print("🚀 Business ROI Calculator")
    print("=" * 50)
    
    if not check_requirements():
        return
    
    print("🌐 Starting application...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🎯 Calculate ROI for any business project!")
    print("=" * 50)
    
    # Import and run the app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()