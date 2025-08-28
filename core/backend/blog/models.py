from django.db import models
from django.utils.text import slugify
import os
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    meta_description = models.TextField(blank=True, null=True, help_text="Meta description for the blog post")
    keywords = models.TextField(blank=True, null=True, help_text="Comma separated keywords for the SEO post")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def get_image_size(self):
        """Get the size of the image in MB."""
        if not self.image:
            return 0
        try:
            if hasattr(self.image, 'path') and os.path.exists(self.image.path):
                if hasattr(self.image, 'size'):
                    return round(self.image.size / (1024 * 1024), 2)
                else:
                    return 0
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
        """Clean up all blog posts with orphaned image references."""
        cleaned_count = 0
        blogs = cls.objects.filter(image__isnull=False)
        
        for blog in blogs:
            if blog.clean_orphaned_image():
                cleaned_count += 1
        
        return cleaned_count
    
    def optimize_image(self):
        """Optimize the blog image to reduce file size."""
        if not self.image:
            return False
            
        try:
            original_size = self.get_image_size()
            self._original_image_size = original_size
            
            img = Image.open(self.image)
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            original_width, original_height = img.size
            
            # Blog images can be larger than product images
            max_width = 1600
            max_height = 1200
            
            if original_width > max_width or original_height > max_height:
                ratio = min(max_width / original_width, max_height / original_height)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            buffer = BytesIO()
            
            quality = 85
            max_size_mb = 1.5  # Blog images can be slightly larger
            
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
            
            file_name = f'{self.slug}_{self.id}_optimized.jpg'
            
            self.image.save(file_name, ContentFile(buffer.read()), save=False)
            buffer.close()
            
            return True
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Image optimization failed for blog {self.id}: {str(e)}")
            return False
    
    def save(self, *args, **kwargs):
        is_new_image = False
        if self.pk:  
            try:
                old_blog = Blog.objects.get(pk=self.pk)
                is_new_image = (old_blog.image != self.image)
            except Blog.DoesNotExist:
                is_new_image = True
        else:
            is_new_image = bool(self.image)
        
        super().save(*args, **kwargs)
        
        if is_new_image and self.image:
            self.optimize_image()
            super().save(update_fields=['image'])