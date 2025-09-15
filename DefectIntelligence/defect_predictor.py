"""
AI-Powered Defect Prediction - Standalone Module
"""
import json
import os
from datetime import datetime
from typing import Dict, List


class DefectPredictor:
    def __init__(self):
        self.history_file = "Outputs/defect_history.json"
        self.predictions_file = "Outputs/defect_predictions.json"
        self.failure_patterns = self._load_history()
    
    def predict_failure_probability(self, test_name: str) -> Dict:
        """Predict failure probability for a test"""
        base_probability = 0.1
        
        # Pattern-based prediction
        if test_name in self.failure_patterns:
            pattern = self.failure_patterns[test_name]
            failure_rate = pattern.get('failure_count', 0) / max(pattern.get('total_runs', 1), 1)
            base_probability = min(failure_rate * 1.2, 0.95)
        
        # Risk factors
        risk_factors = []
        if 'api' in test_name.lower():
            risk_factors.append("Network dependency")
            base_probability += 0.1
        if 'ui' in test_name.lower():
            risk_factors.append("UI element instability")
            base_probability += 0.15
        if 'mobile' in test_name.lower():
            risk_factors.append("Device compatibility")
            base_probability += 0.2
        
        prediction = {
            "test_name": test_name,
            "failure_probability": round(min(base_probability, 0.95), 2),
            "risk_factors": risk_factors,
            "confidence": 0.85,
            "predicted_at": datetime.now().isoformat()
        }
        
        self._save_prediction(prediction)
        return prediction
    
    def suggest_preemptive_fixes(self, test_name: str) -> List[str]:
        """Suggest fixes before test runs"""
        fixes = []
        
        if 'api' in test_name.lower():
            fixes.extend(["Add retry mechanism", "Increase timeout", "Add response validation"])
        if 'ui' in test_name.lower():
            fixes.extend(["Use explicit waits", "Add element presence check", "Use stable locators"])
        if 'visual' in test_name.lower():
            fixes.extend(["Update baseline if needed", "Use relaxed threshold", "Check viewport size"])
        
        return fixes[:3]  # Top 3 suggestions
    
    def update_prediction_accuracy(self, test_name: str, actual_result: str):
        """Update prediction accuracy based on actual results"""
        if not os.path.exists(self.history_file):
            self.failure_patterns = {}
        
        if test_name not in self.failure_patterns:
            self.failure_patterns[test_name] = {"total_runs": 0, "failure_count": 0}
        
        self.failure_patterns[test_name]["total_runs"] += 1
        if actual_result == "FAILED":
            self.failure_patterns[test_name]["failure_count"] += 1
        
        self._save_history()
    
    def _load_history(self) -> Dict:
        """Load historical failure data"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_history(self):
        """Save failure history"""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump(self.failure_patterns, f, indent=2)
    
    def _save_prediction(self, prediction: Dict):
        """Save prediction for analysis"""
        predictions = []
        if os.path.exists(self.predictions_file):
            try:
                with open(self.predictions_file, 'r') as f:
                    predictions = json.load(f)
            except:
                pass
        
        predictions.append(prediction)
        os.makedirs(os.path.dirname(self.predictions_file), exist_ok=True)
        with open(self.predictions_file, 'w') as f:
            json.dump(predictions[-100:], f, indent=2)  # Keep last 100