#!/usr/bin/env python
"""
Script to check email configuration from environment
Run this inside Docker: docker-compose exec web python check_email_config.py
"""
import os
from decouple import config

print("\n" + "="*60)
print("EMAIL CONFIGURATION DIAGNOSTIC")
print("="*60)

# Check environment variables
print("\n📋 Environment Variables Check:")
print(f"  EMAIL_USE_SMTP (raw env): {os.getenv('EMAIL_USE_SMTP', 'NOT SET')}")
print(f"  EMAIL_USE_SMTP (config): {config('EMAIL_USE_SMTP', default='NOT SET')}")
print(f"  EMAIL_USE_SMTP (bool): {config('EMAIL_USE_SMTP', default=False, cast=bool)}")
print(f"  EMAIL_HOST: {config('EMAIL_HOST', default='NOT SET')}")
print(f"  EMAIL_PORT: {config('EMAIL_PORT', default='NOT SET')}")
print(f"  EMAIL_HOST_USER: {config('EMAIL_HOST_USER', default='NOT SET')}")
print(f"  EMAIL_HOST_PASSWORD: {'***SET***' if config('EMAIL_HOST_PASSWORD', default='') else 'NOT SET'}")

# Check .env file location
print("\n📁 File Check:")
env_path = '/app/.env'
if os.path.exists(env_path):
    print(f"  ✓ .env file exists at: {env_path}")
    # Read first few lines to check format
    try:
        with open(env_path, 'r') as f:
            lines = f.readlines()[:20]
            print(f"  ✓ File readable, first 20 lines:")
            for i, line in enumerate(lines, 1):
                if 'EMAIL' in line.upper():
                    print(f"    Line {i}: {line.strip()}")
    except Exception as e:
        print(f"  ✗ Error reading file: {e}")
else:
    print(f"  ✗ .env file NOT found at: {env_path}")

# Simulate settings logic
print("\n🔧 Settings Logic Simulation:")
production = config('PRODUCTION', default=False, cast=bool)
email_use_smtp = config('EMAIL_USE_SMTP', default=False, cast=bool)

print(f"  PRODUCTION: {production}")
print(f"  EMAIL_USE_SMTP: {email_use_smtp}")
print(f"  Will use SMTP: {production or email_use_smtp}")

if production or email_use_smtp:
    print("\n  ✅ Should use SMTP backend")
    print(f"  EMAIL_HOST: {config('EMAIL_HOST', default='smtp.hostinger.com')}")
    print(f"  EMAIL_PORT: {config('EMAIL_PORT', default=587, cast=int)}")
else:
    print("\n  ❌ Will use Console backend")
    print("  → Add EMAIL_USE_SMTP=True to your .env file")

print("\n" + "="*60)

