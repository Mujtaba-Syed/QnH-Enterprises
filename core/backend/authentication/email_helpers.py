from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .token import account_activation_token
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

def send_email(subject, recipient_email, message):
    """
    Generic email sending function with improved error handling
    """
    try:
        if not all([subject, recipient_email, message]):
            logger.error("Missing required email parameters")
            return False

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
            reply_to=[settings.DEFAULT_FROM_EMAIL],
        )
        email.send()
        logger.info(f"Email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
        return False

def send_verification_email(user, recipient_email):
    """
    Send password reset verification email with token
    """
    if not user or not recipient_email:
        logger.error("User or recipient email is missing")
        return False

    try:
        if not hasattr(settings, 'FRONTEND_URL'):
            logger.error("FRONTEND_URL is not configured in settings")
            return False

        # Generate token with expiration
        expiration_minutes = account_activation_token.expiration_minutes
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        
        # Build reset link
        reset_link = f"{settings.FRONTEND_URL}/accounts/password-reset-confirm/{uid}/{token}/"
        
        # Build email content
        subject = "Password Reset Request"
        message = (
            f"Hello {user.username},\n\n"
            f"You requested a password reset for your account.\n\n"
            f"Please click the following link to reset your password:\n"
            f"{reset_link}\n\n"
            f"This link will expire in {expiration_minutes} minutes.\n\n"
            f"If you didn't request this, please ignore this email.\n\n"
            f"Thanks,\n"
            f"Your Application Team"
        )

        # Send email
        return send_email(subject, recipient_email, message)
    except Exception as e:
        logger.error(f"Error in send_verification_email: {str(e)}")
        return False