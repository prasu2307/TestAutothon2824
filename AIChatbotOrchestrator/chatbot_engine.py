"""
Main AI Chatbot Engine for Test Orchestration
"""
from .nlp_processor import NLPProcessor
from .test_executor import TestExecutor
from typing import Dict, List


class TestChatBot:
    """AI Chatbot for natural language test orchestration"""
    
    def __init__(self):
        self.nlp_processor = NLPProcessor()
        self.test_executor = TestExecutor()
        self.conversation_history = []
    
    def process_command(self, user_input: str) -> str:
        """Process natural language command and return response"""
        # Parse the user input
        intent = self.nlp_processor.parse_intent(user_input)
        
        # Store in conversation history
        self.conversation_history.append({
            'user_input': user_input,
            'parsed_intent': intent
        })
        
        # Execute the intent
        response = self.test_executor.execute_intent(intent)
        
        # Add context-aware response
        contextual_response = self._add_context(response, intent)
        
        return contextual_response
    
    def _add_context(self, response: str, intent: Dict) -> str:
        """Add contextual information to response"""
        context_info = []
        
        # Add helpful tips based on intent
        if intent['action'] == 'run_tests':
            if intent.get('test_type') == 'visual':
                context_info.append("💡 Tip: Run baseline creation first if visual tests fail")
        
        if intent['action'] == 'optimize':
            context_info.append("🔄 You can re-run tests to see optimization effects")
        
        if context_info:
            response += "\\n\\n" + "\\n".join(context_info)
        
        return response
    
    def get_help(self) -> str:
        """Get help information"""
        help_text = """
🤖 AI Test Chatbot - Available Commands:

📋 Test Execution:
• "Run UI tests on Chrome"
• "Execute API tests for non-prod"
• "Test visual validation"
• "Start mobile testing"

🔧 Test Optimization:
• "Optimize visual tests"
• "Fix flaky tests"
• "Speed up test execution"
• "Improve test stability"

📊 Test Analysis:
• "Analyze UI test results"
• "Check test coverage"
• "Review test performance"

🎯 Supported Test Types: UI, API, Mobile, Visual
🌐 Environments: non-prod, prod
🔍 Browsers: Chrome, Firefox, Edge
        """
        return help_text.strip()
    
    def get_conversation_summary(self) -> List[Dict]:
        """Get conversation history summary"""
        return self.conversation_history[-5:]  # Last 5 interactions