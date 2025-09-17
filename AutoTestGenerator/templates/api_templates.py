"""API Test Templates"""
from typing import Dict, List, Any

class APITemplates:
    @staticmethod
    def generate_api_test_class(class_name: str, steps: List[str]) -> str:
        template = '''"""
Auto-generated API Test Case
"""
import pytest
import requests
from HelperClasses.API.ValidateAPI import ValidateAPI

class {class_name}:
    
    @pytest.mark.api_test
    @pytest.mark.auto_generated
    def test_auto_generated_api(self):
        api_validator = ValidateAPI()
        
{test_steps}
'''
        test_steps = "\n".join([f"        {step}" for step in steps])
        return template.format(class_name=class_name, test_steps=test_steps)
    
    @staticmethod
    def post_data_template(api_url: str, data_fields: List[str]) -> str:
        return f'''# Post extracted data to API
api_url = "{api_url}"

payload = {{
    "headline": extracted_data[0].get("headline", ""),
    "link": extracted_data[0].get("link", ""),
    "date_time": extracted_data[0].get("date_time", ""),
    "team_name": "TestAutothon2824"
}}

response = requests.post(api_url, json=payload)
assert response.status_code == 200, f"API POST failed: {{response.status_code}}"

response_data = response.json()
item_id = response_data.get("item_id")
assert item_id, "Item ID not found in response"'''
    
    @staticmethod
    def validate_data_template(api_url: str) -> str:
        return f'''# Validate data using Item ID
validate_url = f"{api_url}/{{item_id}}"

validate_response = requests.get(validate_url)
assert validate_response.status_code == 200, f"API validation failed: {{validate_response.status_code}}"

validated_data = validate_response.json()
assert validated_data.get("headline") == payload["headline"], "Headline validation failed"
assert validated_data.get("team_name") == payload["team_name"], "Team name validation failed"'''