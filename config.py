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
    MARK_AS_READ = os.getenv('MARK_AS_READ', 'false').lower() == 'true'

    # Processing checkpoint (to resume from last processed point)
    CHECKPOINT_ENABLED = os.getenv('CHECKPOINT_ENABLED', 'true').lower() == 'true'
    CHECKPOINT_PATH = os.getenv('CHECKPOINT_PATH', 'state.json')
    
    # Response Templates
    DEFAULT_RESPONSE_TEMPLATE = os.getenv('DEFAULT_RESPONSE_TEMPLATE', 
        'Thank you for your email. I have received your message and will get back to you as soon as possible.')
    
    # Gmail API Scopes
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
              'https://www.googleapis.com/auth/gmail.send',
              'https://www.googleapis.com/auth/gmail.modify']

    # Gemini AI
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
    GEMINI_TEMPERATURE = float(os.getenv('GEMINI_TEMPERATURE', 0.3))
    GEMINI_TOP_P = float(os.getenv('GEMINI_TOP_P', 0.9))
    GEMINI_MAX_OUTPUT_TOKENS = int(os.getenv('GEMINI_MAX_OUTPUT_TOKENS', 256))

    # Target recipient email to process
    TARGET_EMAIL = os.getenv('TARGET_EMAIL', 'mohak.bansal@xecurify.com')

    # Signature (appended locally to save AI tokens)
    SIGNATURE_NAME = os.getenv('SIGNATURE_NAME', 'Mohak Bansal')
    SIGNATURE_TITLE = os.getenv('SIGNATURE_TITLE', 'Software Engineer')
    SIGNATURE_COMPANY = os.getenv('SIGNATURE_COMPANY', 'miniOrange')

    # Context limits
    MAX_THREAD_EMAILS = int(os.getenv('MAX_THREAD_EMAILS', 10))
    MAX_THREAD_CHARS = int(os.getenv('MAX_THREAD_CHARS', 6000))

    # Cost safeguards
    MAX_GEMINI_CALLS_PER_RUN = int(os.getenv('MAX_GEMINI_CALLS_PER_RUN', 10))
    GEMINI_REPLY_CACHE_PATH = os.getenv('GEMINI_REPLY_CACHE_PATH', 'reply_cache.json')
