import time
import logging
from datetime import datetime
from gmail_client import GmailClient
from email_classifier import EmailClassifier
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_automation.log'),
        logging.StreamHandler()
    ]
)

class EmailAutomation:
    def __init__(self):
        self.gmail_client = GmailClient()
        self.classifier = EmailClassifier()
        self.processed_emails = set()  # Track processed emails to avoid duplicates
        self.logger = logging.getLogger(__name__)
    
    def process_new_emails(self):
        """Process new unread emails and send appropriate responses"""
        try:
            self.logger.info("Checking for new emails...")
            
            # Get unread emails
            emails = self.gmail_client.get_unread_emails(Config.MAX_EMAILS_PER_CHECK)
            
            if not emails:
                self.logger.info("No new emails found.")
                return
            
            self.logger.info(f"Found {len(emails)} new emails to process.")
            
            for email in emails:
                if email['id'] in self.processed_emails:
                    continue
                
                self.process_single_email(email)
                self.processed_emails.add(email['id'])
                
                # Small delay between processing emails
                time.sleep(2)
            
        except Exception as e:
            self.logger.error(f"Error processing emails: {str(e)}")
    
    def process_single_email(self, email):
        """Process a single email and send response if appropriate"""
        try:
            self.logger.info(f"Processing email: {email['subject']} from {email['sender']}")
            
            # Classify the email
            category = self.classifier.classify_email(email['subject'], email['body'], email['sender'])
            self.logger.info(f"Email classified as: {category}")
            
            # Check if this is an auto-reply or from a no-reply address
            if self.should_skip_email(email):
                self.logger.info("Skipping email (auto-reply or no-reply)")
                self.gmail_client.mark_as_read(email['id'])
                return
            
            # Only create drafts for mohak64bansal.com emails
            if category == 'mohak64bansal':
                # Get response template
                response_template = self.classifier.get_response_template(category)
                
                # Customize response
                response = self.customize_response(response_template, email)
                
                # Create draft instead of sending
                if Config.AUTO_REPLY_ENABLED:
                    success = self.gmail_client.create_draft_reply(email, response)
                    if success:
                        self.logger.info(f"Draft created successfully for mohak64bansal.com email: {email['subject']}")
                        # Mark as read after successful draft creation
                        self.gmail_client.mark_as_read(email['id'])
                    else:
                        self.logger.error(f"Failed to create draft for mohak64bansal.com email: {email['subject']}")
                else:
                    self.logger.info("Auto-reply is disabled. mohak64bansal.com email processed but no draft created.")
                    self.gmail_client.mark_as_read(email['id'])
            else:
                # For all other emails, just mark as read without sending response
                self.logger.info(f"No automated response for {category} email from {email['sender']}. Marking as read.")
                self.gmail_client.mark_as_read(email['id'])
            
        except Exception as e:
            self.logger.error(f"Error processing email {email['id']}: {str(e)}")
    
    def should_skip_email(self, email):
        """Determine if an email should be skipped (auto-replies, no-reply addresses, etc.)"""
        sender = email['sender'].lower()
        subject = email['subject'].lower()
        
        # Skip auto-replies
        auto_reply_indicators = [
            'auto-reply', 'automatic reply', 'out of office', 'vacation',
            'away message', 'no-reply', 'noreply', 'donotreply'
        ]
        
        for indicator in auto_reply_indicators:
            if indicator in sender or indicator in subject:
                return True
        
        # Skip emails from no-reply addresses
        if 'no-reply' in sender or 'noreply' in sender or 'donotreply' in sender:
            return True
        
        return False
    
    def customize_response(self, template, email):
        """Customize response template with email-specific information"""
        response = template
        
        # Extract sender name from email address
        sender_name = self.extract_sender_name(email['sender'])
        
        # Replace placeholders
        response = response.replace('[Your Name]', 'Your Assistant')
        
        # Add email-specific customization
        if 'pricing' in template.lower():
            # Add specific pricing information if available
            response += "\n\nNote: Please reply with your specific requirements for a detailed quote."
        
        return response
    
    def extract_sender_name(self, sender_email):
        """Extract sender name from email address"""
        # Extract name from "Name <email@domain.com>" format
        if '<' in sender_email and '>' in sender_email:
            name_part = sender_email.split('<')[0].strip()
            if name_part:
                return name_part
        
        # Extract name from email address
        email_part = sender_email.split('<')[-1].split('>')[0]
        if '@' in email_part:
            name = email_part.split('@')[0]
            return name.replace('.', ' ').replace('_', ' ').title()
        
        return sender_email
    
    def run_continuous(self):
        """Run the automation continuously"""
        self.logger.info("Starting email automation...")
        self.logger.info(f"Check interval: {Config.CHECK_INTERVAL_MINUTES} minutes")
        self.logger.info(f"Auto-draft enabled: {Config.AUTO_REPLY_ENABLED}")
        
        while True:
            try:
                self.process_new_emails()
                self.logger.info(f"Waiting {Config.CHECK_INTERVAL_MINUTES} minutes before next check...")
                time.sleep(Config.CHECK_INTERVAL_MINUTES * 60)
            except KeyboardInterrupt:
                self.logger.info("Email automation stopped by user.")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error: {str(e)}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def run_once(self):
        """Run the automation once"""
        self.logger.info("Running email automation once...")
        self.process_new_emails()
        self.logger.info("Email automation completed.")
