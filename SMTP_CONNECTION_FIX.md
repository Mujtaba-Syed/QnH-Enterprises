# 🔧 Fix SMTP Connection Timeout

You're getting: **"Connection unexpectedly closed: timed out"**

This means SMTP is configured but can't connect to Hostinger's server.

## Quick Fix: Try Port 465 with SSL

Hostinger sometimes works better with port 465 and SSL. Update your `.env` file:

```env
EMAIL_USE_SMTP=True
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=465
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_HOST_USER=support@qhenterprises.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=support@qhenterprises.com
```

**Key changes:**
- `EMAIL_PORT=465` (instead of 587)
- `EMAIL_USE_SSL=True` (instead of False)
- `EMAIL_USE_TLS=False` (instead of True)

## Alternative: Check Hostinger SMTP Settings

Hostinger might use different SMTP settings. Check your Hostinger control panel:

1. Go to **Email** section in Hostinger
2. Look for **SMTP Settings** or **Email Client Configuration**
3. Verify:
   - SMTP Server: `smtp.hostinger.com` or `smtp.titan.email`
   - Port: `587` (TLS) or `465` (SSL)
   - Security: TLS or SSL

## Common Solutions

### Solution 1: Use Port 465 with SSL
```env
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_USE_TLS=False
```

### Solution 2: Try Different SMTP Host
Some Hostinger accounts use:
```env
EMAIL_HOST=smtp.titan.email
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_USE_TLS=False
```

### Solution 3: Check Firewall/Network
- Docker might be blocking outbound SMTP connections
- Check if your network/firewall allows SMTP ports (587, 465)
- Try testing from outside Docker first

### Solution 4: Verify Email Credentials
- Make sure `EMAIL_HOST_USER` is the full email: `support@qhenterprises.com`
- Verify `EMAIL_HOST_PASSWORD` is correct (no extra spaces)
- Some email providers require app-specific passwords

## Test Connection

After updating `.env`, restart Docker:

```bash
docker-compose restart web
```

Then test again. The timeout has been increased to 30 seconds.

## Still Not Working?

1. **Check Hostinger Email Settings**: Log into Hostinger and verify SMTP configuration
2. **Test from Host Machine**: Try sending email from your computer (not Docker) to verify credentials
3. **Check Docker Network**: Make sure Docker can reach external SMTP servers
4. **Try Gmail SMTP** (for testing): Temporarily use Gmail to verify your code works:
   ```env
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-gmail@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

## Current Configuration

Based on your terminal, you have:
- ✅ Email Backend: SMTP (working!)
- ✅ Email Host: smtp.hostinger.com:587
- ✅ Email User: support@qhenterprises.com
- ❌ Connection timeout (can't reach server)

Try port 465 with SSL first - that's the most common fix for Hostinger!

