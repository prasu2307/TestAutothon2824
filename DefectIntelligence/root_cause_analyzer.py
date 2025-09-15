"""
Real-Time Defect Root Cause Analysis - Standalone Module
"""
import json
import os
import re
from datetime import datetime
from typing import Dict, List


class RootCauseAnalyzer:
    def __init__(self):
        self.analysis_file = "Outputs/root_cause_analysis.json"
        self.known_patterns = {
            "timeout": {
                "keywords": ["timeout", "timed out", "TimeoutException"],
                "root_cause": "Network/Performance Issue",
                "fix_suggestion": "Increase timeout or add retry mechanism"
            },
            "element_not_found": {
                "keywords": ["NoSuchElementException", "element not found", "not clickable"],
                "root_cause": "UI Element Locator Issue",
                "fix_suggestion": "Update locator strategy or add explicit wait"
            },
            "connection_error": {
                "keywords": ["ConnectionError", "connection refused", "network"],
                "root_cause": "Network Connectivity Issue",
                "fix_suggestion": "Check service availability or add connection retry"
            },
            "assertion_error": {
                "keywords": ["AssertionError", "expected", "but was"],
                "root_cause": "Data/Logic Validation Issue",
                "fix_suggestion": "Review test data or application logic"
            }
        }
    
    def analyze_failure_instantly(self, test_result: Dict) -> Dict:
        """Instant analysis when test fails"""
        test_name = test_result.get('test_name', 'unknown')
        error_message = test_result.get('error_message', '')
        stack_trace = test_result.get('stack_trace', '')
        
        # Combine error sources
        full_error = f"{error_message} {stack_trace}".lower()
        
        # Pattern matching
        root_cause = "Unknown Issue"
        fix_suggestion = "Review test manually"
        confidence = 0.3
        
        for pattern_name, pattern_data in self.known_patterns.items():
            if any(keyword in full_error for keyword in pattern_data["keywords"]):
                root_cause = pattern_data["root_cause"]
                fix_suggestion = pattern_data["fix_suggestion"]
                confidence = 0.85
                break
        
        # Find similar failures
        similar_failures = self._find_similar_failures(full_error)
        
        analysis = {
            "test_name": test_name,
            "root_cause": root_cause,
            "fix_suggestion": fix_suggestion,
            "confidence": confidence,
            "similar_failures": similar_failures,
            "error_category": self._categorize_error(full_error),
            "analyzed_at": datetime.now().isoformat()
        }
        
        self._save_analysis(analysis)
        return analysis
    
    def get_failure_trends(self) -> Dict:
        """Get failure trend analysis"""
        analyses = self._load_analyses()
        
        trends = {
            "most_common_causes": {},
            "failure_categories": {},
            "recurring_tests": {}
        }
        
        for analysis in analyses:
            # Count root causes
            cause = analysis.get('root_cause', 'Unknown')
            trends["most_common_causes"][cause] = trends["most_common_causes"].get(cause, 0) + 1
            
            # Count categories
            category = analysis.get('error_category', 'Other')
            trends["failure_categories"][category] = trends["failure_categories"].get(category, 0) + 1
            
            # Count recurring tests
            test_name = analysis.get('test_name', 'unknown')
            trends["recurring_tests"][test_name] = trends["recurring_tests"].get(test_name, 0) + 1
        
        return trends
    
    def suggest_test_improvements(self, test_name: str) -> List[str]:
        """Suggest improvements based on historical failures"""
        analyses = self._load_analyses()
        test_failures = [a for a in analyses if a.get('test_name') == test_name]
        
        if not test_failures:
            return ["No historical data available"]
        
        suggestions = set()
        for failure in test_failures[-5:]:  # Last 5 failures
            suggestions.add(failure.get('fix_suggestion', 'Review manually'))
        
        # Add general suggestions based on failure count
        if len(test_failures) > 3:
            suggestions.add("Consider test stability improvements")
        if len(test_failures) > 5:
            suggestions.add("Mark as flaky test for investigation")
        
        return list(suggestions)
    
    def _categorize_error(self, error_text: str) -> str:
        """Categorize error type"""
        if any(word in error_text for word in ["timeout", "slow", "performance"]):
            return "Performance"
        elif any(word in error_text for word in ["element", "locator", "clickable"]):
            return "UI/Locator"
        elif any(word in error_text for word in ["connection", "network", "refused"]):
            return "Network"
        elif any(word in error_text for word in ["assertion", "expected", "validation"]):
            return "Logic/Data"
        else:
            return "Other"
    
    def _find_similar_failures(self, error_text: str) -> List[str]:
        """Find similar historical failures"""
        analyses = self._load_analyses()
        similar = []
        
        # Simple similarity based on common keywords
        error_words = set(re.findall(r'\w+', error_text.lower()))
        
        for analysis in analyses[-20:]:  # Check last 20 analyses
            other_error = f"{analysis.get('error_message', '')} {analysis.get('stack_trace', '')}".lower()
            other_words = set(re.findall(r'\w+', other_error))
            
            # Calculate simple similarity
            common_words = error_words.intersection(other_words)
            if len(common_words) > 2:  # At least 3 common words
                test_name = analysis.get('test_name', 'unknown')
                if test_name not in similar:
                    similar.append(test_name)
        
        return similar[:3]  # Top 3 similar
    
    def _load_analyses(self) -> List[Dict]:
        """Load historical analyses"""
        if os.path.exists(self.analysis_file):
            try:
                with open(self.analysis_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_analysis(self, analysis: Dict):
        """Save analysis result"""
        analyses = self._load_analyses()
        analyses.append(analysis)
        
        os.makedirs(os.path.dirname(self.analysis_file), exist_ok=True)
        with open(self.analysis_file, 'w') as f:
            json.dump(analyses[-200:], f, indent=2)  # Keep last 200