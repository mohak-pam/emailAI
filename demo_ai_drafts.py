#!/usr/bin/env python3
"""
Demo showing AI-enhanced drafts for all emails
"""

from email_automation import EmailAutomation
from gemini_integration import GeminiPAMProcessor

def demo_ai_drafts():
    """Demonstrate AI-enhanced draft creation"""
    print("🤖 === AI-Enhanced Draft Creation Demo ===")
    print()
    
    automation = EmailAutomation()
    gemini = GeminiPAMProcessor()
    
    # Simulate different types of emails
    test_emails = [
        {
            'id': 'demo1',
            'thread_id': 'thread1',
            'subject': 'PAM Configuration Error',
            'body': 'Hi, we are having trouble configuring the PAM solution. Getting authentication errors when trying to set up LDAP integration.',
            'sender': 'admin@company.com',
            'date': '2025-09-22 10:00:00'
        },
        {
            'id': 'demo2',
            'thread_id': 'thread2', 
            'subject': 'Demo Request for PAM Solution',
            'body': 'Hello, we would like to schedule a demo of your PAM solution. We are looking for a comprehensive solution for our enterprise.',
            'sender': 'cto@enterprise.com',
            'date': '2025-09-22 11:00:00'
        },
        {
            'id': 'demo3',
            'thread_id': 'thread3',
            'subject': 'Pricing Inquiry',
            'body': 'Could you please provide pricing information for your PAM solution? We need to protect around 1000 privileged accounts.',
            'sender': 'procurement@bigcorp.com',
            'date': '2025-09-22 12:00:00'
        }
    ]
    
    print("📧 Processing different email types...")
    print()
    
    for i, email in enumerate(test_emails, 1):
        print(f"--- Email {i}: {email['subject']} ---")
        
        # Simulate thread context
        thread_emails = [email]  # Single email for demo
        
        # Get AI analysis
        ai_analysis = gemini.summarize_pam_thread(thread_emails)
        
        # Generate draft
        response = automation._generate_ai_enhanced_draft(email, ai_analysis, None, 'demo')
        
        print(f"AI Analysis: {ai_analysis.get('conversation_type', 'Unknown')} - {ai_analysis.get('urgency_level', 'Unknown')} urgency")
        print(f"Draft Preview: {response[:200]}...")
        print()
    
    print("✅ AI-enhanced drafts would be created for ALL emails!")
    print("📧 Check your Gmail drafts folder to see the actual drafts created.")

if __name__ == "__main__":
    demo_ai_drafts()

