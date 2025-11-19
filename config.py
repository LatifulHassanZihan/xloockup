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
VERSION = "2.0.0"

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
    'BD': 'Bangladesh',
    'IN': 'India',
    'US': 'United States',
    'UK': 'United Kingdom',
    'AE': 'United Arab Emirates',
    'SA': 'Saudi Arabia',
    'PK': 'Pakistan',
    'CA': 'Canada',
    'AU': 'Australia',
    'SG': 'Singapore'
}

# Installation check
def check_installation():
    """Check if truecallerpy is installed"""
    try:
        from truecallerpy import search_phonenumber
        return True
    except ImportError:
        return False
