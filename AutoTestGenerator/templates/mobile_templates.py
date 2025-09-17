"""Mobile Test Templates"""
from typing import Dict, List, Any

class MobileTemplates:
    @staticmethod
    def generate_mobile_test_class(class_name: str, steps: List[str]) -> str:
        template = '''"""
Auto-generated Mobile Test Case
"""
import pytest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

class {class_name}:
    
    @pytest.mark.mobile_test
    @pytest.mark.auto_generated
    def test_auto_generated_mobile(self):
        
{test_steps}
'''
        test_steps = "\n".join([f"        {step}" for step in steps])
        return template.format(class_name=class_name, test_steps=test_steps)
    
    @staticmethod
    def setup_mobile_driver_template(apk_path: str = "app.apk") -> str:
        return f'''# Setup mobile driver
desired_caps = {{
    "platformName": "Android",
    "deviceName": "emulator-5554",
    "app": "{apk_path}",
    "automationName": "UiAutomator2"
}}

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
driver.implicitly_wait(10)'''
    
    @staticmethod
    def extract_product_data_template(fields: List[str]) -> str:
        field_extraction = []
        for field in fields:
            if 'name' in field.lower():
                field_extraction.append('name = driver.find_element(AppiumBy.ID, "product_name").text')
            elif 'description' in field.lower():
                field_extraction.append('description = driver.find_element(AppiumBy.ID, "product_description").text')
            elif 'price' in field.lower():
                field_extraction.append('price = driver.find_element(AppiumBy.ID, "product_price").text')
        
        extractions = "\n            ".join(field_extraction)
        
        return f'''# Extract product data from mobile app
try:
    {extractions}
    
    product_data = {{
        "name": name if 'name' in locals() else "",
        "description": description if 'description' in locals() else "",
        "price": price if 'price' in locals() else "",
        "team_name": "TestAutothon2824"
    }}
    
except Exception as e:
    print(f"Error extracting product data: {{e}}")
    product_data = {{"team_name": "TestAutothon2824"}}'''
    
    @staticmethod
    def cleanup_mobile_template() -> str:
        return '''# Cleanup mobile driver
try:
    driver.quit()
except:
    pass'''