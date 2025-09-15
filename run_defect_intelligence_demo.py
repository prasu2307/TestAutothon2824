"""
Quick launcher for DefectIntelligence Demo
Standalone demonstration of X-Factor features
"""
import sys
import os

# Add DefectIntelligence to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'DefectIntelligence'))

from DefectIntelligence.demo_runner import demo_defect_intelligence

if __name__ == "__main__":
    print("🚀 Starting DefectIntelligence Demo...")
    print("This demo showcases X-Factor features for TestAutothon2025")
    print()
    
    try:
        demo_defect_intelligence()
    except Exception as e:
        print(f"Demo error: {e}")
        print("Make sure you're running from the TestAutothon2824 root directory")