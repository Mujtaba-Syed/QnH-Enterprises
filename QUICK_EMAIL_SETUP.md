# Quick Email Setup for Development

## Step 1: Add to your `.env` file

Add these lines to your `.env` file:

```env
# Enable SMTP email in development (set to True)
EMAIL_USE_SMTP=True

# Hostinger SMTP Configuration
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

# Your Hostinger email credentials
EMAIL_HOST_USER=your-email@qhenterprises.com
EMAIL_HOST_PASSWORD=your-actual-password

# Sender email
DEFAULT_FROM_EMAIL=your-email@qhenterprises.com

# Admin settings (optional)
ADMIN_EMAIL=admin@qhenterprises.com
ADMIN_NAME=Admin
```

## Step 2: Restart Docker

After adding the settings, restart your containers:

```bash
docker-compose restart web
```

Or if that doesn't work:

```bash
docker-compose down
docker-compose up --build
```

## Step 3: Check Terminal Output

After restart, you should see:

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

## Step 4: Test Email

### Option A: Using Swagger UI
1. Go to: `http://localhost:8000/api/docs/`
2. Find `POST /api/orders/test-email/`
3. Click "Try it out"
4. Enter your email: `{"email": "your-email@gmail.com"}`
5. Click "Execute"
6. Check your inbox!

### Option B: Using curl
```bash
curl -X POST http://localhost:8000/api/orders/test-email/ \
  -H "Content-Type: application/json" \
  -d '{"email": "your-email@gmail.com"}'
```

### Option C: Using Python
```python
import requests

response = requests.post(
    'http://localhost:8000/api/orders/test-email/',
    json={'email': 'your-email@gmail.com'}
)
print(response.json())
```

## Troubleshooting

### Still seeing "Console" backend?
- ✅ Make sure `EMAIL_USE_SMTP=True` (not `False` or commented out)
- ✅ Restart Docker containers completely
- ✅ Check for typos in `.env` file

### "Failed to send email" error?
- ✅ Double-check `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`
- ✅ Make sure password doesn't have extra spaces
- ✅ Try port 465 with SSL:
  ```env
  EMAIL_PORT=465
  EMAIL_USE_SSL=True
  EMAIL_USE_TLS=False
  ```

### Email not received?
- ✅ Check spam folder
- ✅ Wait a few minutes (sometimes delayed)
- ✅ Verify recipient email is correct

## Example .env Section

Here's what your `.env` should look like (around lines 59-71):

```env
# ... other settings ...

# Email Configuration for Development
EMAIL_USE_SMTP=True
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=info@qhenterprises.com
EMAIL_HOST_PASSWORD=YourActualPassword123
DEFAULT_FROM_EMAIL=info@qhenterprises.com
ADMIN_EMAIL=admin@qhenterprises.com
ADMIN_NAME=Admin
```

**Important**: Replace `info@qhenterprises.com` and `YourActualPassword123` with your real Hostinger email credentials!

