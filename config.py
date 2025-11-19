#!/usr/bin/env python3
"""
Xloockup - Configuration Module
Developer: Latiful Hassan Zihan
Telegram: t.me/alwayszihan
"""

import os
import json
from datetime import datetime

# Base paths for Termux Android
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "xloockup_data")
RESULTS_DIR = os.path.join(DATA_DIR, "results")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

# Create necessary directories
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Default configuration
DEFAULT_CONFIG = {
    "api_timeout": 30,
    "max_retries": 3,
    "rate_limit_delay": 2,
    "default_country_code": "BD",
    "save_results": True,
    "session_data": {}
}

# Mobile-optimized headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

def load_config():
    """Load configuration from file"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
    except Exception:
        pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception:
        return False

def get_results_filename():
    """Generate results filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(RESULTS_DIR, f"lookup_results_{timestamp}.json")
