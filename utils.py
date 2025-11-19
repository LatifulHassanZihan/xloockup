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
║        Truecaller Number Lookup v2.0         ║
║           Powered by truecallerpy            ║
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
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', str(number))
    
    if not cleaned:
        return False, "Empty phone number"
    
    # Handle different formats
    if cleaned.startswith('01') and len(cleaned) == 11:
        # Bangladesh: 017... to +88017...
        cleaned = '+880' + cleaned[1:]
    elif cleaned.startswith('1') and len(cleaned) == 10:
        # Bangladesh: 1... to +8801...
        cleaned = '+8801' + cleaned
    elif cleaned.startswith('91') and len(cleaned) == 12:
        # India: 91... to +91...
        cleaned = '+' + cleaned
    elif not cleaned.startswith('+'):
        # Add + if missing
        cleaned = '+' + cleaned
    
    # Basic length validation
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
    if not result:
        print_message('error', f"No results received for {phone_number}")
        return
        
    if 'error' in result:
        print_message('error', f"Error: {result['error']}")
        return
    
    print(f"\n{COLORS['success']}=== XLOOCKUP RESULTS ==={COLORS['reset']}")
    print(f"{COLORS['info']}Phone: {COLORS['reset']}{phone_number}")
    
    # Extract data from truecallerpy response
    data = result.get('data', [{}])[0] if result.get('data') else {}
    
    # Name information
    name = data.get('name', 'Not Available')
    if name and name != 'Not Available':
        print(f"{COLORS['info']}Name: {COLORS['reset']}{name}")
    
    # Phone information
    if data.get('phones'):
        phone_info = data['phones'][0]
        carrier = phone_info.get('carrier', 'Not Available')
        number_type = phone_info.get('type', 'Not Available')
        
        print(f"{COLORS['info']}Carrier: {COLORS['reset']}{carrier}")
        print(f"{COLORS['info']}Type: {COLORS['reset']}{number_type}")
    
    # Address information
    if data.get('addresses'):
        address_info = data['addresses'][0]
        city = address_info.get('city', 'Not Available')
        country = address_info.get('countryCode', 'Not Available')
        
        if city and city != 'Not Available':
            print(f"{COLORS['info']}City: {COLORS['reset']}{city}")
        if country and country != 'Not Available':
            print(f"{COLORS['info']}Country: {COLORS['reset']}{country}")
    
    # Email information
    if data.get('internetAddresses'):
        for internet_addr in data['internetAddresses']:
            email = internet_addr.get('id', '')
            if '@' in email:
                print(f"{COLORS['info']}Email: {COLORS['reset']}{email}")
                break
    
    # Spam information
    spam_score = data.get('spamScore', 0)
    spam_type = data.get('spamType', 'Not Spam')
    
    if spam_score > 70:
        spam_status = f"{COLORS['error']}HIGH SPAM"
    elif spam_score > 40:
        spam_status = f"{COLORS['warning']}MEDIUM SPAM"
    else:
        spam_status = f"{COLORS['success']}CLEAN"
    
    print(f"{COLORS['info']}Spam Score: {COLORS['reset']}{spam_score} - {spam_status}")
    print(f"{COLORS['info']}Spam Type: {COLORS['reset']}{spam_type}")
    
    # Confidence score
    score = data.get('score', 0)
    if score > 80:
        score_color = COLORS['success']
    elif score > 60:
        score_color = COLORS['warning']
    else:
        score_color = COLORS['error']
    
    print(f"{COLORS['info']}Confidence: {score_color}{score}%{COLORS['reset']}")
    
    print(f"{COLORS['success']}{'='*40}{COLORS['reset']}")

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def format_phone_for_display(phone):
    """Format phone number for better display"""
    return phone
