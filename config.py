"""
Xloockup Configuration
Developer: Latiful Hassan Zihan
Telegram: t.me/alwayszihan
"""

import os
from colorama import Fore, Style

# Project Info
PROJECT_NAME = "Xloockup"
DEVELOPER = "Latiful Hassan Zihan"
TELEGRAM = "t.me/alwayszihan"
VERSION = "1.1.0"

# API Configuration
TRUECALLER_SEARCH_URL = "https://search5-noneu.truecaller.com/v2/search"
TRUECALLER_BULK_SEARCH_URL = "https://search5-noneu.truecaller.com/v2/bulk"

# Updated Headers for better compatibility
HEADERS = {
    'User-Agent': 'Truecaller/12.45.7 (Android;10; samsung SM-G973F)',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/json; charset=UTF-8',
    'Connection': 'keep-alive',
    'clientId': 'a1i0k--f2b4046a6f199a1d4a7e7a7b7d9a5d8e0e8f2c3'
}

# File Paths
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Colors
COLORS = {
    'success': Fore.GREEN,
    'error': Fore.RED,
    'warning': Fore.YELLOW,
    'info': Fore.BLUE,
    'cyan': Fore.CYAN,
    'magenta': Fore.MAGENTA,
    'reset': Style.RESET_ALL
}

# Country Codes with proper formatting info
COUNTRY_CODES = {
    'BD': 'Bangladesh (+880)',
    'IN': 'India (+91)',
    'US': 'United States (+1)',
    'UK': 'United Kingdom (+44)',
    'AE': 'United Arab Emirates (+971)',
    'SA': 'Saudi Arabia (+966)',
    'PK': 'Pakistan (+92)',
    'CA': 'Canada (+1)',
    'AU': 'Australia (+61)',
    'SG': 'Singapore (+65)'
}

# Country specific number formats
COUNTRY_FORMATS = {
    'BD': {
        'example': '+8801712345678',
        'length': 14,
        'description': 'Bangladesh: +880 followed by 10 digits'
    },
    'IN': {
        'example': '+919876543210', 
        'length': 13,
        'description': 'India: +91 followed by 10 digits'
    },
    'US': {
        'example': '+12345678901',
        'length': 12,
        'description': 'USA: +1 followed by 10 digits'
    }
}
