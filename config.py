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
VERSION = "1.0.0"

# API Configuration
TRUECALLER_SEARCH_URL = "https://search5-noneu.truecaller.com/v2/search"
TRUECALLER_BULK_SEARCH_URL = "https://search5-noneu.truecaller.com/v2/bulk"

# Headers
HEADERS = {
    'User-Agent': 'Truecaller/12.45.7 (Android;10)',
    'Accept': 'application/json',
    'Accept-Language': 'en-US',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer a1i0k--f2b4046a6f199a1d4a7e7a7b7d9a5d8e0e8f2c3'
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

# Country Codes
COUNTRY_CODES = {
    'IN': 'India',
    'US': 'United States',
    'BD': 'Bangladesh',
    'UK': 'United Kingdom',
    'AE': 'United Arab Emirates',
    'SA': 'Saudi Arabia',
    'PK': 'Pakistan'
}
