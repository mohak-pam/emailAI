#!/usr/bin/env python3
"""
Gmail Email Automation System
Automatically responds to common email queries with appropriate templates.
"""

import argparse
import sys
import os
from email_automation import EmailAutomation
from config import Config

def main():
    parser = argparse.ArgumentParser(description='Gmail Email Automation System')
    parser.add_argument('--mode', choices=['once', 'continuous'], default='once',
                       help='Run mode: once (single check) or continuous (keep running)')
    parser.add_argument('--config-check', action='store_true',
                       help='Check configuration and exit')
    
    args = parser.parse_args()
    
    # Check configuration
    if args.config_check:
        check_configuration()
        return
    
    # Validate configuration before running
    if not validate_configuration():
        print("Configuration validation failed. Please check your .env file.")
        sys.exit(1)
    
    # Initialize and run automation
    try:
        automation = EmailAutomation()
        
        if args.mode == 'continuous':
            automation.run_continuous()
        else:
            automation.run_once()
            
    except KeyboardInterrupt:
        print("\nEmail automation stopped by user.")
    except Exception as e:
        print(f"Error running email automation: {str(e)}")
        sys.exit(1)

def check_configuration():
    """Check and display current configuration"""
    print("=== Gmail Email Automation Configuration ===")
    print(f"Gmail Client ID: {'✓ Set' if Config.GMAIL_CLIENT_ID else '✗ Missing'}")
    print(f"Gmail Client Secret: {'✓ Set' if Config.GMAIL_CLIENT_SECRET else '✗ Missing'}")
    print(f"Gmail Refresh Token: {'✓ Set' if Config.GMAIL_REFRESH_TOKEN else '✗ Missing'}")
    print(f"Auto-reply Enabled: {Config.AUTO_REPLY_ENABLED}")
    print(f"Check Interval: {Config.CHECK_INTERVAL_MINUTES} minutes")
    print(f"Max Emails Per Check: {Config.MAX_EMAILS_PER_CHECK}")
    print(f"Default Response Template: {Config.DEFAULT_RESPONSE_TEMPLATE[:50]}...")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✓ .env file found")
    else:
        print("✗ .env file not found - please create one from .env.example")

def validate_configuration():
    """Validate that required configuration is present"""
    required_fields = [
        ('GMAIL_CLIENT_ID', Config.GMAIL_CLIENT_ID),
        ('GMAIL_CLIENT_SECRET', Config.GMAIL_CLIENT_SECRET),
        ('GMAIL_REFRESH_TOKEN', Config.GMAIL_REFRESH_TOKEN)
    ]
    
    missing_fields = []
    for field_name, field_value in required_fields:
        if not field_value:
            missing_fields.append(field_name)
    
    if missing_fields:
        print(f"Missing required configuration fields: {', '.join(missing_fields)}")
        return False
    
    return True

if __name__ == "__main__":
    main()
