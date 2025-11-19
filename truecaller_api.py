"""
Truecaller API Handler for Xloockup
"""

import requests
import json
from config import HEADERS, TRUECALLER_SEARCH_URL, COUNTRY_CODES
from utils import print_message, validate_phone_number

class TruecallerAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def search_number(self, phone_number, country_code="IN"):
        """
        Search phone number using Truecaller API
        """
        try:
            # Validate phone number
            is_valid, cleaned_number = validate_phone_number(phone_number)
            if not is_valid:
                print_message('error', f"Invalid phone number: {cleaned_number}")
                return None
            
            print_message('info', f"Searching: {cleaned_number} ({COUNTRY_CODES.get(country_code, country_code)})")
            
            # Prepare payload
            payload = {
                "q": cleaned_number,
                "countryCode": country_code,
                "type": "4",
                "placement": "SEARCHRESULTS,HISTORY,DETAILS",
                "encoding": "json"
            }
            
            # Make API request
            response = self.session.post(
                TRUECALLER_SEARCH_URL,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_response(data, cleaned_number)
            else:
                print_message('error', f"API Error: Status {response.status_code}")
                return {"error": f"API returned status {response.status_code}"}
                
        except requests.exceptions.Timeout:
            print_message('error', "Request timeout - Try again")
            return {"error": "Request timeout"}
        except requests.exceptions.ConnectionError:
            print_message('error', "Network connection error")
            return {"error": "Network connection failed"}
        except Exception as e:
            print_message('error', f"Unexpected error: {str(e)}")
            return {"error": str(e)}
    
    def _parse_response(self, data, phone_number):
        """Parse Truecaller API response"""
        try:
            if not data or 'data' not in data:
                return {"error": "No data available"}
            
            result = {"searched_number": phone_number}
            
            # Extract information from response
            for item in data.get('data', []):
                # Name information
                if 'name' in item:
                    result['name'] = item['name']
                
                # Phone information
                if 'phones' in item and item['phones']:
                    phone_info = item['phones'][0]
                    result['phone'] = phone_info.get('e164Format', '')
                    result['carrier'] = phone_info.get('carrier', '')
                    result['type'] = phone_info.get('type', '')
                
                # Location information
                if 'addresses' in item and item['addresses']:
                    address_info = item['addresses'][0]
                    result['address'] = address_info.get('city', '')
                    result['country'] = address_info.get('countryCode', '')
                
                # Email information
                if 'internetAddresses' in item and item['internetAddresses']:
                    for internet_addr in item['internetAddresses']:
                        if 'email' in internet_addr.get('id', '').lower():
                            result['email'] = internet_addr.get('id', '')
                
                # Spam and score information
                result['score'] = item.get('score', 0)
                result['spam_score'] = item.get('spamScore', 0)
                result['spam_type'] = item.get('spamType', '')
                
                # Break after first valid result
                break
            
            return result if any(key in result for key in ['name', 'carrier', 'address']) else {"error": "No identifiable information found"}
            
        except Exception as e:
            print_message('error', f"Error parsing response: {str(e)}")
            return {"error": "Failed to parse API response"}
    
    def bulk_search(self, phone_numbers, country_code="IN"):
        """Search multiple phone numbers"""
        results = {}
        total = len(phone_numbers)
        
        for i, number in enumerate(phone_numbers, 1):
            print_message('info', f"Processing {i}/{total}: {number}")
            results[number] = self.search_number(number, country_code)
        
        return results
