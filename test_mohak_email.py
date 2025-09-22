#!/usr/bin/env python3
"""
Test script for mohak64bansal.com email classification
"""

from email_classifier import EmailClassifier

def test_mohak_email():
    """Test email classification for mohak64bansal.com emails"""
    classifier = EmailClassifier()
    
    # Test email from mohak64bansal@gmail.com
    test_email = {
        'subject': 'Hey there!',
        'body': 'Just wanted to say hi and see how you are doing.',
        'sender': 'mohak64bansal@gmail.com'
    }
    
    print("=== Testing mohak64bansal@gmail.com Email Classification ===")
    print()
    
    # Classify the email
    category = classifier.classify_email(
        test_email['subject'], 
        test_email['body'], 
        test_email['sender']
    )
    
    print(f"Email Subject: {test_email['subject']}")
    print(f"Email Body: {test_email['body']}")
    print(f"Email Sender: {test_email['sender']}")
    print(f"Classified as: {category}")
    print()
    
    # Get the response template
    response = classifier.get_response_template(category)
    print(f"Response Template:")
    print(f'"{response}"')
    print()
    
    # Test with different sender to ensure it doesn't trigger
    test_email2 = {
        'subject': 'Hey there!',
        'body': 'Just wanted to say hi and see how you are doing.',
        'sender': 'someone@example.com'
    }
    
    category2 = classifier.classify_email(
        test_email2['subject'], 
        test_email2['body'], 
        test_email2['sender']
    )
    
    print("=== Testing with different sender ===")
    print(f"Email Sender: {test_email2['sender']}")
    print(f"Classified as: {category2}")
    print()
    
    # Test with old domain to make sure it doesn't trigger
    test_email3 = {
        'subject': 'Hey there!',
        'body': 'Just wanted to say hi and see how you are doing.',
        'sender': 'mohak@mohak64bansal.com'
    }
    
    category3 = classifier.classify_email(
        test_email3['subject'], 
        test_email3['body'], 
        test_email3['sender']
    )
    
    print("=== Testing with old domain (should not trigger) ===")
    print(f"Email Sender: {test_email3['sender']}")
    print(f"Classified as: {category3}")
    print()
    
    if category == 'mohak64bansal' and category2 != 'mohak64bansal' and category3 != 'mohak64bansal':
        print("✅ SUCCESS: mohak64bansal@gmail.com emails are correctly identified!")
        print("✅ SUCCESS: Other emails are not incorrectly classified!")
        print("✅ SUCCESS: Old domain emails are not triggering!")
    else:
        print("❌ FAILED: Email classification not working correctly")

if __name__ == "__main__":
    test_mohak_email()
