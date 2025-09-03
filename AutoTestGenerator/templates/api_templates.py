"""
API Test Templates
Code templates for API automation test generation
"""

from typing import Dict, List, Any


class APITemplates:
    
    @staticmethod
    def generate_api_test_class(class_name: str, steps: List[str]) -> str:
        """Generate complete API test class"""
        template = '''"""
Auto-generated API Test Case
Generated from TestAutothon problem statement
"""

import pytest
import requests
import json
from HelperClasses.API.ValidateAPI import ValidateAPI


class {class_name}:
    
    @pytest.mark.api_test
    @pytest.mark.auto_generated
    def test_auto_generated_api(self):
        """Auto-generated API test method"""
        api_validator = ValidateAPI()
        
{test_steps}
'''
        
        test_steps = "\n".join([f"        {step}" for step in steps])
        return template.format(class_name=class_name, test_steps=test_steps)
    
    @staticmethod
    def post_data_template(api_url: str, data_fields: List[str]) -> str:
        """Template for posting data to API"""
        return f'''# Post extracted data to API
        api_url = "{api_url}"
        
        # Prepare data payload
        payload = {{
            "headline": extracted_data[0].get("headline", ""),
            "link": extracted_data[0].get("link", ""),
            "date_time": extracted_data[0].get("date_time", ""),
            "team_name": "TestAutothon2824"
        }}
        
        # Send POST request
        response = requests.post(api_url, json=payload)
        assert response.status_code == 200, f"API POST failed: {{response.status_code}}"
        
        # Extract Item ID from response
        response_data = response.json()
        item_id = response_data.get("item_id")
        assert item_id, "Item ID not found in response"'''
    
    @staticmethod
    def validate_data_template(api_url: str) -> str:
        """Template for validating data using API"""
        return f'''# Validate data using Item ID
        validate_url = f"{api_url}/{{item_id}}"
        
        # Send GET request to validate
        validate_response = requests.get(validate_url)
        assert validate_response.status_code == 200, f"API validation failed: {{validate_response.status_code}}"
        
        # Validate response data
        validated_data = validate_response.json()
        assert validated_data.get("headline") == payload["headline"], "Headline validation failed"
        assert validated_data.get("team_name") == payload["team_name"], "Team name validation failed"'''
    
    @staticmethod
    def format_date_template(date_format: str = "DDMMYYYY") -> str:
        """Template for formatting date"""
        return '''# Format date to required format (DDMMYYYY)
        from datetime import datetime
        import re
        
        def format_date_to_ddmmyyyy(date_string):
            """Convert date string to DDMMYYYY format"""
            # Extract date patterns
            date_patterns = [
                r'(\d{1,2})-(\w+)-(\d{4})',  # 15-Aug-2024
                r'(\d{1,2})/(\d{1,2})/(\d{4})',  # 15/08/2024
                r'(\d{4})-(\d{1,2})-(\d{1,2})',  # 2024-08-15
            ]
            
            month_map = {
                'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
            }
            
            for pattern in date_patterns:
                match = re.search(pattern, date_string.lower())
                if match:
                    if len(match.groups()) == 3:
                        day, month, year = match.groups()
                        if month.isalpha():
                            month = month_map.get(month[:3], '01')
                        return f"{day.zfill(2)}{month.zfill(2)}{year}"
            
            return date_string
        
        # Apply date formatting to extracted data
        for data in extracted_data:
            if data.get("date_time"):
                data["date_time"] = format_date_to_ddmmyyyy(data["date_time"])'''