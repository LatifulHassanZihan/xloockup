"""
Truecaller API Handler for Xloockup
"""

import requests
import json
import time
from config import HEADERS, TRUECALLER_SEARCH_URL, COUNTRY_CODES
from utils import print_message, validate_phone_number

class TruecallerAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.request_count = 0
    
    def search_number(self, phone_number, country_code="IN"):
        """
        Search phone number using Truecaller API
        """
        try:
            is_valid, cleaned_number = validate_phone_number(phone_number)
            if not is_valid:
                print_message('error', f"Invalid phone number: {cleaned_number}")
                return None
            
            # Fix for Bangladesh numbers - remove extra zeros
            if country_code == "BD" and cleaned_number.startswith("+0"):
                cleaned_number = "+88" + cleaned_number[2:]
            elif country_code == "BD" and cleaned_number.startswith("0"):
                cleaned_number = "+88" + cleaned_number[1:]
            
            country_name = COUNTRY_CODES.get(country_code, country_code)
            print_message('info', f"Searching: {cleaned_number} ({country_name})")
            
            # Rate limiting
            self.request_count += 1
            if self.request_count % 3 == 0:
                print_message('warning', "Rate limiting - waiting 2 seconds...")
                time.sleep(2)
            
            # Updated payload structure
            payload = {
                "q": cleaned_number,
                "countryCode": country_code,
                "type": "1",
                "placement": "SEARCHRESULTS,HISTORY,DETAILS",
                "encoding": "json"
            }
            
            # Try different API endpoints
            endpoints = [
                "https://search5-noneu.truecaller.com/v2/search",
                "https://search5.truecaller.com/v2/search",
                "https://api4.truecaller.com/v1/search"
            ]
            
            response = None
            for endpoint in endpoints:
                try:
                    print_message('info', f"Trying endpoint: {endpoint.split('/')[-2]}")
                    response = self.session.post(
                        endpoint,
                        json=payload,
                        timeout=15
                    )
                    if response.status_code == 200:
                        break
                except:
                    continue
            
            if not response:
                print_message('error', "All API endpoints failed")
                return {"error": "All API endpoints failed"}
            
            if response.status_code == 200:
                data = response.json()
                parsed_data = self._parse_response(data, cleaned_number)
                if 'error' not in parsed_data:
                    print_message('success', "Lookup successful!")
                return parsed_data
            elif response.status_code == 404:
                print_message('error', "Number not found in database")
                return {"error": "Number not found in Truecaller database"}
            elif response.status_code == 429:
                print_message('error', "Rate limited - Too many requests")
                return {"error": "Rate limited - try again later"}
            else:
                print_message('error', f"API Error: Status {response.status_code}")
                return {"error": f"API returned status {response.status_code}"}
                
        except requests.exceptions.Timeout:
            print_message('error', "Request timeout - Server took too long to respond")
            return {"error": "Request timeout"}
        except requests.exceptions.ConnectionError:
            print_message('error', "Network connection error - Check your internet")
            return {"error": "Network connection failed"}
        except Exception as e:
            print_message('error', f"Unexpected error: {str(e)}")
            return {"error": str(e)}
    
    def _parse_response(self, data, phone_number):
        """Parse Truecaller API response"""
        try:
            if not data:
                return {"error": "Empty response from API"}
                
            if 'data' not in data or not data['data']:
                return {"error": "No data available for this number"}
            
            result = {
                "searched_number": phone_number,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Take first result item
            item = data['data'][0]
            
            # Extract name
            if 'name' in item and item['name']:
                result['name'] = item['name']
            
            # Extract phone information
            if 'phones' in item and item['phones']:
                phone_info = item['phones'][0]
                result['phone'] = phone_info.get('e164Format', '')
                result['carrier'] = phone_info.get('carrier', 'Unknown Carrier')
                result['type'] = phone_info.get('type', 'Unknown Type')
            
            # Extract address information
            if 'addresses' in item and item['addresses']:
                address_info = item['addresses'][0]
                result['address'] = address_info.get('city', '')
                result['country'] = address_info.get('countryCode', '')
                if 'address' in address_info:
                    result['full_address'] = address_info.get('address', '')
            
            # Extract email information
            if 'internetAddresses' in item and item['internetAddresses']:
                for internet_addr in item['internetAddresses']:
                    addr_id = internet_addr.get('id', '').lower()
                    if 'email' in addr_id or '@' in addr_id:
                        result['email'] = internet_addr.get('id', '')
                        break
            
            # Extract spam and score information
            result['score'] = item.get('score', 0)
            result['spam_score'] = item.get('spamScore', 0)
            result['spam_type'] = item.get('spamType', 'Not Spam')
            
            # Additional info
            result['search_source'] = item.get('source', 'Truecaller')
            result['active'] = item.get('active', True)
            
            # Check if we got any useful data
            if not any(key in result for key in ['name', 'carrier', 'address', 'email']):
                return {"error": "No identifiable information found"}
            
            return result
            
        except Exception as e:
            print_message('error', f"Error parsing response: {str(e)}")
            return {"error": "Failed to parse API response"}
    
    def bulk_search(self, phone_numbers, country_code="IN"):
        """Search multiple phone numbers"""
        results = {}
        total = len(phone_numbers)
        
        print_message('info', f"Starting bulk search for {total} numbers...")
        
        for i, number in enumerate(phone_numbers, 1):
            print_message('info', f"Progress: {i}/{total} - Processing: {number}")
            results[number] = self.search_number(number, country_code)
            
            # Add delay between requests
            if i < total:
                time.sleep(1)
        
        print_message('success', f"Bulk search completed! Processed {total} numbers")
        return results
    
    def get_api_status(self):
        """Check API status"""
        try:
            test_payload = {
                "q": "+8801712345678",
                "countryCode": "BD",
                "type": "1",
                "encoding": "json"
            }
            
            response = self.session.post(
                TRUECALLER_SEARCH_URL,
                json=test_payload,
                timeout=10
            )
            
            return response.status_code == 200
        except:
            return False
