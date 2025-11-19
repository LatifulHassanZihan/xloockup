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
        except Exception as e:
            print(f"{Fore.RED}❌ Error loading file: {str(e)}")
    
    def view_saved_results(self, filename: str):
        """View specific saved results file"""
        try:
            from config import RESULTS_DIR
            filepath = os.path.join(RESULTS_DIR, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"\n{Fore.GREEN + Style.BRIGHT}📄 VIEWING: {filename}")
            
            if 'results' in data:  # Bulk results
                for result in data['results']:
                    if result.get('success'):
                        self.display_number_info(result)
                        print()
            else:  # Single result
                self.display_number_info(data)
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error reading file: {str(e)}")
    
    def settings_menu(self):
        """Display and modify settings"""
        print(f"\n{Fore.CYAN + Style.BRIGHT}⚙️  SETTINGS")
        print(f"{Fore.CYAN}─" * 30)
        
        print(f"{Fore.GREEN}1. Default Country Code: {self.engine.config.get('default_country_code', 'BD')}")
        print(f"{Fore.GREEN}2. Rate Limit Delay: {self.engine.config.get('rate_limit_delay', 2)}s")
        print(f"{Fore.GREEN}3. Auto-save Results: {'Yes' if self.engine.config.get('save_results', True) else 'No'}")
        
        choice = input(f"\n{Fore.YELLOW}Select setting to change (1-3) or Enter to cancel: {Style.RESET_ALL}").strip()
        
        if choice == '1':
            new_cc = input(f"{Fore.GREEN}Enter new default country code (BD/US/IN/UK): {Style.RESET_ALL}").strip().upper()
            if new_cc in ['BD', 'US', 'IN', 'UK']:
                self.engine.config['default_country_code'] = new_cc
                save_config(self.engine.config)
                print(f"{Fore.GREEN}✅ Country code updated!")
        
        elif choice == '2':
            try:
                new_delay = float(input(f"{Fore.GREEN}Enter new rate limit delay (seconds): {Style.RESET_ALL}"))
                if 1 <= new_delay <= 10:
                    self.engine.config['rate_limit_delay'] = new_delay
                    save_config(self.engine.config)
                    print(f"{Fore.GREEN}✅ Rate limit delay updated!")
                else:
                    print(f"{Fore.RED}❌ Delay must be between 1-10 seconds!")
            except ValueError:
                print(f"{Fore.RED}❌ Invalid number!")
        
        elif choice == '3':
            self.engine.config['save_results'] = not self.engine.config.get('save_results', True)
            save_config(self.engine.config)
            state = "enabled" if self.engine.config['save_results'] else "disabled"
            print(f"{Fore.GREEN}✅ Auto-save {state}!")
    
    def main_menu(self):
        """Display main menu and handle user input"""
        while self.running:
            print(f"\n{Fore.CYAN + Style.BRIGHT}🏠 XLOOCKUP MAIN MENU")
            print(f"{Fore.CYAN}═" * 40)
            print(f"{Fore.GREEN}1. {Style.BRIGHT}🔍 Single Number Lookup")
            print(f"{Fore.BLUE}2. {Style.BRIGHT}📊 Bulk Number Lookup") 
            print(f"{Fore.YELLOW}3. {Style.BRIGHT}📚 View Previous Results")
            print(f"{Fore.MAGENTA}4. {Style.BRIGHT}⚙️  Settings")
            print(f"{Fore.RED}5. {Style.BRIGHT}🚪 Exit")
            print(f"{Fore.CYAN}═" * 40)
            
            choice = input(f"\n{Fore.YELLOW}Select option (1-5): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                self.single_lookup_menu()
            elif choice == '2':
                self.bulk_lookup_menu()
            elif choice == '3':
                self.view_history_menu()
            elif choice == '4':
                self.settings_menu()
            elif choice == '5':
                print(f"\n{Fore.GREEN}👋 Thank you for using Xloockup!")
                print(f"{Fore.CYAN}Developer: Latiful Hassan Zihan")
                print(f"{Fore.BLUE}Telegram: t.me/alwayszihan")
                self.running = False
            else:
                print(f"{Fore.RED}❌ Invalid option! Please choose 1-5.")
    
    def run(self):
        """Main application runner"""
        try:
            self.display_banner()
            self.display_ethical_warning()
            self.main_menu()
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}⚠️  Operation cancelled by user.")
            print(f"{Fore.GREEN}👋 Thank you for using Xloockup!")
        except Exception as e:
            print(f"\n{Fore.RED}❌ Unexpected error: {str(e)}")
            print(f"{Fore.YELLOW}📧 Please report issues to: t.me/alwayszihan")

def main():
    """Application entry point"""
    # Check dependencies
    try:
        import requests
        from colorama import init
        init()  # Initialize colorama
    except ImportError as e:
        print(f"{Fore.RED}❌ Missing dependencies. Please run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Create and run application
    app = XloockupInterface()
    app.run()

if __name__ == "__main__":
    main()
