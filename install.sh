#!/bin/bash

# 🚀 Infinex ROI Calculator - One-Command Termux Installer
# This script installs and runs the quantum ROI calculator on Termux

echo "🚀 Infinex ROI Calculator - Quantum Analytics Platform"
echo "================================================"
echo "📱 Termux One-Command Installation Starting..."
echo ""

# Update Termux packages
echo "📦 Updating Termux packages..."
pkg update -y && pkg upgrade -y

# Install required packages
echo "🔧 Installing Python and Git..."
pkg install python git -y

# Install pip if not available
echo "🐍 Setting up Python pip..."
pkg install python-pip -y

# Clone or update repository
if [ -d "AppM" ]; then
    echo "📂 Repository exists, updating..."
    cd AppM
    git pull origin main
else
    echo "📥 Cloning repository..."
    git clone https://github.com/bullsbears682/AppM.git
    cd AppM
fi

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --break-system-packages --no-cache-dir Flask==2.3.3 Werkzeug==2.3.7 requests==2.31.0 flask-cors==4.0.0 python-dotenv==1.0.0

# Try to install numpy (optional)
echo "🔢 Installing NumPy (optional for enhanced features)..."
pip install --break-system-packages --no-cache-dir numpy || echo "⚠️  NumPy installation failed - app will work with basic features"

# Create optimized .env file for Termux
echo "⚙️  Creating Termux configuration..."
cat > .env << EOL
# Termux Optimized Configuration
FLASK_ENV=development
DEBUG=True
SECRET_KEY=termux-quantum-key-change-in-production
HOST=0.0.0.0
PORT=5000
ENABLE_CORS=True
LOG_LEVEL=WARNING
CALCULATION_PRECISION=2
TERMUX_MODE=true
EOL

echo ""
echo "✅ Installation Complete!"
echo ""
echo "🌟 Starting Infinex Quantum ROI Calculator..."
echo "🌐 Open your browser and go to: http://localhost:5000"
echo "📱 Or access from other devices: http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "🧠 Features Available:"
echo "   • AI-Powered ARIA Assistant"
echo "   • Quantum-Inspired UI with 3D animations"
echo "   • Interactive data visualizations"
echo "   • Advanced financial modeling"
echo "   • Real-time insights and recommendations"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================================"
echo ""

# Start the application
python3 run_termux.py