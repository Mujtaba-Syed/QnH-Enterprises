from django.db import models


class Product(models.Model):
    """Stores all product details."""
    TYPE_CHOICES = [
        ('perfume', 'Perfume'),
        ('shirt', 'Shirt'),
        ('car', 'Car'),
        ('mobile_accessories', 'Mobile Accessories'),
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

    def __str__(self):
        return f"{self.name} - {self.product_type}"
