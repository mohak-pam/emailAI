import time
import logging
from datetime import datetime
from gmail_client import GmailClient
from email_classifier import EmailClassifier
from config import Config
from smart_analyzer import SmartEmailAnalyzer
from gemini_integration import GeminiPAMProcessor

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
        self.smart_analyzer = SmartEmailAnalyzer()
        self.gemini = GeminiPAMProcessor()
        self.processed_emails = set()  # Track processed emails to avoid duplicates
        self.logger = logging.getLogger(__name__)
    
    def process_new_emails(self):
        """Process new unread emails and send appropriate responses"""
        try:
            self.logger.info("Checking for new emails...")
            checkpoint = self.gmail_client.load_checkpoint()
            last_ts = (checkpoint or {}).get('last_processed_internal_ts', 0)
            
            # Get unread emails
            emails = self.gmail_client.get_unread_emails(Config.MAX_EMAILS_PER_CHECK)
            if last_ts:
                emails = [e for e in emails if e.get('internal_ts', 0) > last_ts]
            
            if not emails:
                self.logger.info("No new emails found.")
                return
            
            self.logger.info(f"Found {len(emails)} new emails to process.")
            
            max_seen_ts = last_ts
            for email in emails:
                if email['id'] in self.processed_emails:
                    continue
                
                self.process_single_email(email)
                self.processed_emails.add(email['id'])
                if email.get('internal_ts', 0) > max_seen_ts:
                    max_seen_ts = email['internal_ts']
                
                # Small delay between processing emails
                time.sleep(2)

            # Save checkpoint
            if max_seen_ts and max_seen_ts > last_ts:
                self.gmail_client.save_checkpoint(max_seen_ts)
            
        except Exception as e:
            self.logger.error(f"Error processing emails: {str(e)}")
    
    def process_single_email(self, email):
        """Process a single email and send response if appropriate"""
        try:
            self.logger.info(f"Processing email: {email['subject']} from {email['sender']}")
            
            # Check if this email is TO configured target
            if not self._is_email_to_target(email):
                self.logger.info(f"Email not addressed to {Config.TARGET_EMAIL} - skipping")
                if Config.MARK_AS_READ:
                    self.gmail_client.mark_as_read(email['id'])
                return
            
            # Get thread context if available
            thread_context = None
            thread_info = None
            ai_analysis = None
            if email.get('thread_id'):
                thread_emails = self.gmail_client.get_thread_emails(email['thread_id'])
                if thread_emails:
                    # Always use full thread for Gemini analysis
                    thread_context = thread_emails[:-1] if len(thread_emails) > 1 else None
                    thread_info = self.classifier.analyze_thread_context(thread_emails)
                    self.logger.info(f"Calling Gemini for thread analysis (emails_in_thread={len(thread_emails)})")
                    ai_analysis = self.gemini.summarize_pam_thread(thread_emails)
                    self.logger.info(f"AI Analysis: {ai_analysis.get('type', 'Unknown')} - {ai_analysis.get('urgency', 'Unknown')} urgency")
            
            # Classify the email with thread context
            category = self.classifier.classify_email(email['subject'], email['body'], email['sender'], thread_context)
            self.logger.info(f"Email classified as: {category}")
            
            # Check if this is an auto-reply or from a no-reply address
            if self.should_skip_email(email):
                self.logger.info("Skipping email (auto-reply or no-reply)")
                if Config.MARK_AS_READ:
                    self.gmail_client.mark_as_read(email['id'])
                return
            
            # Generate support-grade reply via Gemini only; skip if none
            response = None
            full_thread = self.gmail_client.get_thread_emails(email['thread_id']) if email.get('thread_id') else [email]
            self.logger.info("Requesting Gemini-generated reply for draft")
            response = self.gemini.generate_support_reply(email, full_thread)
            if not response:
                self.logger.warning("Gemini did not return a reply. Skipping draft creation for this email.")
                return
            # Append local signature block
            signature = f"\n\nBest regards,\n{Config.SIGNATURE_NAME}\n{Config.SIGNATURE_TITLE}\n{Config.SIGNATURE_COMPANY}"
            response = response.strip() + signature
            
            # Create draft
            if Config.AUTO_REPLY_ENABLED:
                success = self.gmail_client.create_draft_reply(email, response)
                if success:
                    self.logger.info(f"Draft created for {category} email: {email['subject']}")
                    if ai_analysis:
                        self.logger.info(f"Thread analysis: {ai_analysis.get('type', 'Unknown')} - {ai_analysis.get('urgency', 'Unknown')} urgency")
                    # Mark as read after successful draft creation
                    if Config.MARK_AS_READ:
                        self.gmail_client.mark_as_read(email['id'])
                else:
                    self.logger.error(f"Failed to create draft for email: {email['subject']}")
                    if Config.MARK_AS_READ:
                        self.gmail_client.mark_as_read(email['id'])
            else:
                self.logger.info("Auto-reply is disabled. Email processed but no draft created.")
                if Config.MARK_AS_READ:
                    self.gmail_client.mark_as_read(email['id'])
            
        except Exception as e:
            self.logger.error(f"Error processing email {email['id']}: {str(e)}")
    
    def _is_email_to_target(self, email):
        """Check if email is addressed to configured TARGET_EMAIL"""
        to_field = email.get('to', '')
        return Config.TARGET_EMAIL.lower() in to_field.lower()
    
    def _generate_contextual_response(self, email, ai_analysis, thread_info, category):
        """Generate contextual response for emails TO mohak"""
        # Create a professional response based on analysis
        response = f"""Hello,

Thank you for your email regarding "{email['subject']}".

"""
        
        if ai_analysis:
            # Add context based on analysis
            if ai_analysis.get('type') == 'error':
                response += """I understand you're experiencing technical issues. I'll review the details and provide assistance to resolve this matter.

"""
            elif ai_analysis.get('type') == 'meeting':
                response += """I'd be happy to schedule a meeting to discuss this further. Please let me know your availability.

"""
            elif ai_analysis.get('type') == 'support':
                response += """I'll review your support request and ensure you receive the appropriate assistance.

"""
            elif ai_analysis.get('type') == 'sales':
                response += """Thank you for your interest in our services. I'll prepare the relevant information for you.

"""
            
            # Add urgency context
            urgency = ai_analysis.get('urgency', 'low')
            if urgency == 'high':
                response += """Given the urgency of this matter, I'll prioritize this and respond promptly.

"""
            elif urgency == 'medium':
                response += """I'll address this matter with appropriate priority.

"""
        
        response += """I'll review the full thread context and provide a comprehensive response shortly.

Best regards,
Mohak Bansal
miniOrange Team"""
        
        return response
    
    def _generate_ai_enhanced_draft(self, email, ai_analysis, thread_info, category):
        """Generate AI-enhanced draft with industry-standard thread analysis"""
        # Create a professional draft with comprehensive AI insights
        draft_content = f"""📧 AI-ENHANCED EMAIL DRAFT
═══════════════════════════════════════════════════════════════

📋 EXECUTIVE SUMMARY
{ai_analysis.get('executive_summary', 'Email thread analysis')}

📊 CONVERSATION ANALYSIS
┌─────────────────────────────────────────────────────────────┐
│ Type: {ai_analysis.get('type', 'Unknown').title():<20} │
│ Urgency: {ai_analysis.get('urgency', 'Unknown').title():<15} │
│ Sentiment: {ai_analysis.get('sentiment', 'Unknown').title():<12} │
│ Complexity: {ai_analysis.get('complexity', 'Unknown').title():<10} │
│ Business Impact: {ai_analysis.get('business_impact', 'Unknown').title():<8} │
└─────────────────────────────────────────────────────────────┘

🎯 KEY ISSUES & REQUIREMENTS
{chr(10).join([f"• {issue}" for issue in ai_analysis.get('issues', ['None identified'])])}

👥 STAKEHOLDERS INVOLVED
{', '.join(ai_analysis.get('stakeholders', ['Unknown']))}

⏰ TIMELINE & URGENCY
• Response Expected: {ai_analysis.get('response_time', 'Unknown').replace('_', ' ').title()}
• Escalation Needed: {'Yes' if ai_analysis.get('escalation', False) else 'No'}
• Business Impact: {ai_analysis.get('business_impact', 'Unknown').title()}

💡 RECOMMENDED RESPONSE STRATEGY
Based on {ai_analysis.get('type', 'general')} conversation with {ai_analysis.get('urgency', 'low')} urgency

✅ RECOMMENDED ACTIONS
{chr(10).join([f"• {action}" for action in ai_analysis.get('recommended_actions', ['Review and respond manually'])])}

📧 ORIGINAL EMAIL CONTENT
Subject: {email['subject']}
From: {email['sender']}
Category: {category}

Body Preview:
{email['body'][:300]}{'...' if len(email['body']) > 300 else ''}

--- Thread Context ---"""
        
        if thread_info:
            draft_content += f"""
Total Emails in Thread: {thread_info.get('total_emails', 'Unknown')}
Conversation Summary: {thread_info.get('conversation_summary', 'No summary available')}
Key Topics: {[topic[0] for topic in thread_info.get('topics', [])[:3]]}
Participants: {', '.join(thread_info.get('participants', []))}"""
        
        draft_content += f"""

═══════════════════════════════════════════════════════════════
🤖 Generated by AI Email Assistant - {ai_analysis.get('type', 'Unknown').title()} Analysis
═══════════════════════════════════════════════════════════════
"""
        
        return draft_content
    
    def _generate_basic_draft(self, email, thread_info, category):
        """Generate basic draft without AI analysis"""
        draft_content = f"""--- Basic Email Draft ---
        
Original Email: {email['subject']}
From: {email['sender']}
Category: {category}

--- Thread Context ---"""
        
        if thread_info:
            draft_content += f"""
Total Emails in Thread: {thread_info.get('total_emails', 'Unknown')}
Conversation Summary: {thread_info.get('conversation_summary', 'No summary available')}
Key Topics: {[topic[0] for topic in thread_info.get('topics', [])[:3]]}
Participants: {', '.join(thread_info.get('participants', []))}"""
        
        draft_content += f"""

--- Original Email Content ---
Subject: {email['subject']}
Body: {email['body'][:500]}{'...' if len(email['body']) > 500 else ''}

--- End of Basic Analysis ---
"""
        
        return draft_content
    
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

    def process_emails_to_target(self, max_results: int | None = None):
        """Process all emails addressed to Config.TARGET_EMAIL with full thread analysis and create drafts."""
        try:
            self.logger.info(f"Searching for emails addressed to {Config.TARGET_EMAIL} ...")
            checkpoint = self.gmail_client.load_checkpoint()
            last_ts = (checkpoint or {}).get('last_processed_internal_ts', 0)
            query = f"to:{Config.TARGET_EMAIL} -category:spam"
            if last_ts:
                emails = self.gmail_client.search_emails_since(query, last_ts, max_results or Config.MAX_EMAILS_PER_CHECK)
            else:
                emails = self.gmail_client.search_emails(query, max_results or Config.MAX_EMAILS_PER_CHECK)

            if not emails:
                self.logger.info(f"No emails found addressed to {Config.TARGET_EMAIL}.")
                return

            max_seen_ts = last_ts
            for email in emails:
                if email['id'] in self.processed_emails:
                    continue

                # Fetch full thread
                thread_emails = self.gmail_client.get_thread_emails(email['thread_id']) if email.get('thread_id') else [email]

                # Determine if reply is needed (skip auto-replies, no-reply, etc.)
                if self.should_skip_email(email):
                    self.logger.info("Skipping email (auto-reply or no-reply)")
                    if Config.MARK_AS_READ:
                        self.gmail_client.mark_as_read(email['id'])
                    continue

                # Analyze with Gemini using full thread
                ai_analysis = self.gemini.summarize_pam_thread(thread_emails)
                thread_info = self.classifier.analyze_thread_context(thread_emails)

                # Build response
                response = self._generate_contextual_response(email, ai_analysis, thread_info, self.classifier.classify_email(email['subject'], email['body'], email['sender'], thread_emails[:-1] if len(thread_emails) > 1 else None))

                # Create draft
                if Config.AUTO_REPLY_ENABLED:
                    success = self.gmail_client.create_draft_reply(email, response)
                    if success:
                        self.logger.info(f"Draft created for email: {email['subject']}")
                        if Config.MARK_AS_READ:
                            self.gmail_client.mark_as_read(email['id'])
                else:
                    self.logger.info("Auto-reply is disabled. Email processed but no draft created.")

                self.processed_emails.add(email['id'])
                if email.get('internal_ts', 0) > max_seen_ts:
                    max_seen_ts = email['internal_ts']
                time.sleep(1)
            # Save checkpoint
            if max_seen_ts and max_seen_ts > last_ts:
                self.gmail_client.save_checkpoint(max_seen_ts)
        except Exception as e:
            self.logger.error(f"Error processing target emails: {str(e)}")
