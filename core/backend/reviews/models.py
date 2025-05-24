from django.db import models
from django.core.exceptions import ValidationError
from backend.products.models import Product

class Review(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True, related_name='reviews')
    image = models.ImageField(upload_to='review_images/', blank=True, null=True)
    description = models.TextField()
    rating = models.PositiveSmallIntegerField() 
    is_active = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({'rating': 'Rating must be between 1 and 5.'})

    def __str__(self):
        return f"{self.name} - {self.rating}/5"
