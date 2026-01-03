# Email Testing Guide

This guide explains how to test the email configuration for QnH Enterprises.

## Prerequisites

1. **Development Mode**: Set `DEBUG=True` in your `.env` file to enable test endpoints
2. **Environment Variables**: Make sure your `.env` file has the email configuration:

```env
# For Development (uses console backend)
DEBUG=True
PRODUCTION=False

# For Production (uses Hostinger SMTP)
DEBUG=False
PRODUCTION=True
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your-email@qhenterprises.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@qhenterprises.com
ADMIN_EMAIL=admin@qhenterprises.com
ADMIN_NAME=Admin
```

## Testing Methods

### Method 1: Using Management Command (Recommended)

The easiest way to test emails is using the Django management command:

```bash
# Test basic email
python manage.py test_email --email your-email@example.com

# Test order confirmation email
python manage.py test_email --email your-email@example.com --type confirmation

# Test order status update email
python manage.py test_email --email your-email@example.com --type status

# Test admin notification email
python manage.py test_email --email your-email@example.com --type admin

# Test order shipped email
python manage.py test_email --email your-email@example.com --type shipped

# Test all email types
python manage.py test_email --email your-email@example.com --type all --name "John Doe"
```

**Note**: In development mode (console backend), emails will be printed to the terminal instead of being sent.

### Method 2: Using API Endpoints (Development Only)

These endpoints are only available when `DEBUG=True` for security.

#### Test Basic Email

```bash
curl -X POST http://localhost:8000/api/orders/test-email/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

Or using Python requests:

```python
import requests

response = requests.post(
    'http://localhost:8000/api/orders/test-email/',
    json={'email': 'test@example.com'}
)
print(response.json())
```

#### Test Order Emails

```bash
# Test order confirmation
curl -X POST http://localhost:8000/api/orders/test-order-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "John Doe",
    "type": "confirmation"
  }'

# Test all order email types
curl -X POST http://localhost:8000/api/orders/test-order-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "John Doe",
    "type": "all",
    "admin_email": "admin@example.com"
  }'
```

### Method 3: Using Django Shell

You can also test emails directly in Django shell:

```bash
python manage.py shell
```

```python
from django.core.mail import EmailMessage
from django.conf import settings
from backend.orders.email_helpers import send_order_confirmation_email

# Test basic email
email = EmailMessage(
    subject='Test Email',
    body='This is a test email.',
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=['your-email@example.com'],
)
email.send()

# Test order confirmation (with mock order)
class MockOrder:
    def __init__(self):
        self.id = 12345
        self.created_at = '2024-01-01 12:00:00'
        self.total = 999.99

order = MockOrder()
send_order_confirmation_email(order, 'your-email@example.com', 'John Doe')
```

## Testing in Development vs Production

### Development Mode (`DEBUG=True`, `PRODUCTION=False`)

- Uses **console email backend**
- Emails are printed to the terminal/console
- No actual emails are sent
- Perfect for testing email content and formatting

**Example output:**
```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Order Confirmation - Order #12345
From: noreply@qhenterprises.com
To: test@example.com
Date: ...

Hello John Doe,

Thank you for your order!
...
```

### Production Mode (`DEBUG=False`, `PRODUCTION=True`)

- Uses **SMTP email backend** (Hostinger)
- Emails are actually sent via SMTP
- Requires valid Hostinger email credentials
- Check your email inbox for received emails

## Troubleshooting

### Issue: "Email testing is only available in DEBUG mode"

**Solution**: Set `DEBUG=True` in your `.env` file, or use the management command which works in both modes.

### Issue: "Failed to send email" in production

**Check:**
1. Verify your Hostinger email credentials in `.env`
2. Ensure `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are correct
3. Check if Hostinger requires app-specific passwords
4. Verify firewall/network allows SMTP connections (port 587)
5. Check Django logs for detailed error messages

### Issue: Emails not received in production

**Check:**
1. Check spam/junk folder
2. Verify the recipient email address is correct
3. Check Hostinger email account for any restrictions
4. Review SMTP logs in Django logs
5. Test with a different email provider to isolate the issue

### Issue: Connection timeout

**Solution**: 
- Try using port 465 with SSL instead of 587 with TLS
- Set `EMAIL_USE_SSL=True` and `EMAIL_USE_TLS=False`
- Check if your hosting provider blocks SMTP ports

## Email Types Available

1. **Order Confirmation** - Sent when order is created
2. **Order Status Update** - Sent when order status changes
3. **Admin Notification** - Sent to admin when new order is received
4. **Order Shipped** - Sent when order is shipped (with tracking number)

## Next Steps

After testing, integrate these email functions into your order processing logic:

```python
from backend.orders.email_helpers import (
    send_order_confirmation_email,
    send_order_notification_to_admin,
    send_order_status_update_email,
    send_order_shipped_email
)

# When order is created
def create_order(order_data):
    order = Order.objects.create(**order_data)
    send_order_confirmation_email(order, order.customer_email, order.customer_name)
    send_order_notification_to_admin(order)
    return order

# When order status changes
def update_order_status(order, new_status):
    order.status = new_status
    order.save()
    send_order_status_update_email(order, order.customer_email, order.customer_name, new_status)

# When order is shipped
def ship_order(order, tracking_number):
    order.status = 'Shipped'
    order.tracking_number = tracking_number
    order.save()
    send_order_shipped_email(order, order.customer_email, order.customer_name, tracking_number)
```

## Security Notes

- Test endpoints are **only available when `DEBUG=True`**
- Never commit email credentials to version control
- Use environment variables for all sensitive data
- In production, disable DEBUG mode and use proper SMTP authentication

