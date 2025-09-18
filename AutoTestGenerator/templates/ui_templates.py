"""UI Test Templates"""
from typing import Dict, List, Any

class UITemplates:
    @staticmethod
    def generate_ui_test_class(class_name: str, steps: List[str]) -> str:
        template = '''"""
Auto-generated UI Test Case
"""
import pytest
from HelperClasses.UI.Sample import Sample

@pytest.mark.usefixtures("init_driver")
class {class_name}:
    
    @pytest.mark.ui_test
    @pytest.mark.auto_generated
    def test_auto_generated_ui(self, extra, env, request, caseid):
        sample = Sample(self.driver, extra)
        
{test_steps}
'''
        test_steps = "\n".join([f"        {step}" for step in steps])
        return template.format(class_name=class_name, test_steps=test_steps)
    
    @staticmethod
    def launch_browser_template(website_name: str, url: str) -> str:
        return f'sample.launch_application("{website_name}", "{url}", env)'
    
    @staticmethod
    def click_section_template(sections: List[str]) -> str:
        sections_str = '", "'.join(sections)
        return f'''# Click on section link
section_links = ["{sections_str}"]
for section in section_links:
    try:
        element = self.driver.find_element("link text", section)
        element.click()
        break
    except:
        continue'''
    
    @staticmethod
    def extract_carousel_data_template(fields: List[str], count: int = 3) -> str:
        field_extraction = []
        for field in fields:
            if 'headline' in field.lower():
                field_extraction.append('headline = carousel_item.find_element("css selector", "h2, h3, .headline").text')
            elif 'link' in field.lower():
                field_extraction.append('link = carousel_item.find_element("css selector", "a").get_attribute("href")')
            elif 'date' in field.lower() or 'time' in field.lower():
                field_extraction.append('date_time = carousel_item.find_element("css selector", ".date, .time, time").text')
        
        extractions = "\n                ".join(field_extraction)
        
        return f'''# Extract carousel data
carousel_items = self.driver.find_elements("css selector", ".carousel-item, .slider-item")[:{count}]
extracted_data = []

for carousel_item in carousel_items:
    try:
        {extractions}
        
        data = {{
            "headline": headline if 'headline' in locals() else "",
            "link": link if 'link' in locals() else "",
            "date_time": date_time if 'date_time' in locals() else "",
            "team_name": "TestAutothon2824"
        }}
        extracted_data.append(data)
    except Exception as e:
        print(f"Error extracting carousel data: {{e}}")

return extracted_data'''
    
    @staticmethod
    def visual_checkpoint_template(checkpoint_name: str, threshold: float = 0.85) -> str:
        return f'sample.ssim_visual_checkpoint("{checkpoint_name}", threshold={threshold})'