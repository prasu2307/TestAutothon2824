"""
Problem Statement Parser
Extracts structured information from TestAutothon problem statements
"""

import re
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class TestStep:
    step_number: str
    step_type: str  # 'ui', 'api', 'mobile', 'setup', 'reporting'
    actions: List[str]
    entities: Dict[str, Any]
    raw_text: str


class ProblemParser:
    def __init__(self):
        self.ui_keywords = ['launch', 'browser', 'open', 'click', 'navigate', 'extract', 'locate', 'website']
        self.api_keywords = ['api', 'send', 'post', 'get', 'validate', 'backend', 'endpoint']
        self.mobile_keywords = ['apk', 'mobile', 'device', 'emulator', 'app']
        self.setup_keywords = ['setup', 'automation', 'build', 'deploy', 'jenkins']
        self.reporting_keywords = ['report', 'results', 'issues', 'documentation']
    
    def parse_problem_statement(self, problem_text: str) -> List[TestStep]:
        """Parse problem statement into structured test steps"""
        steps = []
        
        # Split by steps
        step_pattern = r'Step\s+(\d+(?:\.\d+)?):?\s*(.*?)(?=Step\s+\d+|$)'
        matches = re.findall(step_pattern, problem_text, re.DOTALL | re.IGNORECASE)
        
        for step_num, step_content in matches:
            step = self._parse_step(step_num, step_content.strip())
            steps.append(step)
        
        return steps
    
    def _parse_step(self, step_number: str, content: str) -> TestStep:
        """Parse individual step content"""
        step_type = self._classify_step_type(content)
        actions = self._extract_actions(content)
        entities = self._extract_entities(content, step_type)
        
        return TestStep(
            step_number=step_number,
            step_type=step_type,
            actions=actions,
            entities=entities,
            raw_text=content
        )
    
    def _classify_step_type(self, content: str) -> str:
        """Classify step type based on keywords"""
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in self.ui_keywords):
            return 'ui'
        elif any(keyword in content_lower for keyword in self.api_keywords):
            return 'api'
        elif any(keyword in content_lower for keyword in self.mobile_keywords):
            return 'mobile'
        elif any(keyword in content_lower for keyword in self.setup_keywords):
            return 'setup'
        elif any(keyword in content_lower for keyword in self.reporting_keywords):
            return 'reporting'
        else:
            return 'general'
    
    def _extract_actions(self, content: str) -> List[str]:
        """Extract action verbs from content"""
        action_pattern = r'\b(launch|open|click|navigate|extract|locate|send|post|get|validate|setup|create)\b'
        actions = re.findall(action_pattern, content, re.IGNORECASE)
        return list(set(actions))
    
    def _extract_entities(self, content: str, step_type: str) -> Dict[str, Any]:
        """Extract entities based on step type"""
        entities = {}
        
        if step_type == 'ui':
            entities.update(self._extract_ui_entities(content))
        elif step_type == 'api':
            entities.update(self._extract_api_entities(content))
        elif step_type == 'mobile':
            entities.update(self._extract_mobile_entities(content))
        
        return entities
    
    def _extract_ui_entities(self, content: str) -> Dict[str, Any]:
        """Extract UI-specific entities"""
        entities = {}
        
        # Extract URLs
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, content)
        if urls:
            entities['urls'] = urls
        
        # Extract website names
        website_pattern = r'\b([A-Z][a-zA-Z]*\.com)\b'
        websites = re.findall(website_pattern, content)
        if websites:
            entities['websites'] = websites
        
        # Extract sections/links
        section_pattern = r'"([^"]+)"'
        sections = re.findall(section_pattern, content)
        if sections:
            entities['sections'] = sections
        
        # Extract data fields
        if 'extract' in content.lower():
            field_pattern = r'●\s*([^\n]+)'
            fields = re.findall(field_pattern, content)
            entities['extract_fields'] = [field.strip() for field in fields]
        
        return entities
    
    def _extract_api_entities(self, content: str) -> Dict[str, Any]:
        """Extract API-specific entities"""
        entities = {}
        
        # Extract API URLs
        api_url_pattern = r'http[s]?://[^\s]+(?:docs|api)[^\s]*'
        api_urls = re.findall(api_url_pattern, content)
        if api_urls:
            entities['api_urls'] = api_urls
        
        # Extract data format requirements
        if 'format' in content.lower():
            format_pattern = r'format[^.]*\.([^.]*)\.'
            formats = re.findall(format_pattern, content, re.IGNORECASE)
            entities['data_formats'] = formats
        
        return entities
    
    def _extract_mobile_entities(self, content: str) -> Dict[str, Any]:
        """Extract mobile-specific entities"""
        entities = {}
        
        # Extract APK references
        if 'apk' in content.lower():
            entities['app_type'] = 'apk'
        
        # Extract mobile data fields
        if 'extract' in content.lower():
            field_pattern = r'●\s*([^\n]+)'
            fields = re.findall(field_pattern, content)
            entities['extract_fields'] = [field.strip() for field in fields]
        
        return entities