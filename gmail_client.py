import base64
import json
import pickle
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import Config

class GmailClient:
    def __init__(self):
        self.service = None
        self.credentials = None
        self.setup_credentials()
    
    def setup_credentials(self):
        """Setup Gmail API credentials"""
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
                # Create credentials.json if it doesn't exist
                if not os.path.exists('credentials.json'):
                    self.create_credentials_file()
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', Config.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        self.credentials = creds
        self.service = build('gmail', 'v1', credentials=creds)
    
    def create_credentials_file(self):
        """Create credentials.json file from environment variables"""
        credentials_data = {
            "installed": {
                "client_id": Config.GMAIL_CLIENT_ID,
                "project_id": "gmail-automation",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": Config.GMAIL_CLIENT_SECRET,
                "redirect_uris": ["http://localhost"]
            }
        }
        
        with open('credentials.json', 'w') as f:
            json.dump(credentials_data, f, indent=2)
    
    def get_unread_emails(self, max_results=10):
        """Get unread emails from inbox"""
        try:
            results = self.service.users().messages().list(
                userId='me', 
                labelIds=['INBOX', 'UNREAD'],
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me', 
                    id=message['id']
                ).execute()
                
                email_data = self.parse_email(msg)
                emails.append(email_data)
            
            return emails
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []
    
    def parse_email(self, msg):
        """Parse email message and extract relevant information"""
        headers = msg['payload'].get('headers', [])
        
        email_data = {
            'id': msg['id'],
            'thread_id': msg['threadId'],
            'subject': '',
            'sender': '',
            'date': '',
            'body': '',
            'labels': msg.get('labelIds', [])
        }
        
        # Extract headers
        for header in headers:
            name = header['name'].lower()
            if name == 'subject':
                email_data['subject'] = header['value']
            elif name == 'from':
                email_data['sender'] = header['value']
            elif name == 'date':
                email_data['date'] = header['value']
        
        # Extract body
        email_data['body'] = self.extract_body(msg['payload'])
        
        return email_data
    
    def extract_body(self, payload):
        """Extract email body from payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
                elif part['mimeType'] == 'text/html':
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            if payload['mimeType'] == 'text/plain':
                data = payload['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')
        
        return body
    
    def create_draft_reply(self, original_email, reply_text):
        """Create a draft reply to an email"""
        try:
            # Create reply message
            message = MIMEMultipart()
            message['to'] = original_email['sender']
            message['subject'] = f"Re: {original_email['subject']}"
            message['In-Reply-To'] = original_email['id']
            message['References'] = original_email['id']
            
            # Add reply text
            message.attach(MIMEText(reply_text, 'plain'))
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Create draft - only include threadId if it's valid
            draft_body = {
                'message': {
                    'raw': raw_message
                }
            }
            
            # Only add threadId if it's a real thread ID (not test data)
            if original_email.get('thread_id') and not original_email['thread_id'].startswith('thread'):
                draft_body['message']['threadId'] = original_email['thread_id']
            
            # Create draft
            draft = self.service.users().drafts().create(
                userId='me',
                body=draft_body
            ).execute()
            
            print(f"Draft created successfully. Draft ID: {draft['id']}")
            return True
            
        except HttpError as error:
            print(f'An error occurred while creating draft: {error}')
            return False
    
    def send_reply(self, original_email, reply_text):
        """Send a reply to an email"""
        try:
            # Create reply message
            message = MIMEMultipart()
            message['to'] = original_email['sender']
            message['subject'] = f"Re: {original_email['subject']}"
            message['In-Reply-To'] = original_email['id']
            message['References'] = original_email['id']
            
            # Add reply text
            message.attach(MIMEText(reply_text, 'plain'))
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send message
            send_message = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message, 'threadId': original_email['thread_id']}
            ).execute()
            
            print(f"Reply sent successfully. Message ID: {send_message['id']}")
            return True
            
        except HttpError as error:
            print(f'An error occurred while sending reply: {error}')
            return False
    
    def mark_as_read(self, email_id):
        """Mark an email as read"""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except HttpError as error:
            print(f'An error occurred while marking email as read: {error}')
            return False
