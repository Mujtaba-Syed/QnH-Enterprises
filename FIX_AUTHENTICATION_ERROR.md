# 🔐 Fix Email Authentication Error

**Error**: `(535, b'5.7.8 Error: authentication failed: (reason unavailable)')`

This means the SMTP connection works, but authentication is failing.

## Common Causes & Solutions

### 1. Wrong Password ✅ Most Common

**Check:**
- Make sure `EMAIL_HOST_PASSWORD` in `.env` is correct
- No extra spaces before/after the password
- Password might have special characters that need escaping

**Fix:**
```env
EMAIL_HOST_PASSWORD=your-exact-password-with-no-spaces
```

### 2. Wrong Username Format

**Check:**
- Use full email address: `support@qhenterprises.com`
- NOT just: `support`

**Fix:**
```env
EMAIL_HOST_USER=support@qhenterprises.com
```

### 3. Hostinger Requires App Password

Some email providers require app-specific passwords instead of regular passwords.

**Steps:**
1. Log into Hostinger control panel
2. Go to Email section
3. Look for "App Passwords" or "Application Passwords"
4. Generate a new app password
5. Use that password in `.env` instead of your regular password

### 4. Email Account Not Activated

**Check:**
- Make sure the email account `support@qhenterprises.com` is active
- Verify you can log into webmail with the same credentials
- Check if email account is suspended or locked

### 5. Hostinger SMTP Restrictions

Hostinger might have restrictions on SMTP access.

**Check:**
1. Log into Hostinger
2. Go to Email settings
3. Look for "SMTP Access" or "Email Client Settings"
4. Make sure SMTP is enabled for your account
5. Check if there are IP restrictions

### 6. Try Different Authentication Method

Sometimes the issue is with TLS/SSL settings. Try these combinations:

**Option A: Port 587 with TLS**
```env
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```

**Option B: Port 465 with SSL**
```env
EMAIL_PORT=465
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
```

**Option C: Port 2525 (Alternative)**
```env
EMAIL_PORT=2525
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```

### 7. Verify Credentials Work

Test your credentials manually:

**Using Python (outside Docker):**
```python
import smtplib

try:
    server = smtplib.SMTP('smtp.hostinger.com', 587)
    server.starttls()
    server.login('support@qhenterprises.com', 'your-password')
    print("✅ Authentication successful!")
    server.quit()
except Exception as e:
    print(f"❌ Error: {e}")
```

**Or use an email client:**
- Try setting up the same email in Outlook/Thunderbird
- If it works there, credentials are correct
- If it doesn't, the issue is with the credentials themselves

## Quick Checklist

- [ ] Password is correct (no typos, no extra spaces)
- [ ] Username is full email: `support@qhenterprises.com`
- [ ] Email account is active and not locked
- [ ] SMTP access is enabled in Hostinger
- [ ] Using app password if required
- [ ] Tried both port 587 (TLS) and 465 (SSL)

## Test Your Credentials

Run this inside Docker to test:

```bash
docker-compose exec web python -c "
import smtplib
from decouple import config

host = config('EMAIL_HOST', default='smtp.hostinger.com')
port = config('EMAIL_PORT', default=587, cast=int)
user = config('EMAIL_HOST_USER', default='')
password = config('EMAIL_HOST_PASSWORD', default='')
use_tls = config('EMAIL_USE_TLS', default=True, cast=bool)

try:
    server = smtplib.SMTP(host, port)
    if use_tls:
        server.starttls()
    server.login(user, password)
    print('✅ Authentication successful!')
    server.quit()
except Exception as e:
    print(f'❌ Authentication failed: {e}')
"
```

## Still Not Working?

1. **Contact Hostinger Support**: Ask them for:
   - Correct SMTP settings for your account
   - Whether app passwords are required
   - If there are any restrictions on your account

2. **Check Email Account Status**: 
   - Log into webmail: https://webmail.hostinger.com
   - Verify you can log in with the same credentials
   - Check account status

3. **Try Different Email Account**: 
   - Test with a different Hostinger email account
   - Or temporarily use Gmail SMTP to verify your code works

