#!/bin/bash

# INFINEX ROI CALCULATOR - TERMUX SETUP SCRIPT
# Complete installation and configuration for Termux/Android

set -e  # Exit on any error

echo "🚀 Infinex ROI Calculator - Termux Setup"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in Termux
if [ ! -d "$PREFIX" ]; then
    print_error "This script is designed for Termux. Please run it in Termux."
    exit 1
fi

print_info "Detected Termux environment: $PREFIX"

# Update package list
print_info "Updating package list..."
pkg update -y

# Install required system packages
print_info "Installing system packages..."
pkg install -y python python-pip git wget curl build-essential libffi openssl

# Verify Python installation
python_version=$(python --version 2>&1)
print_status "Python installed: $python_version"

# Setup storage permissions
print_info "Setting up storage permissions..."
termux-setup-storage

# Create app directory if it doesn't exist
APP_DIR="$HOME/infinex-roi"
if [ ! -d "$APP_DIR" ]; then
    mkdir -p "$APP_DIR"
fi

cd "$APP_DIR"

# Clean up existing installation
if [ -d "AppM" ]; then
    print_warning "Existing installation found. Backing up..."
    mv AppM "AppM.backup.$(date +%Y%m%d_%H%M%S)" 2>/dev/null || true
fi

# Clone the repository
print_info "Cloning Infinex ROI Calculator..."
git clone https://github.com/bullsbears682/AppM.git
cd AppM

# Setup environment
print_info "Setting up environment configuration..."
if [ -f ".env.termux" ]; then
    cp .env.termux .env
    print_status "Termux environment configuration applied"
else
    print_warning ".env.termux not found, creating basic configuration..."
    cat > .env << EOF
FLASK_ENV=development
FLASK_APP=app.py
DEBUG=true
HOST=0.0.0.0
PORT=5000
SECRET_KEY=termux-demo-secret-key
DATABASE_URL=sqlite:///infinex_roi.db
ENABLE_USER_AUTHENTICATION=false
ENABLE_ADVANCED_ANALYTICS=true
EOF
fi

# Upgrade pip
print_info "Upgrading pip..."
python -m pip install --upgrade pip

# Install Python dependencies
print_info "Installing Python dependencies..."
if [ -f "requirements-termux.txt" ]; then
    print_info "Using Termux-optimized requirements..."
    pip install -r requirements-termux.txt
else
    print_warning "Termux requirements not found, installing core dependencies..."
    pip install flask flask-cors numpy pandas scipy python-dotenv requests matplotlib
fi

# Create necessary directories
print_info "Creating application directories..."
mkdir -p logs uploads static/css static/js static/images

# Set up database
print_info "Setting up database..."
python -c "
import sys
sys.path.append('.')
try:
    from models import init_db
    from app import create_app
    app = create_app()
    with app.app_context():
        init_db(app)
    print('✅ Database initialized successfully')
except Exception as e:
    print(f'⚠️  Database setup skipped: {e}')
"

# Create startup script
print_info "Creating startup script..."
cat > start.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"

echo "🌟 Starting Infinex ROI Calculator..."
echo "=================================="

# Find available port
PORT=5000
while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
    PORT=$((PORT + 1))
done

export PORT=$PORT

# Get local IP
LOCAL_IP=$(ip route get 1.1.1.1 | awk '{print $7; exit}' 2>/dev/null || echo "localhost")

echo "📡 Port: $PORT"
echo "🌐 Local: http://localhost:$PORT"
echo "📱 Network: http://$LOCAL_IP:$PORT"
echo ""
echo "🧠 Features Available:"
echo "   • Quantum-Inspired UI with 3D animations"
echo "   • Advanced ROI calculations and analytics"
echo "   • Interactive charts and visualizations"
echo "   • Multi-industry analysis (17 sectors)"
echo "   • Real-time insights and recommendations"
echo ""
echo "Press Ctrl+C to stop"
echo "=================================="

# Use the smart starter if available, otherwise basic Flask
if [ -f "start_app.py" ]; then
    python start_app.py
else
    python app.py
fi
EOF

chmod +x start.sh

# Create quick launch script
print_info "Creating quick launch script..."
cat > "$HOME/../usr/bin/infinex" << EOF
#!/bin/bash
cd "$APP_DIR/AppM"
./start.sh
EOF
chmod +x "$HOME/../usr/bin/infinex"

# Test basic functionality
print_info "Testing basic functionality..."
python -c "
import flask
import numpy
import pandas
print('✅ Core dependencies working')
"

# Setup complete
echo ""
print_status "🎉 SETUP COMPLETE!"
echo ""
echo -e "${PURPLE}📋 QUICK START GUIDE:${NC}"
echo ""
echo -e "${CYAN}1. Start the application:${NC}"
echo "   cd $APP_DIR/AppM"
echo "   ./start.sh"
echo ""
echo -e "${CYAN}2. Alternative quick start (from anywhere):${NC}"
echo "   infinex"
echo ""
echo -e "${CYAN}3. Open in browser:${NC}"
echo "   http://localhost:5000"
echo ""
echo -e "${PURPLE}🌟 FEATURES AVAILABLE:${NC}"
echo "   • Beautiful Quantum-inspired UI"
echo "   • Advanced ROI calculations"
echo "   • 17 industry-specific analyses"
echo "   • Interactive charts and graphs"
echo "   • Multi-currency support"
echo "   • Professional export capabilities"
echo ""
echo -e "${PURPLE}💡 TIPS:${NC}"
echo "   • The app will auto-find available ports"
echo "   • Access from other devices using your IP"
echo "   • All data is stored locally in SQLite"
echo "   • Calculation results persist between sessions"
echo ""
echo -e "${GREEN}🚀 Ready to calculate ROI like a pro!${NC}"
echo ""
EOF