"""
Truecaller API Handler for Xloockup using truecallerpy
"""

import time
from truecallerpy import search_phonenumber
from utils import print_message, validate_phone_number
from config import COUNTRY_CODES

class TruecallerAPI:
    def __init__(self):
        self.request_count = 0
        # You need to get this from Truecaller developer account
        self.api_key = "a1i0k--f2b4046a6f199a1d4a7e7a7b7d9a5d8e0e8f2c3"
    
    def search_number(self, phone_number, country_code="IN"):
        """
        Search phone number using truecallerpy API
        """
        try:
            is_valid, cleaned_number = validate_phone_number(phone_number)
            if not is_valid:
                print_message('error', f"Invalid phone number: {cleaned_number}")
                return None
            
            country_name = COUNTRY_CODES.get(country_code, country_code)
            print_message('info', f"Searching: {cleaned_number} ({country_name})")
            
            # Rate limiting
            self.request_count += 1
            if self.request_count % 3 == 0:
                print_message('warning', "Rate limiting - waiting 2 seconds...")
                time.sleep(2)
            
            # Use truecallerpy to search
            print_message('info', "Using truecallerpy API...")
            
            response = search_phonenumber(
                cleaned_number, 
                country_code, 
                self.api_key
            )
            
            if response and 'data' in response:
                if response['data']:
                    print_message('success', "Lookup successful!")
                    return response
                else:
                    print_message('error', "No data found for this number")
                    return {"error": "No data found in Truecaller database"}
            else:
                print_message('error', "API returned empty response")
                return {"error": "Empty response from Truecaller API"}
                
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower():
                print_message('error', "API quota exceeded - try again later")
                return {"error": "API quota exceeded"}
            elif "invalid" in error_msg.lower():
                print_message('error', "Invalid API key or parameters")
                return {"error": "Invalid API request"}
            elif "not found" in error_msg.lower():
                print_message('error', "Number not found in database")
                return {"error": "Number not found"}
            else:
                print_message('error', f"API Error: {error_msg}")
                return {"error": error_msg}
    
    def bulk_search(self, phone_numbers, country_code="IN"):
        """Search multiple phone numbers"""
        results = {}
        total = len(phone_numbers)
        
        print_message('info', f"Starting bulk search for {total} numbers...")
        
        for i, number in enumerate(phone_numbers, 1):
            print_message('info', f"Progress: {i}/{total} - Processing: {number}")
            results[number] = self.search_number(number, country_code)
            
            # Add delay between requests to avoid rate limiting
            if i < total:
                time.sleep(1)
        
        print_message('success', f"Bulk search completed! Processed {total} numbers")
        return results
    
    def get_api_status(self):
        """Check API status"""
        try:
            # Test with a sample number
            test_response = search_phonenumber(
                "+911234567890", 
                "IN", 
                self.api_key
            )
            return test_response is not None
        except:
            return False
    
    def set_api_key(self, api_key):
        """Set custom API key"""
        self.api_key = api_key
        print_message('success', "API key updated successfully")
