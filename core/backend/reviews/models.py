from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from backend.products.models import Product

User = get_user_model()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)  # Optional, can be auto-populated from user
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True, related_name='reviews')
    image = models.ImageField(upload_to='review_images/', blank=True, null=True)
    whtsapp_image = models.ImageField(upload_to='whtsapp_images/', blank=True, null=True)
    description = models.TextField()
    rating = models.PositiveSmallIntegerField() 
    is_active = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'product']  # Prevent duplicate reviews from same user for same product


    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({'rating': 'Rating must be between 1 and 5.'})

    def __str__(self):
        display_name = self.name or (self.user.username if self.user else 'Anonymous')
        return f"{display_name} - {self.rating}/5"
