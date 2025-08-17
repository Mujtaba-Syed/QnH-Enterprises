from django.db import models
from django.core.exceptions import ValidationError

class Product(models.Model):
    """Stores all product details."""
    TYPE_CHOICES = [
        ('perfume', 'Perfume'),
        ('shirt', 'Shirt'),
        ('car', 'Car'),
        ('mobile_accessories', 'Mobile Accessories'),
        ('watches', 'Watches'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    product_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='perfume')
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    attributes = models.JSONField(default=dict, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    newly_added = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)
    rating= models.PositiveIntegerField(default=0, null=True, blank=True)

    def clean(self):
        if self.rating > 5:
            raise ValidationError("Rating must be between 0 and 5")

    def __str__(self):
        return f"{self.name} - {self.product_type}"


class FeaturedProducts(models.Model):
    """Stores all featured products."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_percentage = models.PositiveIntegerField(null=True, blank=True)
    discount_text = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.discount_percentage}"
