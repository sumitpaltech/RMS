#!/usr/bin/env python
"""
Application Entry Point
Use: python run.py
"""
from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=7001, debug=True)
