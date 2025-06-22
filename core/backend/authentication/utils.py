from django.conf import settings
from datetime import timedelta

def get_jwt_access_token_lifetime():
    """
    Get JWT access token lifetime from settings
    """
    jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
    return jwt_settings.get('ACCESS_TOKEN_LIFETIME', timedelta(minutes=5))

def get_jwt_refresh_token_lifetime():
    """
    Get JWT refresh token lifetime from settings
    """
    jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
    return jwt_settings.get('REFRESH_TOKEN_LIFETIME', timedelta(days=1))

def get_password_reset_token_expiry_minutes():
    """
    Get password reset token expiry time in minutes from settings
    """
    return getattr(settings, 'PASSWORD_RESET_TOKEN_EXPIRY_MINUTES', 120)

def format_token_lifetime(timedelta_obj):
    """
    Format timedelta object into human readable string
    """
    total_seconds = int(timedelta_obj.total_seconds())
    
    if total_seconds < 60:
        return f"{total_seconds} seconds"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        return f"{minutes} minutes"
    elif total_seconds < 86400:
        hours = total_seconds // 3600
        return f"{hours} hours"
    else:
        days = total_seconds // 86400
        return f"{days} days" 