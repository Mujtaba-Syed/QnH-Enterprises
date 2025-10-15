from django.db import models
from django.contrib.auth.models import User
from backend.products.models import Product
from django.conf import settings
import uuid
from django.utils import timezone
from datetime import timedelta

class GuestUser(models.Model):
    """Model to track guest users for cart persistence"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest_token = models.CharField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.guest_token:
            self.guest_token = str(uuid.uuid4())
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=7)  # 7 days TTL
        super().save(*args, **kwargs)
    
    def is_expired(self):
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"Guest - {self.guest_token[:8]}..."

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    guest_user = models.OneToOneField(GuestUser, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(user__isnull=False) | models.Q(guest_user__isnull=False),
                name='cart_must_have_user_or_guest'
            )
        ]
    
    def __str__(self):
        if self.user:
            return f"Cart - {self.user.username}"
        else:
            return f"Guest Cart - {self.guest_user.guest_token[:8]}..."


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')  
