#!/usr/bin/env python3
"""
Test script for email classification
This script helps you test the email classification system with sample emails.
"""

from email_classifier import EmailClassifier

def test_classification():
    """Test email classification with sample emails"""
    classifier = EmailClassifier()
    
    # Sample test emails
    test_emails = [
        {
            'subject': 'Pricing Inquiry',
            'body': 'Hi, I am interested in your services. Could you please provide me with pricing information?',
            'expected': 'pricing'
        },
        {
            'subject': 'Need Help',
            'body': 'I am having trouble with the software. It keeps crashing when I try to save files.',
            'expected': 'support'
        },
        {
            'subject': 'Product Information',
            'body': 'What features does your product have? I would like to know more about its capabilities.',
            'expected': 'product_info'
        },
        {
            'subject': 'Schedule a Meeting',
            'body': 'Hello, I would like to schedule a demo call for next week. When are you available?',
            'expected': 'meeting'
        },
        {
            'subject': 'General Inquiry',
            'body': 'Good morning! I hope you are doing well. I have some questions about your company.',
            'expected': 'general_inquiry'
        },
        {
            'subject': 'Random Email',
            'body': 'This is a random email that should be classified as default.',
            'expected': 'default'
        }
    ]
    
    print("=== Email Classification Test ===")
    print()
    
    correct_predictions = 0
    total_predictions = len(test_emails)
    
    for i, email in enumerate(test_emails, 1):
        predicted = classifier.classify_email(email['subject'], email['body'])
        expected = email['expected']
        
        status = "✓" if predicted == expected else "✗"
        if predicted == expected:
            correct_predictions += 1
        
        print(f"Test {i}: {status}")
        print(f"  Subject: {email['subject']}")
        print(f"  Body: {email['body'][:50]}...")
        print(f"  Expected: {expected}")
        print(f"  Predicted: {predicted}")
        print()
    
    accuracy = (correct_predictions / total_predictions) * 100
    print(f"=== Results ===")
    print(f"Correct predictions: {correct_predictions}/{total_predictions}")
    print(f"Accuracy: {accuracy:.1f}%")
    
    if accuracy < 80:
        print("\n⚠️  Low accuracy detected. Consider:")
        print("- Adding more specific patterns to query_patterns")
        print("- Improving text preprocessing")
        print("- Adding more training examples")

def test_response_templates():
    """Test response template generation"""
    classifier = EmailClassifier()
    
    print("\n=== Response Template Test ===")
    print()
    
    categories = ['pricing', 'support', 'product_info', 'meeting', 'general_inquiry', 'default']
    
    for category in categories:
        template = classifier.get_response_template(category)
        print(f"Category: {category}")
        print(f"Template preview: {template[:100]}...")
        print()

if __name__ == "__main__":
    test_classification()
    test_response_templates()
