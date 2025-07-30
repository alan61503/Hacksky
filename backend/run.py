#!/usr/bin/env python3
"""
Simple script to run the FastAPI backend server.
"""

import sys
import os
import uvicorn

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Start the FastAPI server."""
    try:
        from backend.config import API_HOST, API_PORT, DEBUG
        
        print("🚀 Starting Autonomous AI Misinformation Detection Engine")
        print(f"📍 Host: {API_HOST}")
        print(f"🔌 Port: {API_PORT}")
        print(f"🐛 Debug: {DEBUG}")
        print("=" * 60)
        
        # Start the server
        uvicorn.run(
            "backend.main:app",
            host=API_HOST,
            port=API_PORT,
            reload=DEBUG,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you have installed all dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 