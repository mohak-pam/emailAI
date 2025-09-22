#!/usr/bin/env python3
"""
Test script to verify that only mohak64bansal.com emails get automated responses
"""

from email_classifier import EmailClassifier

def test_selective_responses():
    """Test that only mohak64bansal.com emails get responses"""
    classifier = EmailClassifier()
    
    print("=== Testing Selective Email Responses ===")
    print("Only mohak64bansal@gmail.com emails should get automated responses")
    print()
    
    # Test emails
    test_emails = [
        {
            'subject': 'Hey there!',
            'body': 'Just wanted to say hi',
            'sender': 'mohak64bansal@gmail.com',
            'should_get_response': True
        },
        {
            'subject': 'Pricing Inquiry',
            'body': 'What are your prices?',
            'sender': 'customer@example.com',
            'should_get_response': False
        },
        {
            'subject': 'Need Help',
            'body': 'I have a problem with your service',
            'sender': 'user@company.com',
            'should_get_response': False
        },
        {
            'subject': 'Meeting Request',
            'body': 'Can we schedule a call?',
            'sender': 'prospect@business.org',
            'should_get_response': False
        },
        {
            'subject': 'Another email from Mohak',
            'body': 'This is another email from Mohak',
            'sender': 'mohak64bansal@gmail.com',
            'should_get_response': True
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
            'category': category,
            'should_get_response': should_get_response,
            'will_get_response': will_get_response,
            'correct': (should_get_response == will_get_response)
        }
        
        results.append(result)
        
        print(f"Test {i}:")
        print(f"  Sender: {email['sender']}")
        print(f"  Subject: {email['subject']}")
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
        print("🎉 SUCCESS: Only mohak64bansal.com emails will get automated responses!")
    else:
        print("❌ FAILED: Some emails are not being handled correctly")
    
    # Show which emails will get responses
    print("\n=== Emails that WILL get automated responses ===")
    mohak_emails = [r for r in results if r['will_get_response']]
    for result in mohak_emails:
        print(f"  - Test {result['email_num']}: {result['sender']}")
    
    print("\n=== Emails that will NOT get automated responses ===")
    other_emails = [r for r in results if not r['will_get_response']]
    for result in other_emails:
        print(f"  - Test {result['email_num']}: {result['sender']}")

if __name__ == "__main__":
    test_selective_responses()
