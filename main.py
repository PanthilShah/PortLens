#!/usr/bin/env python3
"""
PortScan Pro - Advanced Network Security Scanner
Version 2.1.0

Author: Devansh Kuwadiya
License: MIT
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import PortScannerGUI

def main():
    """Main entry point"""
    try:
        app = PortScannerGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()