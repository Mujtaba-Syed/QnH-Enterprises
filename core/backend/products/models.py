from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
import os
from django.core.files.base import ContentFile

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
    
    def get_image_size(self):
        """Get image file size in MB."""
        if not self.image:
            return 0
            
        try:
            if hasattr(self.image, 'path') and os.path.exists(self.image.path):
                if hasattr(self.image, 'size'):
                    return round(self.image.size / (1024 * 1024), 2)
                else:
                    return 0
            else:
                return 0
        except (OSError, FileNotFoundError, AttributeError, Exception):
            return 0
    
    def get_image_dimensions(self):
        """Get image dimensions as a tuple (width, height)."""
        if not self.image:
            return None
            
        try:
            if hasattr(self.image, 'path') and os.path.exists(self.image.path):
                img = Image.open(self.image.path)
                return img.size
            return None
        except Exception:
            return None
    
    def get_optimization_info(self):
        """Get image optimization information."""
        if not self.image:
            return None
            
        current_size = self.get_image_size()
        
        original_size = getattr(self, '_original_image_size', None)
        
        if original_size and original_size > 0:
            savings = ((original_size - current_size) / original_size) * 100
            return {
                'current_size': current_size,
                'original_size': original_size,
                'savings_mb': round(original_size - current_size, 2),
                'savings_percent': round(savings, 1)
            }
        
        return {
            'current_size': current_size,
            'original_size': 'Unknown',
            'savings_mb': 'Unknown',
            'savings_percent': 'Unknown'
        }
    
    def clean_orphaned_image(self):
        """Clean up orphaned image reference if file doesn't exist."""
        try:
            if self.image and hasattr(self.image, 'path'):
                if not os.path.exists(self.image.path):
                    self.image = None
                    self.save(update_fields=['image'])
                    return True
            return False
        except Exception:
            return False
    
    @classmethod
    def cleanup_all_orphaned_images(cls):
        """Clean up all products with orphaned image references."""
        cleaned_count = 0
        products = cls.objects.filter(image__isnull=False)
        
        for product in products:
            if product.clean_orphaned_image():
                cleaned_count += 1
        
        return cleaned_count
    
    def optimize_image(self):
        """Optimize the product image to reduce file size."""
        if not self.image:
            return False
            
        try:
            original_size = self.get_image_size()
            self._original_image_size = original_size
            
            img = Image.open(self.image)
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            original_width, original_height = img.size
            
            max_width = 1200
            max_height = 1200
            
            if original_width > max_width or original_height > max_height:
                ratio = min(max_width / original_width, max_height / original_height)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            buffer = BytesIO()
            
            quality = 85
            max_size_mb = 1.0 
            
            while quality > 30: 
                buffer.seek(0)
                buffer.truncate(0)
                
                img.save(buffer, format='JPEG', quality=quality, optimize=True)
                
                buffer.seek(0)
                file_size_mb = len(buffer.getvalue()) / (1024 * 1024)
                
                if file_size_mb <= max_size_mb:
                    break
                
                quality -= 10  
            
            buffer.seek(0)
            
            file_name = f'{self.name}_{self.id}_optimized.jpg'
            
            self.image.save(file_name, ContentFile(buffer.read()), save=False)
            buffer.close()
            
            return True
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Image optimization failed for product {self.id}: {str(e)}")
            return False
    
    def save(self, *args, **kwargs):
        # Check if this is a new image being added
        is_new_image = False
        if self.pk:  # Existing product
            try:
                old_product = Product.objects.get(pk=self.pk)
                is_new_image = (old_product.image != self.image)
            except Product.DoesNotExist:
                is_new_image = True
        else:
            is_new_image = bool(self.image)
        
        # Save first to get the ID
        super().save(*args, **kwargs)
        
        # Optimize image if it's new or changed
        if is_new_image and self.image:
            self.optimize_image()
            # Save again with the optimized image
            super().save(update_fields=['image'])

class FeaturedProducts(models.Model):
    """Stores all featured products."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_percentage = models.PositiveIntegerField(null=True, blank=True)
    discount_text = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.discount_percentage}"
