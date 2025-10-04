# Gmail Email Automation System

A Python-based system that automatically responds to common email queries in your Gmail inbox with appropriate pre-written templates. This system uses Gmail API to read emails, classify them based on content, and send automated responses.

## Features

- **Automatic Email Classification**: Intelligently categorizes emails into different types (pricing, support, product info, meeting requests, etc.)
- **Template-based Responses**: Pre-written response templates for different query types
- **Gmail API Integration**: Secure integration with Gmail using OAuth 2.0
- **Configurable Settings**: Customizable check intervals, response templates, and automation rules
- **Smart Filtering**: Automatically skips auto-replies and no-reply emails
- **Logging**: Comprehensive logging for monitoring and debugging
- **Flexible Modes**: Run once or continuously

## Email Categories Supported

1. **Pricing Inquiries**: Questions about costs, quotes, budgets
2. **Support Requests**: Help requests, bug reports, technical issues
3. **Product Information**: Feature inquiries, specifications, capabilities
4. **Meeting Requests**: Scheduling requests, demo appointments
5. **General Inquiries**: General questions and greetings
6. **Default**: Fallback for unrecognized email types

## Installation

### Prerequisites

- Python 3.7 or higher
- Gmail account with API access
- Google Cloud Console project with Gmail API enabled

### Setup Steps

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gmail API credentials**:
   ```bash
   python setup_gmail_api.py
   ```
   This will guide you through the Gmail API setup process.

4. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your Gmail API credentials

5. **Set target email and Gemini API (enables AI summaries)**:
   - Add to your `.env` file:
     ```
     TARGET_EMAIL=your.address@yourdomain.com
     GEMINI_API_KEY=your_api_key_here
     GEMINI_MODEL=gemini-2.0-flash
     SIGNATURE_NAME=Mohak Bansal
     SIGNATURE_TITLE=Software Engineer
     SIGNATURE_COMPANY=miniOrange
     ```

6. **Test the configuration**:
   ```bash
   python main.py --config-check
   ```

## Usage

### Running the Automation

**Run once (single check)**:
```bash
python main.py --mode once
```

**Run continuously**:
```bash
python main.py --mode continuous
```

**Check configuration**:
```bash
python main.py --config-check
```

### Configuration Options

Edit the `.env` file to customize:

- `AUTO_REPLY_ENABLED`: Enable/disable automatic replies (true/false)
- `CHECK_INTERVAL_MINUTES`: How often to check for new emails (default: 5 minutes)
- `MAX_EMAILS_PER_CHECK`: Maximum emails to process per check (default: 10)
- `DEFAULT_RESPONSE_TEMPLATE`: Default response for unrecognized emails

### Customizing Response Templates

Edit `email_classifier.py` to modify response templates:

```python
def initialize_response_templates(self):
    return {
        'pricing': """Your custom pricing response template...""",
        'support': """Your custom support response template...""",
        # ... other templates
    }
```

### Adding New Email Categories

To add new email categories:

1. Add patterns to `query_patterns` in `email_classifier.py`
2. Add corresponding response template
3. Update the classification logic if needed

## File Structure

```
AImail/
├── main.py                 # Main application entry point
├── gmail_client.py         # Gmail API integration
├── email_classifier.py     # Email classification and templates
├── email_automation.py     # Core automation logic
├── config.py              # Configuration management
├── setup_gmail_api.py     # Gmail API setup script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
└── email_automation.log  # Log file (created when running)
```

## Gmail API Setup

### Step-by-Step Gmail API Setup

1. **Go to Google Cloud Console**:
   - Visit [Google Cloud Console](https://console.developers.google.com/)

2. **Create or select a project**:
   - Create a new project or select an existing one

3. **Enable Gmail API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API" and enable it

4. **Create credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client ID"
   - Choose "Desktop application"
   - Download the credentials.json file

5. **Place credentials.json in the project directory**

6. **Run the setup script**:
   ```bash
   python setup_gmail_api.py
   ```

## Security Considerations

- **Credentials**: Never commit `credentials.json`, `token.pickle`, or `.env` files to version control
- **Permissions**: The system only requests read and send permissions for Gmail
- **Rate Limiting**: Built-in delays prevent API rate limit issues
- **Logging**: Sensitive information is not logged

## Troubleshooting

### Common Issues

1. **"Credentials not found"**:
   - Ensure `credentials.json` is in the project directory
   - Run `python setup_gmail_api.py` to set up credentials

2. **"Permission denied"**:
   - Check that Gmail API is enabled in Google Cloud Console
   - Verify OAuth consent screen is configured

3. **"No emails found"**:
   - Check if there are unread emails in your inbox
   - Verify the Gmail account has the correct permissions

4. **"Failed to send reply"**:
   - Check Gmail API quotas and limits
   - Verify the email address is valid

### Logs

Check `email_automation.log` for detailed information about:
- Email processing status
- Classification results
- Reply sending status
- Error messages

## Customization

### Adding Custom Email Patterns

To add custom email patterns for classification:

```python
def initialize_query_patterns(self):
    return {
        'your_category': [
            r'\b(your|custom|patterns)\b',
            r'\b(more|regex|patterns)\b'
        ],
        # ... existing patterns
    }
```

### Modifying Response Templates

Templates support basic customization:
- `[Your Name]`: Replaced with your name
- Dynamic content based on email content
- Category-specific information

## Contributing

Feel free to contribute by:
- Adding new email categories
- Improving classification accuracy
- Adding new features
- Fixing bugs

## License

This project is open source. Feel free to use and modify as needed.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs
3. Verify Gmail API setup
4. Check configuration settings
