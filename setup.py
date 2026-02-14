#!/usr/bin/env python3
"""
Setup script for PortScan Pro
Author: Devansh Kuwadiya
"""

import subprocess
import sys
import os

def print_banner():
    print("""
    ╔═══════════════════════════════════════════╗
    ║   🔍 PortScan Pro - Installation Setup   ║
    ║          Version 2.1.0                    ║
    ╚═══════════════════════════════════════════╝
    """)

def install_dependencies():
    print("\n📦 Installing dependencies...\n")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("\n✅ Installation complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: {e}")
        return False

def create_directories():
    print("\n📁 Creating directories...")
    for directory in ['data', 'logs', 'exports']:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ {directory}/")
    return True

def main():
    print_banner()
    
    if not create_directories():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    print("\n" + "="*50)
    print("🎉 Setup Complete!")
    print("="*50)
    print("\nRun the application:")
    print("  python main.py")
    print("\n⚠️  Only scan networks you own!")
    print("="*50)

if __name__ == "__main__":
    main()