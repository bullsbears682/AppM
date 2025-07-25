#!/usr/bin/env python3
"""
Termux-Compatible Launcher for Business ROI Calculator v2.0
Handles dependency issues gracefully and provides fallbacks
"""

import os
import sys
import subprocess

def check_and_install_dependencies():
    """Check and install required dependencies for Termux"""
    required_packages = [
        'Flask==2.3.3',
        'Werkzeug==2.3.7', 
        'requests==2.31.0',
        'flask-cors==4.0.0',
        'python-dotenv==1.0.0'
    ]
    
    print("🔧 Checking dependencies...")
    
    for package in required_packages:
        try:
            package_name = package.split('==')[0].replace('-', '_').lower()
            if package_name == 'flask_cors':
                package_name = 'flask_cors'
            __import__(package_name)
            print(f"✅ {package.split('==')[0]} - OK")
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', 
                '--break-system-packages', '--no-cache-dir', package
            ], check=False)
    
    # Try to install numpy, but don't fail if it doesn't work
    try:
        import numpy
        print("✅ NumPy - OK (full features available)")
    except ImportError:
        print("⚠️  NumPy not found - trying to install...")
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install',
            '--break-system-packages', '--no-cache-dir', 'numpy'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("⚠️  NumPy installation failed - using simplified calculations")
            print("💡 App will still work with most features!")

def main():
    """Main launcher function"""
    print("🚀 Starting Business ROI Calculator v2.0 for Termux")
    print("=" * 50)
    
    # Check dependencies
    check_and_install_dependencies()
    
    # Set Termux-friendly environment variables
    os.environ['TERMUX_MODE'] = 'true'
    os.environ['LOG_LEVEL'] = 'WARNING'  # Reduce log noise
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("📝 Creating Termux-optimized configuration...")
        with open('.env', 'w') as f:
            f.write("""# Termux Configuration for ROI Calculator v2.0
FLASK_ENV=development
DEBUG=True
SECRET_KEY=termux-dev-key-change-in-production
HOST=0.0.0.0
PORT=5000
ENABLE_CORS=True
LOG_LEVEL=WARNING
CALCULATION_PRECISION=2
""")
    
    print("\n🎯 Configuration:")
    print("   • URL: http://localhost:5000")
    print("   • Mode: Termux-optimized")
    print("   • Features: All enhanced v2.0 features")
    print("   • Calculations: Advanced financial modeling")
    print("\n⏳ Starting server...")
    
    # Import and run the main application
    try:
        from app import app, config_class, logger
        logger.info("Starting Business ROI Calculator v2.0 in Termux mode")
        app.run(
            debug=config_class.DEBUG,
            host=config_class.HOST,
            port=config_class.PORT,
            use_reloader=False  # Disable reloader for Termux stability
        )
    except KeyboardInterrupt:
        print("\n👋 ROI Calculator stopped")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("\n🔧 Try running: pip install --break-system-packages Flask")
        sys.exit(1)

if __name__ == '__main__':
    main()