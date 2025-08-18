from django.contrib import admin
import os
from .models import Product, FeaturedProducts


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'product_type', 'newly_added', 'best_seller', 'is_active', 'image_size')
    list_filter = ('product_type', 'is_active')
    search_fields = ('name', 'description')
    actions = ['optimize_images', 'cleanup_orphaned_images', 'force_reoptimize_images']
    readonly_fields = ('image_size', 'original_image_size', 'optimization_savings', 'image_dimensions')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'product_type', 'sku', 'price', 'brand')
        }),
        ('Image', {
            'fields': ('image', 'image_dimensions', 'image_size', 'original_image_size', 'optimization_savings'),
            'classes': ('collapse',)
        }),
        ('Status & Features', {
            'fields': ('is_active', 'newly_added', 'best_seller', 'rating')
        }),
        ('Additional Data', {
            'fields': ('attributes',),
            'classes': ('collapse',)
        })
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Make image optimization fields read-only."""
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj and obj.image:  
            readonly_fields.extend(['image_size', 'original_image_size', 'optimization_savings', 'image_dimensions'])
        return readonly_fields
    
    def image_size(self, obj):
        """Display current image file size."""
        try:
            size = obj.get_image_size()
            return f"{size}MB" if size > 0 else "No image"
        except Exception:
            return "Error"
    image_size.short_description = 'Current Size'
    
    def original_image_size(self, obj):
        """Display original image size if available."""
        try:
            if hasattr(obj, '_original_image_size'):
                return f"{obj._original_image_size:.2f}MB"
            return "Unknown"
        except Exception:
            return "Error"
    original_image_size.short_description = 'Original Size'
    
    def optimization_savings(self, obj):
        """Display optimization savings."""
        try:
            if hasattr(obj, '_original_image_size') and obj.image:
                current_size = obj.get_image_size()
                original_size = obj._original_image_size
                if original_size > 0:
                    savings = ((original_size - current_size) / original_size) * 100
                    return f"{savings:.1f}% smaller"
            return "N/A"
        except Exception:
            return "Error"
    optimization_savings.short_description = 'Optimization Savings'
    
    def image_dimensions(self, obj):
        """Display image dimensions."""
        try:
            dimensions = obj.get_image_dimensions()
            if dimensions:
                return f"{dimensions[0]} × {dimensions[1]} px"
            return "Unknown"
        except Exception:
            return "Error"
    image_dimensions.short_description = 'Dimensions'
    
    def optimize_images(self, request, queryset):
        """Admin action to optimize selected product images."""
        optimized_count = 0
        failed_count = 0
        
        for product in queryset:
            if product.image:
                try:
                    original_size = product.get_image_size()
                    product._original_image_size = original_size
                    
                    if product.optimize_image():
                        optimized_count += 1
                        product.save(update_fields=['image'])
                    else:
                        failed_count += 1
                except Exception as e:
                    failed_count += 1
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to optimize product {product.id}: {str(e)}")
        
        message = f'Successfully optimized {optimized_count} product images.'
        if failed_count > 0:
            message += f' Failed to optimize {failed_count} images.'
        
        self.message_user(request, message)
    optimize_images.short_description = "Optimize selected product images"
    
    def cleanup_orphaned_images(self, request, queryset):
        """Admin action to clean up orphaned image references."""
        cleaned_count = 0
        
        for product in queryset:
            if product.clean_orphaned_image():
                cleaned_count += 1
        
        self.message_user(
            request,
            f'Cleaned up {cleaned_count} orphaned image references.'
        )
    cleanup_orphaned_images.short_description = "Clean up orphaned images"
    
    def force_reoptimize_images(self, request, queryset):
        """Admin action to force re-optimization of all selected product images."""
        optimized_count = 0
        failed_count = 0
        
        for product in queryset:
            if product.image:
                try:
                    original_size = product.get_image_size()
                    product._original_image_size = original_size
                    
                    if product.optimize_image():
                        optimized_count += 1
                        product.save(update_fields=['image'])
                    else:
                        failed_count += 1
                except Exception as e:
                    failed_count += 1
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to re-optimize product {product.id}: {str(e)}")
        
        message = f'Successfully re-optimized {optimized_count} product images.'
        if failed_count > 0:
            message += f' Failed to re-optimize {failed_count} images.'
        
        self.message_user(request, message)
    force_reoptimize_images.short_description = "Force re-optimize selected images"
    
    def save_model(self, request, obj, form, change):
        """Custom save logic to track image size changes."""
        if change and obj.image:  
            try:
                old_obj = Product.objects.get(pk=obj.pk)
                if old_obj.image and old_obj.image != obj.image:
                    obj._original_image_size = old_obj.get_image_size()
            except Product.DoesNotExist:
                pass
        
        super().save_model(request, obj, form, change)


@admin.register(FeaturedProducts)
class FeaturedProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'product_type', 'discount_percentage', 'discount_text')
    list_filter = ('discount_percentage',)
    search_fields = ('product__name', 'discount_text')
    
    def product_name(self, obj):
        """Get product name from the related Product."""
        return obj.product.name if obj.product else 'N/A'
    product_name.short_description = 'Product Name'
    
    def product_type(self, obj):
        """Get product type from the related Product."""
        return obj.product.product_type if obj.product else 'N/A'
    product_type.short_description = 'Product Type'
