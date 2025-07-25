#!/usr/bin/env python3
"""
Enhanced Business ROI Calculator - Startup Script
Improved version with better error handling and logging
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        logger.error("Python 3.7 or higher is required")
        return False
    logger.info(f"Python version: {sys.version}")
    return True

def check_requirements():
    """Check if required packages are installed"""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        logger.error("requirements.txt not found")
        return False
    
    try:
        # Check if Flask is available
        import flask
        logger.info(f"✅ Flask {flask.__version__} is installed")
        
        # Check if numpy is available (new requirement)
        try:
            import numpy
            logger.info(f"✅ NumPy {numpy.__version__} is installed")
        except ImportError:
            logger.warning("NumPy not found. Installing requirements...")
            install_requirements()
            
        return True
        
    except ImportError:
        logger.warning("Flask not found. Installing requirements...")
        return install_requirements()

def install_requirements():
    """Install requirements from requirements.txt"""
    try:
        logger.info("Installing Python dependencies...")
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True, check=True)
        
        logger.info("✅ Requirements installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install requirements: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error during installation: {e}")
        return False

def check_enhanced_files():
    """Check if enhanced application files exist"""
    required_files = [
        'config.py',
        'utils.py',
        'models.py',
        'app_enhanced.py',
        'templates/index_enhanced.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        logger.warning(f"Enhanced files missing: {missing_files}")
        logger.info("Falling back to original application...")
        return False
    
    logger.info("✅ All enhanced application files found")
    return True

def create_log_directory():
    """Create logs directory if it doesn't exist"""
    log_dir = Path("logs")
    if not log_dir.exists():
        log_dir.mkdir()
        logger.info("Created logs directory")

def display_startup_info():
    """Display startup information"""
    print("=" * 60)
    print("🚀 ENHANCED BUSINESS ROI CALCULATOR")
    print("=" * 60)
    print("✨ Features:")
    print("   🎯 Advanced Financial Modeling")
    print("   📊 Monte Carlo Simulation")
    print("   🛡️  Comprehensive Risk Assessment")
    print("   🌍 Multi-Currency Support")
    print("   🧠 AI-Powered Market Insights")
    print("   📱 Responsive Design")
    print("   🔒 Enhanced Security & Validation")
    print()

def get_app_config():
    """Get application configuration from environment"""
    config = {
        'host': os.environ.get('HOST', '0.0.0.0'),
        'port': int(os.environ.get('PORT', 5000)),
        'debug': os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 'yes'],
        'env': os.environ.get('FLASK_ENV', 'development')
    }
    return config

def main():
    """Main startup function"""
    try:
        display_startup_info()
        
        # Check Python version
        if not check_python_version():
            sys.exit(1)
        
        # Check and install requirements
        if not check_requirements():
            logger.error("Failed to install requirements")
            sys.exit(1)
        
        # Create necessary directories
        create_log_directory()
        
        # Get configuration
        config = get_app_config()
        
        logger.info("🌐 Starting Enhanced ROI Calculator...")
        logger.info(f"📊 Environment: {config['env']}")
        logger.info(f"🔧 Debug mode: {config['debug']}")
        logger.info(f"🌍 Server: http://{config['host']}:{config['port']}")
        logger.info("🎯 Ready to calculate ROI for any business project!")
        print("=" * 60)
        
        # Try to use enhanced application first
        if check_enhanced_files():
            logger.info("🚀 Loading Enhanced Application...")
            try:
                from app_enhanced import app
                app.run(
                    host=config['host'],
                    port=config['port'],
                    debug=config['debug']
                )
            except Exception as e:
                logger.error(f"Enhanced application failed: {e}")
                logger.info("Falling back to original application...")
                fallback_to_original(config)
        else:
            fallback_to_original(config)
            
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down gracefully...")
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        sys.exit(1)

def fallback_to_original(config):
    """Fallback to original application if enhanced version fails"""
    try:
        logger.info("🔄 Loading Original Application...")
        from app import app
        app.run(
            host=config['host'],
            port=config['port'],
            debug=config['debug']
        )
    except Exception as e:
        logger.error(f"❌ Original application also failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()