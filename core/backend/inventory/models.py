from django.db import models
from backend.products.models import Product
class Inventory(models.Model):
    """Manages stock levels for each product."""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="inventory")
    stock_quantity = models.PositiveIntegerField(default=0)
    restock_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.stock_quantity} in stock"
