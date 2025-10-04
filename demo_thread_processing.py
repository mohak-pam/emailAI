#!/usr/bin/env python3
"""
Demo script showing thread-aware email processing with draft generation
"""

from email_classifier import EmailClassifier
from gmail_client import GmailClient
import time

def demo_thread_processing():
    """Demonstrate thread-aware email processing with draft generation"""
    print("🚀 === THREAD-AWARE EMAIL PROCESSING DEMO ===")
    print()
    
    classifier = EmailClassifier()
    gmail_client = GmailClient()
    
    # Simulate a realistic email thread with PAM discussion
    print("📧 === SIMULATED EMAIL THREAD ===")
    print()
    
    thread_emails = [
        {
            'id': 'thread_email_1',
            'thread_id': 'thread_12345',
            'subject': 'PAM Solution Inquiry',
            'body': 'Hi Mohak,\n\nI hope you are doing well. I am reaching out to inquire about your PAM (Privileged Access Management) solution for our organization.\n\nWe are looking for a comprehensive PAM solution that can help us manage privileged accounts across our Windows and Linux infrastructure.\n\nCould you please provide more information about your PAM capabilities?\n\nBest regards,\nJohn Smith\nIT Director',
            'sender': 'john.smith@company.com',
            'date': '2025-09-22 09:00:00'
        },
        {
            'id': 'thread_email_2',
            'thread_id': 'thread_12345', 
            'subject': 'Re: PAM Solution Inquiry',
            'body': 'Hello John,\n\nThank you for your interest in our PAM solution. I would be happy to assist you with this.\n\nBefore we proceed, could you please share:\n1. The number of privileged accounts you need to manage\n2. Your current infrastructure setup\n3. Any specific compliance requirements\n\nI will prepare a detailed proposal based on your requirements.\n\nBest regards,\nMohak Bansal\nminiOrange Team',
            'sender': 'mohak.bansal@xecurify.com',
            'date': '2025-09-22 10:30:00'
        },
        {
            'id': 'thread_email_3',
            'thread_id': 'thread_12345',
            'subject': 'Re: PAM Solution Inquiry', 
            'body': 'Hi Mohak,\n\nThank you for your quick response. Here are the details:\n\n1. We have approximately 500 privileged accounts to manage\n2. Our infrastructure includes:\n   - 50 Windows servers\n   - 30 Linux servers\n   - 10 network devices\n   - 5 database servers\n\n3. We need to comply with SOX and PCI-DSS requirements\n\nWe are also interested in session recording and monitoring capabilities.\n\nWhat would be the pricing for such a setup? Also, do you offer on-premise deployment?\n\nBest regards,\nJohn Smith',
            'sender': 'john.smith@company.com',
            'date': '2025-09-22 14:15:00'
        },
        {
            'id': 'thread_email_4',
            'thread_id': 'thread_12345',
            'subject': 'Re: PAM Solution Inquiry',
            'body': 'Hello John,\n\nThank you for the detailed information. Based on your requirements, I can see that our PAM solution would be a perfect fit.\n\nI will prepare a comprehensive proposal including:\n- Detailed pricing for 500 accounts\n- On-premise deployment options\n- SOX and PCI-DSS compliance features\n- Session recording and monitoring capabilities\n\nI will send this to you by tomorrow. Would you be available for a demo call this week?\n\nBest regards,\nMohak Bansal',
            'sender': 'mohak.bansal@xecurify.com',
            'date': '2025-09-22 16:45:00'
        },
        {
            'id': 'thread_email_5',
            'thread_id': 'thread_12345',
            'subject': 'Re: PAM Solution Inquiry',
            'body': 'Hi Mohak,\n\nThis is a query for PAM solution. I have a few more questions:\n\n1. What is the implementation timeline?\n2. Do you provide training for our team?\n3. What kind of support do you offer post-implementation?\n4. Can we get a trial version to test the solution?\n\nAlso, our CTO would like to join the demo call if possible.\n\nLooking forward to your response.\n\nBest regards,\nMohak Bansal',
            'sender': 'mohak64bansal@gmail.com',
            'date': '2025-09-22 17:30:00'
        }
    ]
    
    # Display the thread
    print("📋 Thread Overview:")
    for i, email in enumerate(thread_emails, 1):
        print(f"  {i}. [{email['date']}] From: {email['sender']}")
        print(f"     Subject: {email['subject']}")
        print(f"     Preview: {email['body'][:80]}...")
        print()
    
    # Simulate processing the latest email (which contains "query for pam")
    print("🔍 === PROCESSING LATEST EMAIL ===")
    print()
    
    current_email = thread_emails[-1]  # Latest email
    thread_context = thread_emails[:-1]  # Previous emails
    
    print(f"Processing: {current_email['subject']}")
    print(f"From: {current_email['sender']}")
    print(f"Thread has {len(thread_context)} previous emails")
    print()
    
    # Analyze thread context
    print("🧠 === THREAD ANALYSIS ===")
    thread_info = classifier.analyze_thread_context(thread_emails)
    
    if thread_info:
        print(f"📊 Thread Statistics:")
        print(f"   • Total emails: {thread_info['total_emails']}")
        print(f"   • Participants: {', '.join(thread_info['participants'])}")
        print(f"   • Conversation Summary: {thread_info['conversation_summary']}")
        print(f"   • Key Topics: {[topic[0] for topic in thread_info['topics'][:5]]}")
        print()
    
    # Classify email with thread context
    print("🎯 === EMAIL CLASSIFICATION ===")
    category = classifier.classify_email(
        current_email['subject'],
        current_email['body'],
        current_email['sender'],
        thread_context
    )
    
    print(f"Classification Result: {category}")
    print()
    
    if category == 'mohak64bansal':
        print("✅ PAM Query Detected! Generating contextual response...")
        print()
        
        # Generate contextual response
        response_template = classifier.get_response_template(category)
        contextual_response = classifier.generate_contextual_response(
            response_template, thread_info, current_email
        )
        
        print("📝 === GENERATED DRAFT RESPONSE ===")
        print("=" * 60)
        print(contextual_response)
        print("=" * 60)
        print()
        
        # Create draft
        print("💾 === CREATING DRAFT ===")
        success = gmail_client.create_draft_reply(current_email, contextual_response)
        
        if success:
            print("✅ Draft created successfully!")
            print("📧 Check your Gmail drafts folder to see the contextual response.")
            print()
            
            # Show what makes this response contextual
            print("🎯 === CONTEXTUAL FEATURES ===")
            print("This response is contextual because it includes:")
            print("• Thread conversation summary")
            print("• Total number of emails in thread")
            print("• Key topics discussed")
            print("• Understanding of the ongoing conversation")
            print("• Appropriate response based on thread history")
        else:
            print("❌ Failed to create draft")
    else:
        print("❌ Email not classified as PAM query")
    
    print()
    print("🎉 === DEMO COMPLETED ===")
    print("The system successfully:")
    print("• Read and analyzed the entire email thread")
    print("• Understood the conversation context")
    print("• Detected the PAM query in the latest email")
    print("• Generated a contextual response with thread information")
    print("• Created a draft for your review")

if __name__ == "__main__":
    demo_thread_processing()
