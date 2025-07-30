#!/usr/bin/env python3
"""
Smart application starter that finds an available port automatically
"""

import socket
import os
import sys
from contextlib import closing

def find_free_port(start_port=5000, max_port=5100):
    """Find a free port starting from start_port"""
    for port in range(start_port, max_port):
        try:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                if result != 0:  # Port is free
                    return port
        except:
            continue
    return None

def get_local_ip():
    """Get local IP address"""
    try:
        # Connect to a remote address to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "127.0.0.1"

def main():
    """Main function to start the ROI calculator"""
    print("🚀 Infinex Quantum ROI Calculator - Smart Starter")
    print("=" * 60)
    
    # Find available port
    port = find_free_port()
    if not port:
        print("❌ Could not find an available port between 5000-5100")
        sys.exit(1)
    
    # Set environment variables
    os.environ['PORT'] = str(port)
    os.environ['HOST'] = '0.0.0.0'
    
    # Get local IP for network access
    local_ip = get_local_ip()
    
    print(f"🌟 Starting Quantum ROI Calculator...")
    print(f"📡 Found available port: {port}")
    print(f"🌐 Local Access:   http://localhost:{port}")
    print(f"📱 Network Access: http://{local_ip}:{port}")
    print()
    print("🧠 Quantum Features Available:")
    print("   • AI-Powered ARIA Assistant")
    print("   • Quantum-Inspired UI with 3D animations")
    print("   • Interactive data visualizations")
    print("   • Advanced financial modeling")
    print("   • Real-time insights and recommendations")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Import and start the Flask app
    try:
        from app import app, config_class
        app.run(
            debug=False,
            host='0.0.0.0',
            port=port,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n👋 Quantum ROI Calculator stopped")
    except ImportError as e:
        print(f"❌ Failed to import Flask app: {e}")
        print("Make sure you're in the correct directory with app.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()