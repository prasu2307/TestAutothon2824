"""
Demo Runner for DefectIntelligence Features
Standalone demonstration without affecting existing tests
"""
from defect_predictor import DefectPredictor
from root_cause_analyzer import RootCauseAnalyzer
from defect_triage import DefectTriage
import json


def demo_defect_intelligence():
    """Demonstrate all DefectIntelligence features"""
    print("🤖 DefectIntelligence Demo - TestAutothon2025 X-Factor")
    print("=" * 60)
    
    # Initialize components
    predictor = DefectPredictor()
    analyzer = RootCauseAnalyzer()
    triage = DefectTriage()
    
    # Demo test names
    test_cases = [
        "test_ui_login_chrome",
        "test_api_payment_gateway",
        "test_mobile_checkout_android",
        "test_visual_homepage_validation"
    ]
    
    print("\n1. 🔮 AI-Powered Defect Prediction")
    print("-" * 40)
    for test in test_cases:
        prediction = predictor.predict_failure_probability(test)
        print(f"Test: {test}")
        print(f"  Failure Probability: {prediction['failure_probability']*100:.1f}%")
        print(f"  Risk Factors: {', '.join(prediction['risk_factors'])}")
        
        fixes = predictor.suggest_preemptive_fixes(test)
        print(f"  Suggested Fixes: {', '.join(fixes)}")
        print()
    
    # Simulate some failures for analysis
    sample_failures = [
        {
            "test_name": "test_ui_login_chrome",
            "error_message": "TimeoutException: Element not clickable",
            "stack_trace": "selenium.common.exceptions.TimeoutException"
        },
        {
            "test_name": "test_api_payment_gateway", 
            "error_message": "ConnectionError: Connection refused",
            "stack_trace": "requests.exceptions.ConnectionError"
        },
        {
            "test_name": "test_mobile_checkout_android",
            "error_message": "AssertionError: Expected 'Success' but was 'Failed'",
            "stack_trace": "AssertionError in test validation"
        }
    ]
    
    print("\n2. 🔍 Real-Time Root Cause Analysis")
    print("-" * 40)
    for failure in sample_failures:
        analysis = analyzer.analyze_failure_instantly(failure)
        print(f"Test: {analysis['test_name']}")
        print(f"  Root Cause: {analysis['root_cause']}")
        print(f"  Fix Suggestion: {analysis['fix_suggestion']}")
        print(f"  Confidence: {analysis['confidence']*100:.0f}%")
        print(f"  Category: {analysis['error_category']}")
        print()
    
    print("\n3. 📊 Live Defect Triage Dashboard")
    print("-" * 40)
    triage_result = triage.categorize_defects_realtime(sample_failures)
    
    print("Defect Categories:")
    for category, defects in triage_result['categories'].items():
        if defects:
            print(f"  {category.upper()}: {len(defects)} defects")
            for defect in defects:
                print(f"    - {defect['test_name']} ({defect['severity']})")
    
    summary = triage_result['summary']
    print(f"\nSummary:")
    print(f"  Total Defects: {summary['total_defects']}")
    print(f"  Needs Immediate Attention: {summary['needs_immediate_attention']}")
    
    # Generate comprehensive report
    print("\n4. 📈 Comprehensive Triage Report")
    print("-" * 40)
    report = triage.generate_triage_report()
    
    print("Recommendations:")
    for rec in report['recommendations']:
        print(f"  {rec}")
    
    print("\nAction Items:")
    for action in report['action_items']:
        print(f"  • {action}")
    
    print(f"\n✅ Demo completed! Check Outputs/ folder for generated data files.")
    print(f"📁 Files created:")
    print(f"  - defect_history.json (Prediction data)")
    print(f"  - defect_predictions.json (AI predictions)")
    print(f"  - root_cause_analysis.json (Analysis results)")
    print(f"  - defect_triage.json (Triage history)")
    print(f"  - live_dashboard.json (Dashboard data)")


if __name__ == "__main__":
    demo_defect_intelligence()