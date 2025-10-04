#!/usr/bin/env python3
"""
Test script for thread-aware email processing
"""

from email_classifier import EmailClassifier
from gmail_client import GmailClient

def test_thread_awareness():
    """Test thread-aware email classification and response generation"""
    classifier = EmailClassifier()
    gmail_client = GmailClient()
    
    print("=== Testing Thread-Aware Email Processing ===")
    print()
    
    # Simulate a thread with multiple emails
    thread_emails = [
        {
            'id': 'email1',
            'subject': 'Initial PAM Inquiry',
            'body': 'Hi, I am interested in learning about your PAM solution for our organization.',
            'sender': 'mohak64bansal@gmail.com',
            'date': '2025-09-22 10:00:00'
        },
        {
            'id': 'email2', 
            'subject': 'Re: Initial PAM Inquiry',
            'body': 'Thank you for your interest. Could you tell me more about your requirements?',
            'sender': 'mohak.bansal@xecurify.com',
            'date': '2025-09-22 10:30:00'
        },
        {
            'id': 'email3',
            'subject': 'Re: Initial PAM Inquiry', 
            'body': 'We need PAM for Windows servers and Linux machines. Also, what is the pricing? This is a query for PAM solution.',
            'sender': 'mohak64bansal@gmail.com',
            'date': '2025-09-22 11:00:00'
        }
    ]
    
    print("Thread Emails:")
    for i, email in enumerate(thread_emails, 1):
        print(f"  {i}. From: {email['sender']}")
        print(f"     Subject: {email['subject']}")
        print(f"     Body: {email['body'][:50]}...")
        print()
    
    # Test thread analysis
    print("=== Thread Analysis ===")
    thread_info = classifier.analyze_thread_context(thread_emails)
    
    if thread_info:
        print(f"Total emails: {thread_info['total_emails']}")
        print(f"Participants: {', '.join(thread_info['participants'])}")
        print(f"Conversation Summary: {thread_info['conversation_summary']}")
        print(f"Key Topics: {[topic[0] for topic in thread_info['topics'][:3]]}")
        print()
    
    # Test classification with thread context
    print("=== Classification with Thread Context ===")
    current_email = thread_emails[-1]  # Last email in thread
    thread_context = thread_emails[:-1]  # Previous emails
    
    category = classifier.classify_email(
        current_email['subject'],
        current_email['body'], 
        current_email['sender'],
        thread_context
    )
    
    print(f"Current email classified as: {category}")
    print()
    
    # Test contextual response generation
    if category == 'mohak64bansal':
        print("=== Contextual Response Generation ===")
        response_template = classifier.get_response_template(category)
        contextual_response = classifier.generate_contextual_response(
            response_template, thread_info, current_email
        )
        
        print("Generated Response:")
        print("-" * 50)
        print(contextual_response)
        print("-" * 50)
        print()
        
        # Test draft creation with thread context
        print("=== Testing Draft Creation with Thread Context ===")
        success = gmail_client.create_draft_reply(current_email, contextual_response)
        
        if success:
            print("✅ Draft created successfully with thread context!")
            print("Check your Gmail drafts folder to see the contextual response.")
        else:
            print("❌ Failed to create draft")
    else:
        print("❌ Email not classified as PAM query")

if __name__ == "__main__":
    test_thread_awareness()
