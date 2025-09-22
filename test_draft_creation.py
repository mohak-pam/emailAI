#!/usr/bin/env python3
"""
Test script for draft creation functionality
"""

from email_classifier import EmailClassifier
from gmail_client import GmailClient

def test_draft_creation():
    """Test that drafts are created instead of sending emails"""
    classifier = EmailClassifier()
    gmail_client = GmailClient()
    
    print("=== Testing Draft Creation ===")
    print("PAM queries from mohak64bansal@gmail.com should create drafts")
    print()
    
    # Test email that should create a draft
    test_email = {
        'id': 'test123',
        'thread_id': 'thread123',
        'subject': 'Query for PAM solution',
        'body': 'I need information about your PAM product',
        'sender': 'mohak64bansal@gmail.com'
    }
    
    print("Test Email:")
    print(f"  Sender: {test_email['sender']}")
    print(f"  Subject: {test_email['subject']}")
    print(f"  Body: {test_email['body']}")
    print()
    
    # Classify the email
    category = classifier.classify_email(
        test_email['subject'], 
        test_email['body'], 
        test_email['sender']
    )
    
    print(f"Classification: {category}")
    
    if category == 'mohak64bansal':
        print("✅ Email correctly classified as PAM query")
        
        # Get response template
        response_template = classifier.get_response_template(category)
        print(f"\nResponse Template Preview:")
        print(f'"{response_template[:100]}..."')
        
        # Test draft creation (this will create a real draft in Gmail)
        print(f"\nCreating draft...")
        success = gmail_client.create_draft_reply(test_email, response_template)
        
        if success:
            print("✅ Draft created successfully!")
            print("Check your Gmail drafts folder to review the draft before sending.")
        else:
            print("❌ Failed to create draft")
    else:
        print("❌ Email not classified as PAM query")

if __name__ == "__main__":
    test_draft_creation()
