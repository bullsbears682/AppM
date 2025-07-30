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

def setup_repository():
    """Setup the repository if not already present"""
    if not os.path.exists('app.py'):
        print("📥 Repository not found locally, cloning...")
        subprocess.run([
            'git', 'clone', 'https://github.com/bullsbears682/AppM.git', '.'
        ], check=False)
        
        if not os.path.exists('app.py'):
            print("❌ Failed to clone repository. Trying alternative method...")
            # Try downloading individual files
            files_to_download = [
                ('https://raw.githubusercontent.com/bullsbears682/AppM/main/app.py', 'app.py'),
                ('https://raw.githubusercontent.com/bullsbears682/AppM/main/config.py', 'config.py'),
                ('https://raw.githubusercontent.com/bullsbears682/AppM/main/templates/index.html', 'templates/index.html'),
                ('https://raw.githubusercontent.com/bullsbears682/AppM/main/utils/__init__.py', 'utils/__init__.py'),
                ('https://raw.githubusercontent.com/bullsbears682/AppM/main/utils/validators.py', 'utils/validators.py'),
                ('https://raw.githubusercontent.com/bullsbears682/AppM/main/utils/calculator.py', 'utils/calculator.py'),
                ('https://raw.githubusercontent.com/bullsbears682/AppM/main/utils/cache.py', 'utils/cache.py'),
                ('https://raw.githubusercontent.com/bullsbears682/AppM/main/utils/rate_limiter.py', 'utils/rate_limiter.py'),
                ('https://raw.githubusercontent.com/bullsbears682/AppM/main/utils/export.py', 'utils/export.py'),
            ]
            
            os.makedirs('templates', exist_ok=True)
            os.makedirs('utils', exist_ok=True)
            
            try:
                import urllib.request
                for url, filename in files_to_download:
                    print(f"📄 Downloading {filename}...")
                    try:
                        urllib.request.urlretrieve(url, filename)
                    except Exception as e:
                        print(f"⚠️  Failed to download {filename}: {e}")
            except Exception as e:
                print(f"❌ Download failed: {e}")
                print("🔧 Please run this from the AppM directory or install git:")
                print("   pkg install git && git clone https://github.com/bullsbears682/AppM.git && cd AppM")
                sys.exit(1)

def main():
    """Main launcher function"""
    print("🚀 Starting Business ROI Calculator v2.0 for Termux - Quantum Edition")
    print("=" * 60)
    
    # Setup repository if needed
    setup_repository()
    
    # Check dependencies
    check_and_install_dependencies()
    
    # Set Termux-friendly environment variables
    os.environ['TERMUX_MODE'] = 'true'
    os.environ['LOG_LEVEL'] = 'WARNING'  # Reduce log noise
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("📝 Creating Termux-optimized configuration...")
        with open('.env', 'w') as f:
            f.write(f"""# Termux Configuration for ROI Calculator v2.0
FLASK_ENV=production
DEBUG=False
SECRET_KEY={secrets.token_urlsafe(32)}
HOST=0.0.0.0
PORT=5000
ENABLE_CORS=True
LOG_LEVEL=WARNING
CALCULATION_PRECISION=2
TERMUX_MODE=true
""")
    
    print("\n🎯 Configuration:")
    print("   • URL: http://localhost:5000")
    print("   • Mode: Termux-optimized with Quantum UI")
    print("   • Features: AI-powered insights, 3D animations")
    print("   • Calculations: Advanced financial modeling")
    print("\n⏳ Starting quantum server...")
    
    # Ensure we can import the app
    if not os.path.exists('app.py'):
        print("❌ app.py not found! Please run from the AppM directory:")
        print("   cd AppM && python3 run_termux.py")
        sys.exit(1)
    
    # Add current directory to Python path
    sys.path.insert(0, os.getcwd())
    
    # Import and run the main application
    try:
        from app import app, config_class, logger
        logger.info("Starting VoidSight Analytics v2.0 in Termux mode")
        
        # Try to use smart starter if available
        if os.path.exists('start_app.py'):
            print(f"\n🌟 Using smart port detection...")
            os.system('python3 start_app.py')
        else:
            # Fallback to manual port management
            import socket
        from contextlib import closing
        
        def find_free_port(start_port=5000):
            for port in range(start_port, start_port + 100):
                try:
                    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                        result = sock.connect_ex(('localhost', port))
                        if result != 0:
                            return port
                except:
                    continue
            return 5000
        
        port = find_free_port()
        
        print(f"\n👁️ VoidSight Analytics is starting...")
        print(f"📡 Using port: {port}")
        print(f"🌐 Open your browser and go to: http://localhost:{port}")
        print(f"📱 Or from other devices: http://YOUR_IP:{port}")
        print(f"\n🔮 VoidSight Features Available:")
        print(f"   • Spectral AI Intelligence")
        print(f"   • Phantom-Inspired UI with ethereal animations")
        print(f"   • Interactive void visualizations")
        print(f"   • Advanced financial modeling")
        print(f"   • Real-time spectral insights")
        print(f"   • See Beyond The Veil™")
        print(f"\nPress Ctrl+C to stop the server")
        print("=" * 60)
        
        app.run(
            debug=config_class.DEBUG,
            host=config_class.HOST,
            port=port,
            use_reloader=False  # Disable reloader for Termux stability
        )
    except KeyboardInterrupt:
        print("\n👋 VoidSight Analytics stopped")
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Make sure you're in the AppM directory:")
        print("   cd AppM && python3 run_termux.py")
        print("2. Or run the one-command installer:")
        print("   curl -fsSL https://raw.githubusercontent.com/bullsbears682/AppM/main/install.sh | bash")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("\n🔧 Quick fixes:")
        print("1. Install Flask: pip install --break-system-packages Flask")
        print("2. Try the one-command installer:")
        print("   curl -fsSL https://raw.githubusercontent.com/bullsbears682/AppM/main/install.sh | bash")
        print("3. Manual setup:")
        print("   pkg install git && git clone https://github.com/bullsbears682/AppM.git && cd AppM && python3 run_termux.py")
        sys.exit(1)

if __name__ == '__main__':
    main()