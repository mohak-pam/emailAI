# Gmail API Setup Instructions

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Click "Select a project" at the top
3. Click "New Project"
4. Enter a project name (e.g., "gmail-automation")
5. Click "Create"

## Step 2: Enable Gmail API

1. In your project, go to "APIs & Services" > "Library"
2. Search for "Gmail API"
3. Click on "Gmail API"
4. Click "Enable"

## Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type (for personal Gmail accounts)
   - OR Choose "Internal" user type (only if you have Google Workspace)
   - Fill in required fields (App name, User support email, Developer contact)
   - Add your email to test users
   - Save and continue through the steps
4. For Application type, choose "Desktop application"
5. Give it a name (e.g., "Gmail Automation Client")
6. Click "Create"

## Step 4: Download Credentials

1. After creating the OAuth client, click the download button (⬇️)
2. Save the file as `credentials.json` in this directory
3. The file should look like this:

```json
{
  "installed": {
    "client_id": "123456789-abcdefghijklmnop.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "GOCSPX-abcdefghijklmnopqrstuvwxyz",
    "redirect_uris": ["http://localhost"]
  }
}
```

## Step 5: Run Setup

Once you have the correct `credentials.json` file:

```bash
python setup_gmail_api.py
```

This will:
1. Verify your credentials
2. Open a browser for OAuth authentication
3. Create a `token.pickle` file for future use
4. Create a `.env` file with your credentials

## Troubleshooting

### "Access blocked" error
- **For External apps**: Make sure you added your email to test users in OAuth consent screen
- **For Internal apps**: Check that your Google Workspace account has proper permissions
- Wait a few minutes after making changes

### "Invalid client" error
- Check that your `credentials.json` file is properly formatted
- Make sure you downloaded the correct file from Google Cloud Console

### "Redirect URI mismatch" error
- The redirect URI should be `http://localhost` (this is set automatically)

## Next Steps

After successful setup:
1. Test the configuration: `python main.py --config-check`
2. Test email classification: `python test_classification.py`
3. Run automation: `python main.py --mode once`
