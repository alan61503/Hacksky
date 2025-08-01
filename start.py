#!/usr/bin/env python3
"""
Hacksky - Startup Script
A simple script to start both the backend and frontend servers.
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

def print_banner():
    """Print the Hacksky banner."""
    print("=" * 60)
    print("🚀 HACKSKY - Instagram Clone with AI Misinformation Detection")
    print("=" * 60)
    print("Starting servers...")
    print()

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        print("✅ Backend dependencies found")
        return True
    except ImportError:
        print("❌ Backend dependencies not found")
        print("Please install dependencies:")
        print("   cd backend && pip install -r requirements.txt")
        return False

def start_backend():
    """Start the FastAPI backend server."""
    try:
        print("🔧 Starting backend server...")
        os.chdir("backend")
        subprocess.run([sys.executable, "run.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

def start_frontend():
    """Start the frontend HTTP server."""
    try:
        print("🌐 Starting frontend server...")
        os.chdir("frontend")
        subprocess.run([sys.executable, "-m", "http.server", "8080"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

def main():
    """Main startup function."""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Get current directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("📋 Starting servers in separate threads...")
    print("   Backend: http://localhost:8000")
    print("   Frontend: http://localhost:8080")
    print("   API Docs: http://localhost:8000/docs")
    print()
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend in a separate thread
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    frontend_thread.start()
    
    # Wait a moment for frontend to start
    time.sleep(2)
    
    # Open browser
    try:
        print("🌐 Opening browser...")
        webbrowser.open("http://localhost:8080")
    except:
        print("⚠️ Could not open browser automatically")
        print("   Please open: http://localhost:8080")
    
    print()
    print("🎉 Hacksky is running!")
    print("   Press Ctrl+C to stop all servers")
    print()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Hacksky...")
        print("✅ All servers stopped")

if __name__ == "__main__":
    main() 