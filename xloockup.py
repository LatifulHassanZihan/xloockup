#!/usr/bin/env python3
"""
XLOOCKUP - Truecaller Number Lookup Tool v2.0
Developer: Latiful Hassan Zihan
Telegram: t.me/alwayszihan
Powered by truecallerpy
"""

import sys
import json
import os
from colorama import init

# Initialize colorama
init(autoreset=True)

# Import project modules
from config import PROJECT_NAME, DEVELOPER, TELEGRAM, VERSION, COLORS, COUNTRY_CODES, check_installation
from utils import print_banner, print_message, clear_screen, save_results, load_results, display_result
from truecaller_api import TruecallerAPI

def check_dependencies():
    """Check if required packages are installed"""
    if not check_installation():
        print_message('error', "truecallerpy is not installed!")
        print_message('info', "Installing required packages...")
        os.system("pip install truecallerpy colorama")
        print_message('success', "Packages installed successfully!")
        print_message('info', "Please restart the application")
        sys.exit(1)

def show_menu():
    """Display main menu"""
    print(f"""
{COLORS['cyan']}=== {PROJECT_NAME} v{VERSION} ==={COLORS['reset']}
{COLORS['success']}1.{COLORS['reset']} Single Number Lookup
{COLORS['success']}2.{COLORS['reset']} Bulk Number Lookup  
{COLORS['success']}3.{COLORS['reset']} View Saved Results
{COLORS['success']}4.{COLORS['reset']} Country Codes
{COLORS['success']}5.{COLORS['reset']} Check API Status
{COLORS['success']}6.{COLORS['reset']} Set API Key
{COLORS['success']}7.{COLORS['reset']} Clear Screen
{COLORS['success']}8.{COLORS['reset']} Exit

{COLORS['info']}Developer: {DEVELOPER}
Telegram: {TELEGRAM}{COLORS['reset']}
{COLORS['warning']}Powered by truecallerpy API{COLORS['reset']}
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
    
    if result and 'error' not in result:
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
    successful = sum(1 for r in results.values() if r and 'error' not in r)
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
        print_message('error', "✗ API is not accessible. Check your API key and internet connection.")

def set_api_key():
    """Set custom API key"""
    print(f"\n{COLORS['warning']}=== SET API KEY ==={COLORS['reset']}")
    print_message('info', "Get your API key from Truecaller developer account")
    api_key = input(f"{COLORS['cyan']}Enter your API key: {COLORS['reset']}").strip()
    
    if api_key:
        api = TruecallerAPI()
        api.set_api_key(api_key)
        print_message('success', "API key updated! It will be used for this session.")
    else:
        print_message('error', "No API key provided!")

def main():
    """Main application loop"""
    # Check dependencies first
    check_dependencies()
    
    clear_screen()
    print_banner()
    
    while True:
        try:
            show_menu()
            choice = input(f"{COLORS['cyan']}Select option (1-8): {COLORS['reset']}").strip()
            
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
                set_api_key()
            elif choice == '7':
                clear_screen()
                print_banner()
            elif choice == '8':
                print_message('success', "Thank you for using Xloockup v2.0! - t.me/alwayszihan")
                break
            else:
                print_message('error', "Invalid choice! Please select 1-8.")
            
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
