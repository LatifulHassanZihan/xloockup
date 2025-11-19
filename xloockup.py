#!/usr/bin/env python3
"""
Xloockup - Truecaller Number Lookup Tool for Termux Android
Developer: Latiful Hassan Zihan
Telegram: t.me/alwayszihan

A comprehensive Python-based command-line tool for phone number intelligence
and caller identification using Truecaller's data infrastructure.
"""

import re
import sys
import json
import time
import requests
from datetime import datetime
from urllib.parse import quote
from typing import Dict, List, Optional, Any

# Third-party imports
try:
    from colorama import init, Fore, Style, Back
    import colorama
    from bs4 import BeautifulSoup
except ImportError as e:
    print("Required dependencies not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

# Local imports
from config import load_config, save_config, get_results_filename, HEADERS

# Initialize colorama for cross-platform terminal colors
init(autoreset=True)

class XloockupEngine:
    """
    Main engine for Truecaller number lookup operations
    """
    
    def __init__(self):
        self.config = load_config()
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.base_urls = [
            "https://www.truecaller.com",
            "https://search5.truecaller.com",
            "https://api4.truecaller.com"
        ]
        
    def validate_phone_number(self, phone_number: str) -> tuple:
        """
        Validate and clean phone number input
        Returns: (is_valid, cleaned_number, error_message)
        """
        # Remove any non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', phone_number.strip())
        
        if not cleaned:
            return False, "", "Phone number cannot be empty"
            
        # Check if number starts with + or has country code
        if cleaned.startswith('+'):
            if len(cleaned) < 8:
                return False, "", "Invalid international number format"
        else:
            # Add default country code if missing
            default_cc = self.config.get('default_country_code', 'BD')
            country_codes = {'BD': '880', 'US': '1', 'IN': '91', 'UK': '44'}
            if default_cc in country_codes:
                cleaned = country_codes[default_cc] + cleaned
        
        if len(cleaned) < 10:
            return False, "", "Phone number too short"
            
        if len(cleaned) > 15:
            return False, "", "Phone number too long"
            
        return True, cleaned, "Valid phone number"
    
    def lookup_single_number(self, phone_number: str) -> Dict[str, Any]:
        """
        Perform single number lookup with comprehensive data extraction
        """
        print(f"\n{Fore.YELLOW}🔍 Looking up: {phone_number}")
        
        # Validate input
        is_valid, cleaned_number, message = self.validate_phone_number(phone_number)
        if not is_valid:
            return {"error": message, "success": False}
        
        try:
            # Simulate API request (Note: This is a template structure)
            # In a real implementation, you would integrate with Truecaller's actual API
            # with proper authentication and legal compliance
            
            # This is a mock response structure for educational purposes
            mock_data = self._generate_mock_response(cleaned_number)
            
            # Add rate limiting
            time.sleep(self.config.get('rate_limit_delay', 2))
            
            return mock_data
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}", "success": False}
        except Exception as e:
            return {"error": f"Lookup failed: {str(e)}", "success": False}
    
    def _generate_mock_response(self, phone_number: str) -> Dict[str, Any]:
        """
        Generate mock response for demonstration purposes
        In real implementation, this would make actual API calls
        """
        # This is for educational demonstration only
        # Real implementation requires proper API access and legal compliance
        
        # Mock data structure
        country_codes = {
            '880': {'country': 'Bangladesh', 'code': 'BD'},
            '91': {'country': 'India', 'code': 'IN'}, 
            '1': {'country': 'United States', 'code': 'US'}
        }
        
        country_info = country_codes.get(phone_number[:3]) or country_codes.get(phone_number[:1]) or {'country': 'Unknown', 'code': 'XX'}
        
        return {
            "success": True,
            "data": {
                "phoneNumber": phone_number,
                "name": f"Demo User {phone_number[-4:]}",
                "carrier": "Demo Carrier",
                "country": country_info['country'],
                "countryCode": country_info['code'],
                "spamScore": 25,
                "spamType": "None",
                "imageUrl": None,
                "internetAddresses": [],
                "addresses": [],
                "confidence": 85,
                "lookupSource": "Xloockup Demo",
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def bulk_lookup(self, phone_numbers: List[str]) -> Dict[str, Any]:
        """
        Perform bulk number lookup with progress tracking
        """
        total = len(phone_numbers)
        results = []
        
        print(f"\n{Fore.CYAN}📊 Starting bulk lookup for {total} numbers...")
        
        for i, number in enumerate(phone_numbers, 1):
            print(f"{Fore.YELLOW}⏳ Processing {i}/{total}: {number}")
            
            result = self.lookup_single_number(number)
            results.append(result)
            
            # Progress indicator
            progress = (i / total) * 100
            print(f"{Fore.GREEN}✅ Completed: {progress:.1f}%")
            
            # Rate limiting between requests
            if i < total:
                time.sleep(self.config.get('rate_limit_delay', 2))
        
        return {
            "success": True,
            "total_processed": total,
            "successful_lookups": len([r for r in results if r.get('success')]),
            "failed_lookups": len([r for r in results if not r.get('success')]),
            "results": results
        }
    
    def save_lookup_results(self, results: Dict[str, Any], filename: str = None) -> bool:
        """
        Save lookup results to JSON file
        """
        if not self.config.get('save_results', True):
            return False
            
        try:
            if filename is None:
                filename = get_results_filename()
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"{Fore.GREEN}💾 Results saved to: {filename}")
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to save results: {str(e)}")
            return False
    
    def load_previous_results(self) -> List[str]:
        """
        Load list of previous result files
        """
        try:
            from config import RESULTS_DIR
            import os
            files = [f for f in os.listdir(RESULTS_DIR) if f.endswith('.json')]
            return sorted(files, reverse=True)
        except Exception:
            return []

class XloockupInterface:
    """
    User interface handler for terminal interaction
    """
    
    def __init__(self):
        self.engine = XloockupEngine()
        self.running = True
    
    def display_banner(self):
        """Display application banner"""
        banner = f"""
{Fore.CYAN + Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║                   {Fore.YELLOW}XLOOCKUP v1.0{Fore.CYAN}                          ║
║         Truecaller Number Lookup Tool for Termux            ║
║                                                              ║
║    Developer: {Fore.GREEN}Latiful Hassan Zihan{Fore.CYAN}                      ║
║    Telegram: {Fore.BLUE}t.me/alwayszihan{Fore.CYAN}                           ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
    
    def display_ethical_warning(self):
        """Display ethical usage warning"""
        warning = f"""
{Fore.RED + Style.BRIGHT}⚠️  ETHICAL USAGE WARNING ⚠️{Style.RESET_ALL}

{Fore.YELLOW}This tool is designed for:
• Personal contact identification
• Spam protection and analysis  
• Legitimate business verification

{Fore.RED}STRICTLY PROHIBITED:
• Harassment or stalking
• Unauthorized data collection
• Illegal surveillance
• Commercial misuse without permission

{Fore.GREEN}By using this tool, you agree to:
• Comply with local laws and regulations
• Respect privacy rights
• Use data responsibly and ethically
• Accept all legal responsibility for misuse
"""
        print(warning)
        input(f"{Fore.CYAN}Press Enter to continue or Ctrl+C to exit...")
    
    def display_number_info(self, result: Dict[str, Any]):
        """Display formatted number lookup results"""
        if not result.get('success'):
            print(f"{Fore.RED}❌ Lookup failed: {result.get('error', 'Unknown error')}")
            return
        
        data = result['data']
        
        print(f"\n{Fore.CYAN + Style.BRIGHT}📞 PHONE NUMBER INTELLIGENCE REPORT")
        print(f"{Fore.CYAN}═" * 50)
        
        # Basic Information
        print(f"{Fore.GREEN}📱 {Style.BRIGHT}Phone Number: {Fore.WHITE}{data['phoneNumber']}")
        print(f"{Fore.BLUE}👤 {Style.BRIGHT}Name: {Fore.WHITE}{data.get('name', 'Not Available')}")
        print(f"{Fore.MAGENTA}🏢 {Style.BRIGHT}Carrier: {Fore.WHITE}{data.get('carrier', 'Unknown')}")
        print(f"{Fore.YELLOW}🌍 {Style.BRIGHT}Country: {Fore.WHITE}{data.get('country', 'Unknown')} ({data.get('countryCode', 'XX')})")
        
        # Spam Analysis
        spam_score = data.get('spamScore', 0)
        spam_color = Fore.GREEN if spam_score < 30 else Fore.YELLOW if spam_score < 70 else Fore.RED
        print(f"{spam_color}🛡️  {Style.BRIGHT}Spam Score: {spam_color}{spam_score}%")
        print(f"{spam_color}📊 {Style.BRIGHT}Spam Type: {spam_color}{data.get('spamType', 'None')}")
        
        # Confidence and Metadata
        confidence = data.get('confidence', 0)
        conf_color = Fore.RED if confidence < 50 else Fore.YELLOW if confidence < 80 else Fore.GREEN
        print(f"{conf_color}🎯 {Style.BRIGHT}Confidence: {conf_color}{confidence}%")
        print(f"{Fore.CYAN}📡 {Style.BRIGHT}Source: {Fore.WHITE}{data.get('lookupSource', 'Unknown')}")
        print(f"{Fore.WHITE}🕒 {Style.BRIGHT}Timestamp: {Fore.WHITE}{data.get('timestamp', 'Unknown')}")
        
        print(f"{Fore.CYREEN}═" * 50)
    
    def single_lookup_menu(self):
        """Handle single number lookup"""
        print(f"\n{Fore.CYAN + Style.BRIGHT}🔍 SINGLE NUMBER LOOKUP")
        print(f"{Fore.CYAN}─" * 30)
        
        phone_number = input(f"{Fore.GREEN}📞 Enter phone number (with country code): {Style.RESET_ALL}").strip()
        
        if not phone_number:
            print(f"{Fore.RED}❌ No number entered!")
            return
        
        # Perform lookup
        result = self.engine.lookup_single_number(phone_number)
        
        # Display results
        self.display_number_info(result)
        
        # Save results if successful
        if result.get('success'):
            if input(f"\n{Fore.GREEN}💾 Save results? (y/N): {Style.RESET_ALL}").lower() == 'y':
                self.engine.save_lookup_results(result)
    
    def bulk_lookup_menu(self):
        """Handle bulk number lookup"""
        print(f"\n{Fore.CYAN + Style.BRIGHT}📊 BULK NUMBER LOOKUP")
        print(f"{Fore.CYAN}─" * 30)
        
        print(f"{Fore.YELLOW}Enter phone numbers (one per line, empty line to finish):")
        phone_numbers = []
        
        while True:
            number = input(f"{Fore.GREEN}📞 Number {len(phone_numbers) + 1}: {Style.RESET_ALL}").strip()
            if not number:
                break
            phone_numbers.append(number)
        
        if not phone_numbers:
            print(f"{Fore.RED}❌ No numbers entered!")
            return
        
        print(f"{Fore.CYAN}⏳ Processing {len(phone_numbers)} numbers...")
        
        # Perform bulk lookup
        results = self.engine.bulk_lookup(phone_numbers)
        
        # Display summary
        print(f"\n{Fore.GREEN + Style.BRIGHT}📈 BULK LOOKUP SUMMARY")
        print(f"{Fore.GREEN}─" * 40)
        print(f"{Fore.WHITE}✅ Successful: {Fore.GREEN}{results['successful_lookups']}")
        print(f"{Fore.WHITE}❌ Failed: {Fore.RED}{results['failed_lookups']}")
        print(f"{Fore.WHITE}📊 Total: {Fore.CYAN}{results['total_processed']}")
        
        # Save results
        if results['successful_lookups'] > 0:
            if input(f"\n{Fore.GREEN}💾 Save all results? (y/N): {Style.RESET_ALL}").lower() == 'y':
                self.engine.save_lookup_results(results)
    
    def view_history_menu(self):
        """Display previous lookup results"""
        previous_files = self.engine.load_previous_results()
        
        if not previous_files:
            print(f"{Fore.YELLOW}📭 No previous results found!")
            return
        
        print(f"\n{Fore.CYAN + Style.BRIGHT}📚 PREVIOUS RESULTS")
        print(f"{Fore.CYAN}─" * 40)
        
        for i, filename in enumerate(previous_files[:10], 1):
            print(f"{Fore.GREEN}{i}. {filename}")
        
        try:
            choice = input(f"\n{Fore.YELLOW}Enter file number to view (or Enter to cancel): {Style.RESET_ALL}").strip()
            if choice and choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(previous_files):
                    self.view_saved_results(previous_files[idx])
#!/usr/bin/env python3
"""
XLOOCKUP - Truecaller Number Lookup Tool
Developer: Latiful Hassan Zihan
Telegram: t.me/alwayszihan
"""

import sys
import json
import os
from colorama import init

# Initialize colorama
init(autoreset=True)

# Import project modules
from config import PROJECT_NAME, DEVELOPER, TELEGRAM, VERSION, COLORS, COUNTRY_CODES
from utils import print_banner, print_message, clear_screen, save_results, load_results, display_result
from truecaller_api import TruecallerAPI

def show_menu():
    """Display main menu"""
    print(f"""
{COLORS['cyan']}=== {PROJECT_NAME} v{VERSION} ==={COLORS['reset']}
{COLORS['success']}1.{COLORS['reset']} Single Number Lookup
{COLORS['success']}2.{COLORS['reset']} Bulk Number Lookup  
{COLORS['success']}3.{COLORS['reset']} View Saved Results
{COLORS['success']}4.{COLORS['reset']} Country Codes
{COLORS['success']}5.{COLORS['reset']} Clear Screen
{COLORS['success']}6.{COLORS['reset']} Exit

{COLORS['info']}Developer: {DEVELOPER}
Telegram: {TELEGRAM}{COLORS['reset']}
    """)

def single_lookup():
    """Handle single number lookup"""
    print(f"\n{COLORS['warning']}=== SINGLE NUMBER LOOKUP ==={COLORS['reset']}")
    
    phone_number = input(f"{COLORS['cyan']}Enter phone number: {COLORS['reset']}").strip()
    country_code = input(f"{COLORS['cyan']}Country code (IN, US, BD etc) [IN]: {COLORS['reset']}").strip().upper() or "IN"
    
    if not phone_number:
        print_message('error', "Phone number required!")
        return
    
    # Perform lookup
    api = TruecallerAPI()
    result = api.search_number(phone_number, country_code)
    
    if result:
        display_result(result, phone_number)
        
        # Save results
        save_choice = input(f"\n{COLORS['cyan']}Save results? (y/n): {COLORS['reset']}").lower()
        if save_choice in ['y', 'yes']:
            save_results(phone_number, result)

def bulk_lookup():
    """Handle bulk number lookup"""
    print(f"\n{COLORS['warning']}=== BULK NUMBER LOOKUP ==={COLORS['reset']}")
    
    print(f"{COLORS['info']}Enter phone numbers (one per line). Type 'done' to finish:{COLORS['reset']}")
    phone_numbers = []
    
    while True:
        try:
            number = input().strip()
            if number.lower() == 'done':
                break
            if number:
                phone_numbers.append(number)
        except KeyboardInterrupt:
            print_message('warning', "Input interrupted")
            break
    
    if not phone_numbers:
        print_message('error', "No numbers provided!")
        return
    
    country_code = input(f"{COLORS['cyan']}Country code (IN, US, BD etc) [IN]: {COLORS['reset']}").strip().upper() or "IN"
    
    # Perform bulk lookup
    api = TruecallerAPI()
    results = api.bulk_search(phone_numbers, country_code)
    
    # Display all results
    for number, result in results.items():
#!/usr/bin/env python3
"""
XLOOCKUP - Truecaller Number Lookup Tool
Developer: Latiful Hassan Zihan
Telegram: t.me/alwayszihan
"""

import sys
import json
import os
from colorama import init

# Initialize colorama
init(autoreset=True)

# Import project modules
from config import PROJECT_NAME, DEVELOPER, TELEGRAM, VERSION, COLORS, COUNTRY_CODES
from utils import print_banner, print_message, clear_screen, save_results, load_results, display_result
from truecaller_api import TruecallerAPI

def show_menu():
    """Display main menu"""
    print(f"""
{COLORS['cyan']}=== {PROJECT_NAME} v{VERSION} ==={COLORS['reset']}
{COLORS['success']}1.{COLORS['reset']} Single Number Lookup
{COLORS['success']}2.{COLORS['reset']} Bulk Number Lookup  
{COLORS['success']}3.{COLORS['reset']} View Saved Results
{COLORS['success']}4.{COLORS['reset']} Country Codes
{COLORS['success']}5.{COLORS['reset']} Check API Status
{COLORS['success']}6.{COLORS['reset']} Clear Screen
{COLORS['success']}7.{COLORS['reset']} Exit

{COLORS['info']}Developer: {DEVELOPER}
Telegram: {TELEGRAM}{COLORS['reset']}
    """)

def single_lookup():
    """Handle single number lookup"""
    print(f"\n{COLORS['warning']}=== SINGLE NUMBER LOOKUP ==={COLORS['reset']}")
    
    phone_number = input(f"{COLORS['cyan']}Enter phone number (with country code): {COLORS['reset']}").strip()
    country_code = input(f"{COLORS['cyan']}Country code (IN, US, BD etc) [IN]: {COLORS['reset']}").strip().upper() or "IN"
    
    if not phone_number:
        print_message('error', "Phone number required!")
        return
    
    if country_code not in COUNTRY_CODES:
        print_message('warning', f"Country code {country_code} not in list, but trying anyway...")
    
    api = TruecallerAPI()
    result = api.search_number(phone_number, country_code)
    
    if result:
        display_result(result, phone_number)
        save_choice = input(f"\n{COLORS['cyan']}Save results? (y/n): {COLORS['reset']}").lower()
        if save_choice in ['y', 'yes']:
            save_results(phone_number, result)
    else:
        print_message('error', "Lookup failed!")

def bulk_lookup():
    """Handle bulk number lookup"""
    print(f"\n{COLORS['warning']}=== BULK NUMBER LOOKUP ==={COLORS['reset']}")
    print(f"{COLORS['info']}Enter phone numbers (one per line). Type 'done' to finish:{COLORS['reset']}")
    print(f"{COLORS['warning']}Note: Bulk search may take time due to rate limiting{COLORS['reset']}")
    
    phone_numbers = []
    
    while True:
        try:
            number = input().strip()
            if number.lower() == 'done':
                break
            if number:
                phone_numbers.append(number)
        except KeyboardInterrupt:
            print_message('warning', "Input interrupted")
            break
    
    if not phone_numbers:
        print_message('error', "No numbers provided!")
        return
    
    if len(phone_numbers) > 10:
        print_message('warning', f"You entered {len(phone_numbers)} numbers. This may take a while.")
        confirm = input(f"{COLORS['cyan']}Continue? (y/n): {COLORS['reset']}").lower()
        if confirm not in ['y', 'yes']:
            return
    
    country_code = input(f"{COLORS['cyan']}Country code (IN, US, BD etc) [IN]: {COLORS['reset']}").strip().upper() or "IN"
    
    api = TruecallerAPI()
    results = api.bulk_search(phone_numbers, country_code)
    
    # Display summary
    successful = sum(1 for r in results.values() if 'error' not in r)
    failed = len(phone_numbers) - successful
    
    print(f"\n{COLORS['success']}=== BULK SEARCH SUMMARY ==={COLORS['reset']}")
    print(f"{COLORS['success']}Successful: {successful}{COLORS['reset']}")
    print(f"{COLORS['error']}Failed: {failed}{COLORS['reset']}")
    print(f"{COLORS['info']}Total: {len(phone_numbers)}{COLORS['reset']}")
    
    # Display all results
    for number, result in results.items():
        display_result(result, number)
    
    save_choice = input(f"\n{COLORS['cyan']}Save all results? (y/n): {COLORS['reset']}").lower()
    if save_choice in ['y', 'yes']:
        save_results("bulk_search", results, "bulk")

def view_saved_results():
    """View previously saved results"""
    files = load_results()
    
    if not files:
        print_message('warning', "No saved results found!")
        return
    
    print(f"\n{COLORS['warning']}=== SAVED RESULTS ({len(files)} files) ==={COLORS['reset']}")
    
    for i, filename in enumerate(files, 1):
        print(f"{COLORS['success']}{i}.{COLORS['reset']} {filename}")
    
    try:
        choice = input(f"\n{COLORS['cyan']}Select file to view (0 to cancel): {COLORS['reset']}").strip()
        if choice == '0':
            return
        
        selected_index = int(choice) - 1
        if 0 <= selected_index < len(files):
            selected_file = files[selected_index]
            filepath = os.path.join("results", selected_file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"\n{COLORS['success']}=== {selected_file} ==={COLORS['reset']}")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print_message('error', "Invalid selection!")
            
    except (ValueError, IndexError):
        print_message('error', "Invalid input!")
    except Exception as e:
        print_message('error', f"Error: {str(e)}")

def show_country_codes():
    """Display available country codes"""
    print(f"\n{COLORS['warning']}=== SUPPORTED COUNTRY CODES ==={COLORS['reset']}")
    for code, country in COUNTRY_CODES.items():
        print(f"{COLORS['success']}{code}:{COLORS['reset']} {country}")

def check_api_status():
    """Check if Truecaller API is accessible"""
    print(f"\n{COLORS['warning']}=== API STATUS CHECK ==={COLORS['reset']}")
    print_message('info', "Testing connection to Truecaller API...")
    
    api = TruecallerAPI()
    status = api.get_api_status()
    
    if status:
        print_message('success', "✓ API is accessible and working")
    else:
        print_message('error', "✗ API is not accessible. Check your internet connection.")

def main():
    """Main application loop"""
    clear_screen()
    print_banner()
    
    while True:
        try:
            show_menu()
            choice = input(f"{COLORS['cyan']}Select option (1-7): {COLORS['reset']}").strip()
            
            if choice == '1':
                single_lookup()
            elif choice == '2':
                bulk_lookup()
            elif choice == '3':
                view_saved_results()
            elif choice == '4':
                show_country_codes()
            elif choice == '5':
                check_api_status()
            elif choice == '6':
                clear_screen()
                print_banner()
            elif choice == '7':
                print_message('success', "Thank you for using Xloockup! - t.me/alwayszihan")
                break
            else:
                print_message('error', "Invalid choice! Please select 1-7.")
            
            input(f"\n{COLORS['cyan']}Press Enter to continue...{COLORS['reset']}")
            clear_screen()
            print_banner()
            
        except KeyboardInterrupt:
            print_message('warning', "\nOperation cancelled by user")
            break
        except Exception as e:
            print_message('error', f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 6):
        print("Python 3.6 or higher is required!")
        sys.exit(1)
    
    # Run main application
    main()
