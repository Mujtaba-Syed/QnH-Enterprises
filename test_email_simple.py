#!/usr/bin/env python
"""
Simple script to test email configuration
Run this from the project root: python test_email_simple.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.mail import EmailMessage
from django.conf import settings

def test_email():
    """Test sending an email"""
    print("\n" + "="*60)
    print("EMAIL CONFIGURATION TEST")
    print("="*60)
    
    # Show current configuration
    print(f"\n📧 Email Backend: {settings.EMAIL_BACKEND}")
    print(f"📧 Email Host: {getattr(settings, 'EMAIL_HOST', 'N/A')}")
    print(f"📧 Email Port: {getattr(settings, 'EMAIL_PORT', 'N/A')}")
    print(f"📧 From Email: {settings.DEFAULT_FROM_EMAIL}")
    print(f"📧 Use TLS: {getattr(settings, 'EMAIL_USE_TLS', False)}")
    print(f"📧 Use SSL: {getattr(settings, 'EMAIL_USE_SSL', False)}")
    
    # Get recipient email
    recipient = input("\n📬 Enter recipient email address: ").strip()
    
    if not recipient:
        print("❌ No email address provided. Exiting.")
        return
    
    # Send test email
    print(f"\n📤 Sending test email to {recipient}...")
    
    try:
        email = EmailMessage(
            subject='Test Email from QnH Enterprises',
            body=f"""
Hello!

This is a test email from your QnH Enterprises application.

If you received this email, your SMTP configuration is working correctly!

Email Settings:
- Backend: {settings.EMAIL_BACKEND}
- Host: {getattr(settings, 'EMAIL_HOST', 'N/A')}
- Port: {getattr(settings, 'EMAIL_PORT', 'N/A')}
- From: {settings.DEFAULT_FROM_EMAIL}

Best regards,
QnH Enterprises Team
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
        )
        email.send()
        
        print("✅ Email sent successfully!")
        print(f"📬 Check your inbox at: {recipient}")
        print("📬 Don't forget to check spam folder if you don't see it!")
        
    except Exception as e:
        print(f"\n❌ Error sending email: {str(e)}")
        print("\n🔍 Troubleshooting:")
        print("1. Check your .env file has EMAIL_USE_SMTP=True")
        print("2. Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are correct")
        print("3. Make sure your Hostinger email account is active")
        print("4. Check if firewall/network allows SMTP connections")
        print(f"\n📋 Full error: {type(e).__name__}: {str(e)}")

if __name__ == '__main__':
    test_email()

