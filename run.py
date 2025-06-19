#!/usr/bin/env python3
"""
Simple run script for ClassForge development
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import and run the application
from app import create_app

if __name__ == '__main__':
    app = create_app()
    
    # Default configuration for development
    host = os.environ.get('HOST', '0.0.0.0')  # Changed for cloud deployment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    print(f"🚀 Starting ClassForge on http://{host}:{port}")
    print("📚 AI-Powered Educational Assistant")
    print("=" * 50)
    
    app.run(host=host, port=port, debug=debug) 