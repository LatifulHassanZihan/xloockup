"""
Utility Functions for Xloockup
"""

import json
import os
import re
from datetime import datetime
from colorama import Fore, Style, init
from config import COLORS, RESULTS_DIR

# Initialize colorama
init(autoreset=True)

def print_banner():
    banner = f"""
{COLORS['cyan']}
╔══════════════════════════════════════════════╗
║                  {COLORS['magenta']}XLOOCKUP{COLORS['cyan']}                   ║
║           Truecaller Number Lookup           ║
║           Developer: Latiful Hassan Zihan    ║
║           Telegram: t.me/alwayszihan         ║
╚══════════════════════════════════════════════╝
{COLORS['reset']}
"""
    print(banner)

def print_message(message_type, message):
    colors = {
        'success': COLORS['success'],
        'error': COLORS['error'],
        'warning': COLORS['warning'],
        'info': COLORS['info']
    }
    symbols = {
        'success': '[✓]',
        'error': '[✗]',
        'warning': '[!]',
        'info': '[i]'
    }
    print(f"{colors[message_type]}{symbols[message_type]} {message}{COLORS['reset']}")

def validate_phone_number(number):
    """Validate and clean phone number"""
    cleaned = re.sub(r'[^\d+]', '', str(number))
    
    if not cleaned:
        return False, "Empty phone number"
    
    if not cleaned.startswith('+'):
        cleaned = '+' + cleaned
    
    if len(cleaned) < 10:
        return False, "Phone number too short"
    
    return True, cleaned

def save_results(phone_number, data, search_type="single"):
    """Save lookup results to JSON file"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if search_type == "single":
            clean_phone = re.sub(r'[^\w]', '_', phone_number)
            filename = f"xloockup_{clean_phone}_{timestamp}.json"
        else:
            filename = f"xloockup_bulk_{timestamp}.json"
        
        filepath = os.path.join(RESULTS_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print_message('success', f"Results saved to: {filepath}")
        return filepath
    except Exception as e:
        print_message('error', f"Failed to save results: {str(e)}")
        return None

def load_results():
    """Load all saved results files"""
    try:
        if not os.path.exists(RESULTS_DIR):
            return []
        
        files = [f for f in os.listdir(RESULTS_DIR) if f.endswith('.json')]
        return sorted(files, reverse=True)
    except Exception as e:
        print_message('error', f"Failed to load results: {str(e)}")
        return []

def display_result(result, phone_number):
    """Display lookup results in formatted way"""
    if not result or 'error' in result:
        print_message('error', f"No results found for {phone_number}")
        return
    
    print(f"\n{COLORS['success']}=== XLOOCKUP RESULTS ==={COLORS['reset']}")
    print(f"{COLORS['info']}Phone: {COLORS['reset']}{phone_number}")
    
    fields = {
        'name': 'Name',
        'carrier': 'Carrier',
        'type': 'Type',
        'address': 'Location',
        'country': 'Country',
        'email': 'Email',
        'spam_score': 'Spam Score',
        'score': 'Confidence Score',
        'spam_type': 'Spam Type'
    }
    
    for key, display_name in fields.items():
        if key in result and result[key]:
            if key == 'spam_score':
                spam_score = result[key]
                if spam_score > 70:
                    spam_status = f"{COLORS['error']}HIGH SPAM"
                elif spam_score > 40:
                    spam_status = f"{COLORS['warning']}MEDIUM SPAM"
                else:
                    spam_status = f"{COLORS['success']}CLEAN"
                print(f"{COLORS['info']}{display_name}: {COLORS['reset']}{spam_score} - {spam_status}")
            elif key == 'score':
                score = result[key]
                if score > 80:
                    score_color = COLORS['success']
                elif score > 60:
                    score_color = COLORS['warning']
                else:
                    score_color = COLORS['error']
                print(f"{COLORS['info']}{display_name}: {score_color}{score}{COLORS['reset']}")
            else:
                print(f"{COLORS['info']}{display_name}: {COLORS['reset']}{result[key]}")
    
    print(f"{COLORS['success']}{'='*40}{COLORS['reset']}")

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')
