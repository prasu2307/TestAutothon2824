"""
Integration Hook for DefectIntelligence with Existing Tests
Non-intrusive integration that can be optionally enabled
"""
import sys
import os
from typing import Dict, Any

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

from defect_predictor import DefectPredictor
from root_cause_analyzer import RootCauseAnalyzer
from defect_triage import DefectTriage


class DefectIntelligenceHook:
    """Optional hook for integrating with existing test framework"""
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        if self.enabled:
            self.predictor = DefectPredictor()
            self.analyzer = RootCauseAnalyzer()
            self.triage = DefectTriage()
    
    def predict_before_test(self, test_name: str) -> Dict:
        """Call before test execution for prediction"""
        if not self.enabled:
            return {}
        
        try:
            prediction = self.predictor.predict_failure_probability(test_name)
            print(f"🔮 DefectIntelligence: {test_name} has {prediction['failure_probability']*100:.1f}% failure probability")
            return prediction
        except Exception as e:
            print(f"DefectIntelligence prediction error: {e}")
            return {}
    
    def analyze_after_failure(self, test_name: str, error_message: str, stack_trace: str = "") -> Dict:
        """Call after test failure for analysis"""
        if not self.enabled:
            return {}
        
        try:
            test_result = {
                "test_name": test_name,
                "error_message": error_message,
                "stack_trace": stack_trace
            }
            
            analysis = self.analyzer.analyze_failure_instantly(test_result)
            print(f"🔍 DefectIntelligence: Root cause - {analysis['root_cause']}")
            print(f"💡 Suggestion: {analysis['fix_suggestion']}")
            
            return analysis
        except Exception as e:
            print(f"DefectIntelligence analysis error: {e}")
            return {}
    
    def update_prediction_accuracy(self, test_name: str, result: str):
        """Update prediction accuracy based on actual result"""
        if not self.enabled:
            return
        
        try:
            self.predictor.update_prediction_accuracy(test_name, result)
        except Exception as e:
            print(f"DefectIntelligence update error: {e}")
    
    def triage_session_failures(self, failures: list) -> Dict:
        """Triage all failures from a test session"""
        if not self.enabled or not failures:
            return {}
        
        try:
            triage_result = self.triage.categorize_defects_realtime(failures)
            
            print(f"\n📊 DefectIntelligence Triage Summary:")
            print(f"   Total Defects: {triage_result['summary']['total_defects']}")
            print(f"   Critical: {triage_result['summary']['critical_count']}")
            print(f"   Need Attention: {triage_result['summary']['needs_immediate_attention']}")
            
            return triage_result
        except Exception as e:
            print(f"DefectIntelligence triage error: {e}")
            return {}


# Global instance for easy integration
defect_intelligence = DefectIntelligenceHook()


# Example integration functions (can be called from existing tests)
def predict_test_failure(test_name: str):
    """Standalone function to predict test failure"""
    return defect_intelligence.predict_before_test(test_name)


def analyze_test_failure(test_name: str, error_msg: str, stack_trace: str = ""):
    """Standalone function to analyze test failure"""
    return defect_intelligence.analyze_after_failure(test_name, error_msg, stack_trace)


def triage_failures(failure_list: list):
    """Standalone function to triage multiple failures"""
    return defect_intelligence.triage_session_failures(failure_list)