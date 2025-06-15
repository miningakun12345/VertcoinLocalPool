#!/usr/bin/env python3
"""
Simple entry point for P2Pool Vertcoin
Convenience wrapper around main.py
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run main
from main import main

if __name__ == '__main__':
    main()
