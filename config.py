import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Gmail API Credentials
    GMAIL_CLIENT_ID = os.getenv('GMAIL_CLIENT_ID')
    GMAIL_CLIENT_SECRET = os.getenv('GMAIL_CLIENT_SECRET')
    GMAIL_REFRESH_TOKEN = os.getenv('GMAIL_REFRESH_TOKEN')
    
    # Email Settings
    AUTO_REPLY_ENABLED = os.getenv('AUTO_REPLY_ENABLED', 'true').lower() == 'true'  # Creates drafts instead of sending
    CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', 5))
    MAX_EMAILS_PER_CHECK = int(os.getenv('MAX_EMAILS_PER_CHECK', 10))
    
    # Response Templates
    DEFAULT_RESPONSE_TEMPLATE = os.getenv('DEFAULT_RESPONSE_TEMPLATE', 
        'Thank you for your email. I have received your message and will get back to you as soon as possible.')
    
    # Gmail API Scopes
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
              'https://www.googleapis.com/auth/gmail.send',
              'https://www.googleapis.com/auth/gmail.modify']
