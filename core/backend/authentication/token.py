from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.utils import timezone
import datetime
from django.conf import settings

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator with expiration time
    """
    def __init__(self, expiration_minutes=None):
        self.expiration_minutes = expiration_minutes or getattr(
            settings, 'PASSWORD_RESET_TOKEN_EXPIRY_MINUTES', 120
        )
        super().__init__()

    def _make_hash_value(self, user, timestamp):
        """
        Create a hash value that will be used to generate the token
        """
        return (
            six.text_type(user.pk) + 
            six.text_type(timestamp) + 
            six.text_type(user.is_active) +
            six.text_type(user.password)  
        )

    def make_token(self, user):
        """
        Generate a token with expiration timestamp appended
        Format: token:expiration_timestamp
        """
        token_value = super().make_token(user)
        
        expiration_time = int((timezone.now() + datetime.timedelta(minutes=self.expiration_minutes)).timestamp())
        
        return f"{token_value}:{expiration_time}"

    def check_token(self, user, token):
        """
        Validate token by checking:
        1. Token structure
        2. Expiration time
        3. Base token validity
        """
        try:
            token_value, expiration_time = token.rsplit(":", 1)
            expiration_time = int(expiration_time)

            if timezone.now().timestamp() > expiration_time:
                return False

            return super().check_token(user, token_value)
        except (ValueError, IndexError):
            return False

account_activation_token = AccountActivationTokenGenerator()