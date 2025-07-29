#!/usr/bin/env python3
"""
Termux Quick Start - One Command ROI Calculator
Downloads and runs the entire Quantum ROI Calculator automatically
"""

import os
import sys
import subprocess
import urllib.request

def run_command(cmd, description):
    """Run a command with error handling"""
    print(f"🔧 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️  Warning: {description} failed, but continuing...")
        print(f"   Error: {result.stderr}")
    return result.returncode == 0

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    
    # Update packages
    run_command("pkg update -y", "Updating Termux packages")
    
    # Install essential packages
    packages = ["python", "git", "curl"]
    for package in packages:
        run_command(f"pkg install {package} -y", f"Installing {package}")
    
    # Install Python packages
    python_packages = [
        "Flask==2.3.3",
        "Werkzeug==2.3.7",
        "requests==2.31.0",
        "flask-cors==4.0.0",
        "python-dotenv==1.0.0"
    ]
    
    for package in python_packages:
        run_command(
            f"pip install --break-system-packages --no-cache-dir {package}",
            f"Installing {package}"
        )
    
    # Optional numpy
    run_command(
        "pip install --break-system-packages --no-cache-dir numpy",
        "Installing NumPy (optional)"
    )

def setup_application():
    """Setup the application directory and files"""
    print("📥 Setting up Quantum ROI Calculator...")
    
    # Create directory structure
    app_dir = "InfinexROI"
    if os.path.exists(app_dir):
        print(f"📂 Directory {app_dir} exists, updating...")
        os.chdir(app_dir)
        if os.path.exists('.git'):
            run_command("git pull origin main", "Updating repository")
        else:
            setup_from_github()
    else:
        os.makedirs(app_dir)
        os.chdir(app_dir)
        setup_from_github()

def setup_from_github():
    """Setup from GitHub repository"""
    print("📥 Downloading from GitHub...")
    
    # Try git clone first
    if run_command("git clone https://github.com/bullsbears682/AppM.git .", "Cloning repository"):
        print("✅ Repository cloned successfully")
        return
    
    # Fallback to direct file download
    print("📄 Git clone failed, downloading files directly...")
    
    files_to_download = {
        'app.py': 'https://raw.githubusercontent.com/bullsbears682/AppM/main/app.py',
        'config.py': 'https://raw.githubusercontent.com/bullsbears682/AppM/main/config.py',
        'run_termux.py': 'https://raw.githubusercontent.com/bullsbears682/AppM/main/run_termux.py',
        'templates/index.html': 'https://raw.githubusercontent.com/bullsbears682/AppM/main/templates/index.html',
        'utils/__init__.py': 'https://raw.githubusercontent.com/bullsbears682/AppM/main/utils/__init__.py',
        'utils/validators.py': 'https://raw.githubusercontent.com/bullsbears682/AppM/main/utils/validators.py',
        'utils/calculator.py': 'https://raw.githubusercontent.com/bullsbears682/AppM/main/utils/calculator.py',
        'utils/cache.py': 'https://raw.githubusercontent.com/bullsbears682/AppM/main/utils/cache.py',
        'utils/rate_limiter.py': 'https://raw.githubusercontent.com/bullsbears682/AppM/main/utils/rate_limiter.py',
        'utils/export.py': 'https://raw.githubusercontent.com/bullsbears682/AppM/main/utils/export.py',
    }
    
    # Create directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('utils', exist_ok=True)
    
    # Download files
    for filename, url in files_to_download.items():
        try:
            print(f"📄 Downloading {filename}...")
            urllib.request.urlretrieve(url, filename)
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")

def create_config():
    """Create optimized configuration"""
    config_content = """# Termux Quantum Configuration
FLASK_ENV=development
DEBUG=True
SECRET_KEY=termux-quantum-infinex-2024
HOST=0.0.0.0
PORT=5000
ENABLE_CORS=True
LOG_LEVEL=WARNING
CALCULATION_PRECISION=2
TERMUX_MODE=true
"""
    
    with open('.env', 'w') as f:
        f.write(config_content)
    print("⚙️  Configuration created")

def get_local_ip():
    """Get local IP address"""
    try:
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().split()[0]
    except:
        pass
    return "YOUR_DEVICE_IP"

def start_application():
    """Start the Quantum ROI Calculator"""
    print("\n🚀 Starting Infinex Quantum ROI Calculator...")
    
    # Add current directory to Python path
    sys.path.insert(0, os.getcwd())
    
    try:
        # Import and run
        from app import app, config_class
        
        local_ip = get_local_ip()
        
        print("\n" + "=" * 60)
        print("🌟 INFINEX QUANTUM ROI CALCULATOR")
        print("=" * 60)
        print(f"🌐 Local Access:   http://localhost:5000")
        print(f"📱 Network Access: http://{local_ip}:5000")
        print("\n🧠 Quantum Features Available:")
        print("   • AI-Powered ARIA Assistant")
        print("   • Quantum-Inspired UI with 3D animations")
        print("   • Interactive data visualizations")
        print("   • Advanced financial modeling")
        print("   • Real-time insights and recommendations")
        print("\n⚡ Performance Optimizations:")
        print("   • Termux-optimized configuration")
        print("   • Reduced resource usage")
        print("   • Mobile-first responsive design")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 60)
        
        app.run(
            debug=False,  # Disable debug for better performance
            host=config_class.HOST,
            port=config_class.PORT,
            use_reloader=False
        )
        
    except KeyboardInterrupt:
        print("\n👋 Quantum ROI Calculator stopped")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure all files downloaded correctly")
        print("2. Try running: python3 run_termux.py")
        print("3. Or use the full installer:")
        print("   curl -fsSL https://raw.githubusercontent.com/bullsbears682/AppM/main/install.sh | bash")

def main():
    """Main function"""
    print("🚀 INFINEX QUANTUM ROI CALCULATOR")
    print("🌟 One-Command Termux Setup")
    print("=" * 50)
    
    try:
        install_dependencies()
        setup_application()
        create_config()
        start_application()
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("\n🔧 Try the alternative installer:")
        print("curl -fsSL https://raw.githubusercontent.com/bullsbears682/AppM/main/install.sh | bash")

if __name__ == '__main__':
    main()