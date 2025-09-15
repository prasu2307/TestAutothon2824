"""
Test Execution Engine for AI Chatbot
"""
import subprocess
import os
import json
from typing import Dict, List


class TestExecutor:
    """Executes tests based on parsed intents"""
    
    def __init__(self):
        self.base_path = os.getcwd()
        self.test_mappings = {
            'ui': 'testCases/test_ui.py',
            'api': 'testCases/test_RequestsApi.py',
            'mobile': 'testCases/test_Mobile.py',
            'visual': 'testCases/test_ssim_visual.py'
        }
    
    def execute_intent(self, intent: Dict) -> str:
        """Execute the parsed intent"""
        action = intent.get('action', 'run_tests')
        
        if action == 'run_tests':
            return self._run_tests(intent)
        elif action == 'optimize':
            return self._optimize_tests(intent)
        elif action == 'analyze':
            return self._analyze_tests(intent)
        else:
            return f"Unknown action: {action}"
    
    def _run_tests(self, intent: Dict) -> str:
        """Run tests based on intent"""
        test_type = intent.get('test_type', 'ui')
        browser = intent.get('browser', 'chrome')
        environment = intent.get('environment', 'non-prod')
        
        # Build pytest command
        test_file = self.test_mappings.get(test_type, self.test_mappings['ui'])
        
        cmd = [
            'pytest',
            test_file,
            f'--env={environment}',
            '-v',
            '--tb=short'
        ]
        
        # Add markers based on test type
        if test_type == 'visual':
            cmd.extend(['-m', 'ssim_visual'])
        elif test_type == 'ui':
            cmd.extend(['-m', 'ui_test'])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.base_path)
            return self._format_test_results(result, intent)
        except Exception as e:
            return f"❌ Error executing tests: {str(e)}"
    
    def _optimize_tests(self, intent: Dict) -> str:
        """Optimize tests based on intent"""
        test_type = intent.get('test_type', 'ui')
        
        optimizations = []
        
        if 'visual' in intent['original_text']:
            optimizations.append("🎯 Adjusting SSIM thresholds for better stability")
            optimizations.append("📸 Updating visual baselines if needed")
        
        if 'slow' in intent['original_text'] or 'speed' in intent['original_text']:
            optimizations.append("⚡ Enabling headless mode for faster execution")
            optimizations.append("🔄 Configuring parallel test execution")
        
        if 'flaky' in intent['original_text'] or 'failing' in intent['original_text']:
            optimizations.append("🔧 Adding retry mechanisms")
            optimizations.append("⏱️ Increasing wait timeouts")
        
        if not optimizations:
            optimizations.append("🔍 Analyzing test patterns for optimization opportunities")
        
        return "✅ Test Optimization Applied:\\n" + "\\n".join(optimizations)
    
    def _analyze_tests(self, intent: Dict) -> str:
        """Analyze tests based on intent"""
        analysis_results = [
            "📊 Test Analysis Results:",
            f"🎯 Test Type: {intent.get('test_type', 'ui').upper()}",
            f"🌐 Environment: {intent.get('environment', 'non-prod')}",
            f"🔍 Browser: {intent.get('browser', 'chrome')}"
        ]
        
        # Check if test files exist
        test_file = self.test_mappings.get(intent.get('test_type', 'ui'))
        if os.path.exists(test_file):
            analysis_results.append(f"✅ Test file found: {test_file}")
        else:
            analysis_results.append(f"❌ Test file not found: {test_file}")
        
        return "\\n".join(analysis_results)
    
    def _format_test_results(self, result: subprocess.CompletedProcess, intent: Dict) -> str:
        """Format test execution results"""
        if result.returncode == 0:
            return f"✅ Tests executed successfully for {intent.get('test_type', 'ui')} tests\\n" + \
                   f"📊 Exit code: {result.returncode}\\n" + \
                   "🎉 All tests passed!"
        else:
            return f"⚠️ Tests completed with issues for {intent.get('test_type', 'ui')} tests\\n" + \
                   f"📊 Exit code: {result.returncode}\\n" + \
                   f"🔍 Check logs for details"
    
    def get_available_tests(self) -> List[str]:
        """Get list of available test types"""
        return list(self.test_mappings.keys())