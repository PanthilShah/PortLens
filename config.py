"""
Configuration settings for Portlens
Author: Panthil Shah
"""

import os

# Application Settings
APP_NAME = "PortLens"
APP_VERSION = "1.0"
APP_AUTHOR = "Panthil Shah"
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# Scanning Settings
DEFAULT_TIMEOUT = 1.5
MAX_THREADS = 100
DEFAULT_THREADS = 50
COMMON_PORTS_LIMIT = 1000

# Network Settings
DEFAULT_SCAN_TYPE = "TCP"
SCAN_TYPES = ["TCP", "UDP", "COMPREHENSIVE"]

# Color Scheme
COLORS = {
    'primary': '#1a1a2e',
    'secondary': '#16213e',
    'accent': '#0f3460',
    'success': '#00ff88',
    'warning': '#ffd700',
    'danger': '#ff4444',
    'info': '#00d4ff',
    'text': '#e0e0e0',
    'text_secondary': '#a0a0a0',
    'background': '#0a0a15',
    'card': '#1e1e30',
    'hover': '#252540'
}

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
EXPORTS_DIR = os.path.join(BASE_DIR, 'exports')

# Create directories if they don't exist
for directory in [DATA_DIR, LOGS_DIR, EXPORTS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Port Ranges
WELL_KNOWN_PORTS = (1, 1023)
REGISTERED_PORTS = (1024, 49151)
DYNAMIC_PORTS = (49152, 65535)

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"