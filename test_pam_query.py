#!/usr/bin/env python3
"""
Test script for PAM query detection from mohak64bansal@gmail.com
"""

from email_classifier import EmailClassifier

def test_pam_query_detection():
    """Test that only PAM queries from mohak64bansal@gmail.com get responses"""
    classifier = EmailClassifier()
    
    print("=== Testing PAM Query Detection ===")
    print("Only emails from mohak64bansal@gmail.com containing 'query for pam' should get responses")
    print()
    
    # Test emails
    test_emails = [
        {
            'subject': 'Query for PAM solution',
            'body': 'I need information about your PAM product',
            'sender': 'mohak64bansal@gmail.com',
            'should_get_response': True,
            'description': 'PAM query in subject'
        },
        {
            'subject': 'Hello',
            'body': 'I have a query for PAM. Can you help?',
            'sender': 'mohak64bansal@gmail.com',
            'should_get_response': True,
            'description': 'PAM query in body'
        },
        {
            'subject': 'Query for PAM',
            'body': 'Need details about your solution',
            'sender': 'mohak64bansal@gmail.com',
            'should_get_response': True,
            'description': 'PAM query in subject (exact match)'
        },
        {
            'subject': 'Hey there',
            'body': 'Just wanted to say hi',
            'sender': 'mohak64bansal@gmail.com',
            'should_get_response': False,
            'description': 'Regular email from mohak64bansal@gmail.com'
        },
        {
            'subject': 'Query for PAM solution',
            'body': 'I need information about your PAM product',
            'sender': 'someone@example.com',
            'should_get_response': False,
            'description': 'PAM query from different sender'
        },
        {
            'subject': 'General inquiry',
            'body': 'What are your services?',
            'sender': 'customer@company.com',
            'should_get_response': False,
            'description': 'General email from other sender'
        }
    ]
    
    results = []
    
    for i, email in enumerate(test_emails, 1):
        category = classifier.classify_email(
            email['subject'], 
            email['body'], 
            email['sender']
        )
        
        should_get_response = email['should_get_response']
        will_get_response = (category == 'mohak64bansal')
        
        result = {
            'email_num': i,
            'sender': email['sender'],
            'subject': email['subject'],
            'description': email['description'],
            'category': category,
            'should_get_response': should_get_response,
            'will_get_response': will_get_response,
            'correct': (should_get_response == will_get_response)
        }
        
        results.append(result)
        
        print(f"Test {i}: {email['description']}")
        print(f"  Sender: {email['sender']}")
        print(f"  Subject: {email['subject']}")
        print(f"  Body: {email['body'][:50]}...")
        print(f"  Category: {category}")
        print(f"  Should get response: {should_get_response}")
        print(f"  Will get response: {will_get_response}")
        print(f"  Result: {'✅ CORRECT' if result['correct'] else '❌ INCORRECT'}")
        print()
    
    # Summary
    correct_count = sum(1 for r in results if r['correct'])
    total_count = len(results)
    
    print("=== Summary ===")
    print(f"Correct classifications: {correct_count}/{total_count}")
    
    if correct_count == total_count:
        print("🎉 SUCCESS: Only PAM queries from mohak64bansal@gmail.com will get responses!")
    else:
        print("❌ FAILED: Some emails are not being handled correctly")
    
    # Show which emails will get responses
    print("\n=== Emails that WILL get automated responses ===")
    pam_emails = [r for r in results if r['will_get_response']]
    for result in pam_emails:
        print(f"  - Test {result['email_num']}: {result['description']}")
    
    print("\n=== Emails that will NOT get automated responses ===")
    other_emails = [r for r in results if not r['will_get_response']]
    for result in other_emails:
        print(f"  - Test {result['email_num']}: {result['description']}")

if __name__ == "__main__":
    test_pam_query_detection()
