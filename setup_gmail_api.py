#!/usr/bin/env python3
"""
Setup script for Gmail API credentials
This script helps you set up the Gmail API credentials needed for the automation.
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.modify']

def setup_gmail_api():
    """Setup Gmail API credentials"""
    print("=== Gmail API Setup ===")
    print("This script will help you set up Gmail API credentials.")
    print()
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("Please follow these steps:")
        print("1. Go to https://console.developers.google.com/")
        print("2. Create a new project or select existing one")
        print("3. Enable Gmail API")
        print("4. Create credentials (OAuth 2.0 Client ID)")
        print("5. Download the credentials.json file")
        print("6. Place it in this directory")
        print()
        return False
    
    print("✓ credentials.json found")
    
    # Setup credentials
    creds = None
    token_path = 'token.pickle'
    
    # Load existing token
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    print("✓ Gmail API credentials configured successfully!")
    
    # Test the connection
    try:
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        print(f"✓ Connected to Gmail account: {profile.get('emailAddress')}")
        return True
    except Exception as e:
        print(f"❌ Error testing Gmail connection: {str(e)}")
        return False

def create_env_file():
    """Create .env file from credentials"""
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found. Please run setup first.")
        return False
    
    try:
        with open('credentials.json', 'r') as f:
            creds_data = json.load(f)
        
        client_id = creds_data['installed']['client_id']
        client_secret = creds_data['installed']['client_secret']
        
        env_content = f"""# Gmail API Credentials
GMAIL_CLIENT_ID={client_id}
GMAIL_CLIENT_SECRET={client_secret}
GMAIL_REFRESH_TOKEN=your_refresh_token_here

# Email Settings
AUTO_REPLY_ENABLED=true
CHECK_INTERVAL_MINUTES=5
MAX_EMAILS_PER_CHECK=10

# Response Templates
DEFAULT_RESPONSE_TEMPLATE=Thank you for your email. I have received your message and will get back to you as soon as possible.
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✓ .env file created successfully!")
        print("Please update GMAIL_REFRESH_TOKEN in the .env file after running the setup.")
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {str(e)}")
        return False

def main():
    print("Gmail Email Automation - API Setup")
    print("=" * 40)
    
    # Setup Gmail API
    if setup_gmail_api():
        print()
        # Create .env file
        create_env_file()
        print()
        print("🎉 Setup completed successfully!")
        print()
        print("Next steps:")
        print("1. Update the GMAIL_REFRESH_TOKEN in your .env file")
        print("2. Customize response templates in email_classifier.py if needed")
        print("3. Run: python main.py --mode once (to test)")
        print("4. Run: python main.py --mode continuous (to start automation)")
    else:
        print("❌ Setup failed. Please check the instructions above.")

if __name__ == "__main__":
    main()
