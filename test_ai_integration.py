#!/usr/bin/env python3
"""
Test AI integration with email automation
"""

from email_automation import EmailAutomation
from gemini_integration import GeminiPAMProcessor

def test_ai_integration():
    """Test AI-enhanced email processing"""
    print("🤖 Testing AI-Enhanced Email Automation")
    print()
    
    try:
        automation = EmailAutomation()
        print("✅ EmailAutomation initialized successfully")
        
        # Test Gemini processor initialization and fallback
        gemini = GeminiPAMProcessor()
        result = gemini.summarize_pam_thread([
            {"sender": "user@example.com", "subject": "Test", "body": "Need help with PAM setup", "date": "2025-10-04"}
        ])
        assert isinstance(result, dict)
        print("✅ Gemini processor returned analysis")
        
        print("✅ All components loaded successfully")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_integration()

