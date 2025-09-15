"""
Natural Language Processing for Test Commands
"""
import re
from typing import Dict, List


class NLPProcessor:
    """Processes natural language commands into structured test intents"""
    
    def __init__(self):
        self.intent_patterns = {
            'run_tests': [
                r'run\s+(.*?)\s+tests?',
                r'execute\s+(.*?)\s+tests?',
                r'test\s+(.*)',
                r'start\s+(.*?)\s+testing'
            ],
            'optimize': [
                r'optimize\s+(.*)',
                r'fix\s+(.*)',
                r'improve\s+(.*)',
                r'speed up\s+(.*)'
            ],
            'analyze': [
                r'analyze\s+(.*)',
                r'check\s+(.*)',
                r'examine\s+(.*)',
                r'review\s+(.*)'
            ]
        }
        
        self.entity_patterns = {
            'test_type': {
                'ui': ['ui', 'website', 'web', 'browser', 'frontend'],
                'api': ['api', 'rest', 'endpoint', 'service'],
                'mobile': ['mobile', 'android', 'app'],
                'visual': ['visual', 'ssim', 'screenshot', 'appearance']
            },
            'browser': {
                'chrome': ['chrome', 'google'],
                'firefox': ['firefox', 'mozilla'],
                'edge': ['edge', 'microsoft']
            },
            'environment': {
                'non-prod': ['non-prod', 'test', 'staging', 'dev'],
                'prod': ['prod', 'production', 'live']
            }
        }
    
    def parse_intent(self, text: str) -> Dict:
        """Parse natural language text into structured intent"""
        text = text.lower().strip()
        
        # Determine action intent
        action = self._extract_action(text)
        
        # Extract entities
        entities = self._extract_entities(text)
        
        return {
            'action': action,
            'original_text': text,
            **entities
        }
    
    def _extract_action(self, text: str) -> str:
        """Extract the main action from text"""
        for action, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return action
        return 'run_tests'  # default action
    
    def _extract_entities(self, text: str) -> Dict:
        """Extract entities like test_type, browser, environment"""
        entities = {}
        
        for entity_type, entity_map in self.entity_patterns.items():
            for entity_value, keywords in entity_map.items():
                for keyword in keywords:
                    if keyword in text:
                        entities[entity_type] = entity_value
                        break
                if entity_type in entities:
                    break
        
        # Set defaults if not found
        entities.setdefault('test_type', 'ui')
        entities.setdefault('browser', 'chrome')
        entities.setdefault('environment', 'non-prod')
        
        return entities