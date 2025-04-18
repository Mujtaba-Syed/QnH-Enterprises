from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
#make a review model with the following fields
#name, image description, rating, created_at, updated_at

class Review(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    description = models.TextField()
    rating = models.PositiveSmallIntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({'rating': 'Rating must be between 1 and 5.'})

    def __str__(self):
        return f"{self.name} - {self.rating}/5"
