"""
Mobile Test Templates
Code templates for mobile automation test generation
"""

from typing import Dict, List, Any


class MobileTemplates:
    
    @staticmethod
    def generate_mobile_test_class(class_name: str, steps: List[str]) -> str:
        """Generate complete mobile test class"""
        template = '''"""
Auto-generated Mobile Test Case
Generated from TestAutothon problem statement
"""

import pytest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy


class {class_name}:
    
    @pytest.mark.mobile_test
    @pytest.mark.auto_generated
    def test_auto_generated_mobile(self):
        """Auto-generated mobile test method"""
        
{test_steps}
'''
        
        test_steps = "\n".join([f"        {step}" for step in steps])
        return template.format(class_name=class_name, test_steps=test_steps)
    
    @staticmethod
    def setup_mobile_driver_template(apk_path: str = "app.apk") -> str:
        """Template for setting up mobile driver"""
        return f'''# Setup mobile driver
        desired_caps = {{
            "platformName": "Android",
            "deviceName": "emulator-5554",
            "app": "{apk_path}",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 300
        }}
        
        driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
        driver.implicitly_wait(10)'''
    
    @staticmethod
    def extract_product_data_template(fields: List[str]) -> str:
        """Template for extracting product data from mobile app"""
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
            
            print(f"Extracted product data: {{product_data}}")
            
        except Exception as e:
            print(f"Error extracting product data: {{e}}")
            product_data = {{"team_name": "TestAutothon2824"}}'''
    
    @staticmethod
    def mobile_element_interaction_template(action: str, element_id: str) -> str:
        """Template for mobile element interactions"""
        if action.lower() == 'click':
            return f'driver.find_element(AppiumBy.ID, "{element_id}").click()'
        elif action.lower() == 'scroll':
            return f'''# Scroll to find element
            driver.scroll(driver.find_element(AppiumBy.ID, "{element_id}"), 
                         driver.find_element(AppiumBy.ID, "scroll_target"))'''
        elif action.lower() == 'swipe':
            return '''# Swipe gesture
            driver.swipe(start_x=500, start_y=1000, end_x=500, end_y=500, duration=1000)'''
        else:
            return f'# Interact with element: {element_id}'
    
    @staticmethod
    def mobile_wait_template(element_id: str, timeout: int = 10) -> str:
        """Template for waiting for mobile elements"""
        return f'''# Wait for mobile element
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        element = WebDriverWait(driver, {timeout}).until(
            EC.presence_of_element_located((AppiumBy.ID, "{element_id}"))
        )'''
    
    @staticmethod
    def cleanup_mobile_template() -> str:
        """Template for mobile test cleanup"""
        return '''# Cleanup mobile driver
        try:
            driver.quit()
        except:
            pass'''