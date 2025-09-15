"""
Live Defect Triage Dashboard - Standalone Module
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List


class DefectTriage:
    def __init__(self):
        self.triage_file = "Outputs/defect_triage.json"
        self.dashboard_file = "Outputs/live_dashboard.json"
        
    def categorize_defects_realtime(self, failures: List[Dict]) -> Dict:
        """Real-time defect categorization"""
        categories = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": [],
            "environment": [],
            "flaky": []
        }
        
        for failure in failures:
            test_name = failure.get('test_name', '')
            error_msg = failure.get('error_message', '').lower()
            
            # Critical: Payment, Security, Data Loss
            if any(keyword in test_name.lower() for keyword in ['payment', 'security', 'login', 'auth']):
                categories["critical"].append(self._create_defect_entry(failure, "Critical"))
            
            # Environment: Infrastructure issues
            elif any(keyword in error_msg for keyword in ['connection refused', 'database', 'server', 'network']):
                categories["environment"].append(self._create_defect_entry(failure, "Environment"))
            
            # Flaky: Intermittent issues
            elif any(keyword in error_msg for keyword in ['timeout', 'stale element', 'intermittent']):
                categories["flaky"].append(self._create_defect_entry(failure, "Flaky"))
            
            # High: UI/API core functionality
            elif any(keyword in test_name.lower() for keyword in ['core', 'main', 'primary']):
                categories["high"].append(self._create_defect_entry(failure, "High"))
            
            # Medium: Secondary features
            elif any(keyword in test_name.lower() for keyword in ['secondary', 'optional']):
                categories["medium"].append(self._create_defect_entry(failure, "Medium"))
            
            # Low: Everything else
            else:
                categories["low"].append(self._create_defect_entry(failure, "Low"))
        
        triage_result = {
            "categories": categories,
            "summary": self._generate_summary(categories),
            "triaged_at": datetime.now().isoformat()
        }
        
        self._save_triage(triage_result)
        self._update_dashboard(triage_result)
        
        return triage_result
    
    def get_live_dashboard_data(self) -> Dict:
        """Get current dashboard data"""
        if os.path.exists(self.dashboard_file):
            try:
                with open(self.dashboard_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "total_failures": 0,
            "categories": {},
            "trends": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def generate_triage_report(self) -> Dict:
        """Generate comprehensive triage report"""
        dashboard_data = self.get_live_dashboard_data()
        historical_data = self._load_historical_triage()
        
        report = {
            "current_status": dashboard_data,
            "recommendations": self._generate_recommendations(dashboard_data),
            "action_items": self._generate_action_items(dashboard_data),
            "trends": self._analyze_trends(historical_data),
            "generated_at": datetime.now().isoformat()
        }
        
        return report
    
    def prioritize_fixes(self, defects: List[Dict]) -> List[Dict]:
        """Prioritize defects for fixing"""
        priority_scores = []
        
        for defect in defects:
            score = 0
            severity = defect.get('severity', 'Low')
            
            # Base score by severity
            severity_scores = {"Critical": 100, "High": 75, "Medium": 50, "Low": 25, "Environment": 90, "Flaky": 40}
            score += severity_scores.get(severity, 25)
            
            # Frequency bonus
            if defect.get('frequency', 1) > 3:
                score += 20
            
            # Recent failure penalty
            if self._is_recent_failure(defect.get('last_seen')):
                score += 15
            
            priority_scores.append({**defect, "priority_score": score})
        
        return sorted(priority_scores, key=lambda x: x['priority_score'], reverse=True)
    
    def _create_defect_entry(self, failure: Dict, severity: str) -> Dict:
        """Create standardized defect entry"""
        return {
            "test_name": failure.get('test_name', ''),
            "severity": severity,
            "error_message": failure.get('error_message', '')[:200],  # Truncate
            "first_seen": datetime.now().isoformat(),
            "last_seen": datetime.now().isoformat(),
            "frequency": 1,
            "status": "Open"
        }
    
    def _generate_summary(self, categories: Dict) -> Dict:
        """Generate summary statistics"""
        total = sum(len(defects) for defects in categories.values())
        
        return {
            "total_defects": total,
            "critical_count": len(categories["critical"]),
            "high_count": len(categories["high"]),
            "environment_count": len(categories["environment"]),
            "flaky_count": len(categories["flaky"]),
            "needs_immediate_attention": len(categories["critical"]) + len(categories["high"])
        }
    
    def _generate_recommendations(self, dashboard_data: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        categories = dashboard_data.get('categories', {})
        
        if categories.get('critical', 0) > 0:
            recommendations.append("🚨 Address critical defects immediately")
        
        if categories.get('environment', 0) > 2:
            recommendations.append("🔧 Check environment stability")
        
        if categories.get('flaky', 0) > 5:
            recommendations.append("🔄 Review flaky tests for stability improvements")
        
        if categories.get('high', 0) > 3:
            recommendations.append("⚡ Prioritize high-severity fixes")
        
        return recommendations
    
    def _generate_action_items(self, dashboard_data: Dict) -> List[str]:
        """Generate specific action items"""
        actions = []
        categories = dashboard_data.get('categories', {})
        
        if categories.get('critical', 0) > 0:
            actions.append("Assign critical defects to senior developers")
        
        if categories.get('environment', 0) > 0:
            actions.append("Contact DevOps team for environment issues")
        
        if categories.get('flaky', 0) > 3:
            actions.append("Schedule flaky test analysis session")
        
        return actions
    
    def _analyze_trends(self, historical_data: List[Dict]) -> Dict:
        """Analyze defect trends"""
        if not historical_data:
            return {"trend": "No historical data"}
        
        recent = historical_data[-5:] if len(historical_data) >= 5 else historical_data
        
        total_recent = sum(data.get('summary', {}).get('total_defects', 0) for data in recent)
        avg_defects = total_recent / len(recent) if recent else 0
        
        return {
            "average_defects_per_run": round(avg_defects, 1),
            "trend": "Increasing" if avg_defects > 5 else "Stable",
            "most_common_category": "Environment"  # Simplified
        }
    
    def _is_recent_failure(self, timestamp_str: str) -> bool:
        """Check if failure is recent (within 1 hour)"""
        if not timestamp_str:
            return True
        
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return datetime.now() - timestamp < timedelta(hours=1)
        except:
            return True
    
    def _load_historical_triage(self) -> List[Dict]:
        """Load historical triage data"""
        if os.path.exists(self.triage_file):
            try:
                with open(self.triage_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_triage(self, triage_result: Dict):
        """Save triage result"""
        historical = self._load_historical_triage()
        historical.append(triage_result)
        
        os.makedirs(os.path.dirname(self.triage_file), exist_ok=True)
        with open(self.triage_file, 'w') as f:
            json.dump(historical[-50:], f, indent=2)  # Keep last 50
    
    def _update_dashboard(self, triage_result: Dict):
        """Update live dashboard"""
        summary = triage_result.get('summary', {})
        categories = triage_result.get('categories', {})
        
        dashboard = {
            "total_failures": summary.get('total_defects', 0),
            "categories": {k: len(v) for k, v in categories.items()},
            "last_updated": datetime.now().isoformat(),
            "status": "Critical" if summary.get('critical_count', 0) > 0 else "Normal"
        }
        
        os.makedirs(os.path.dirname(self.dashboard_file), exist_ok=True)
        with open(self.dashboard_file, 'w') as f:
            json.dump(dashboard, f, indent=2)