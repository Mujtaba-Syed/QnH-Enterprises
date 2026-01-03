# Email Setup Instructions - Send Real Emails

To send **actual emails** instead of console output, add these settings to your `.env` file:

## Quick Setup

Add these lines to your `.env` file (around lines 59-71 as you mentioned):

```env
# Enable SMTP email (set to True to send real emails)
EMAIL_USE_SMTP=True

# Hostinger SMTP Configuration
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

# Your Hostinger email credentials
EMAIL_HOST_USER=your-email@qhenterprises.com
EMAIL_HOST_PASSWORD=your-email-password

# Email address that will appear as sender
DEFAULT_FROM_EMAIL=your-email@qhenterprises.com

# Admin email for notifications
ADMIN_EMAIL=admin@qhenterprises.com
ADMIN_NAME=Admin
```

## Important Notes

1. **`EMAIL_USE_SMTP=True`** - This is the key setting! Set this to `True` to enable real email sending even in development mode.

2. **Keep `PRODUCTION=False`** - You can keep `PRODUCTION=False` for development, but set `EMAIL_USE_SMTP=True` to send real emails.

3. **Hostinger Email Credentials**:
   - `EMAIL_HOST_USER`: Your full Hostinger email address (e.g., `info@qhenterprises.com`)
   - `EMAIL_HOST_PASSWORD`: Your email account password
   - Make sure you're using the correct password for the email account

4. **Port Configuration**:
   - Port `587` with TLS (recommended) - Set `EMAIL_USE_TLS=True` and `EMAIL_USE_SSL=False`
   - Port `465` with SSL (alternative) - Set `EMAIL_USE_SSL=True` and `EMAIL_USE_TLS=False`

## Example .env Configuration

```env
# Environment
DEBUG=True
PRODUCTION=False

# Enable SMTP for real emails
EMAIL_USE_SMTP=True

# Email Settings
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=info@qhenterprises.com
EMAIL_HOST_PASSWORD=your-actual-password-here
DEFAULT_FROM_EMAIL=info@qhenterprises.com
ADMIN_EMAIL=admin@qhenterprises.com
ADMIN_NAME=Admin
```

## After Updating .env

1. **Restart your Docker containers**:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

2. **Or if running locally**, restart your Django server:
   ```bash
   # Stop the server (Ctrl+C) and restart
   python manage.py runserver
   ```

3. **Test the email**:
   ```bash
   # Using the API endpoint
   curl -X POST http://localhost:8000/api/orders/test-email/ \
     -H "Content-Type: application/json" \
     -d '{"email": "your-email@gmail.com"}'
   ```

4. **Check your email inbox** (and spam folder) for the test email!

## Troubleshooting

### Emails still going to console?

- ✅ Make sure `EMAIL_USE_SMTP=True` in your `.env` file
- ✅ Restart your Docker containers or Django server
- ✅ Check the terminal output - it should say "Email Backend: SMTP" instead of "Console"

### "Failed to send email" error?

- ✅ Verify `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are correct
- ✅ Check that your Hostinger email account is active
- ✅ Try port 465 with SSL instead:
  ```env
  EMAIL_PORT=465
  EMAIL_USE_SSL=True
  EMAIL_USE_TLS=False
  ```
- ✅ Check Django logs for detailed error messages

### Emails not received?

- ✅ Check spam/junk folder
- ✅ Verify the recipient email address is correct
- ✅ Make sure your Hostinger email account allows SMTP access
- ✅ Test with a different email provider (Gmail, etc.) to isolate the issue

### Connection timeout?

- ✅ Check if your network/firewall allows SMTP connections
- ✅ Verify Hostinger SMTP server is accessible
- ✅ Try using port 465 with SSL

## Testing

After setting up, you should see in your terminal:
```
Email Backend: SMTP
Email Host: smtp.hostinger.com:587
Email User: your-email@qhenterprises.com
From Email: your-email@qhenterprises.com
```

Instead of:
```
Email Backend: Console (emails will be printed to terminal)
```

## Security Note

⚠️ **Never commit your `.env` file to version control!** It contains sensitive credentials.

Make sure `.env` is in your `.gitignore` file.

