from django.contrib import admin
from .models import Blog

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'slug', 'is_published', 'created_at', 'updated_at', 'get_image_size', 'get_image_dimensions')
    list_filter = ('is_published', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    
    def get_image_size(self, obj):
        """Display image size in admin list."""
        size = obj.get_image_size()
        return f"{size} MB" if size > 0 else "No image"
    get_image_size.short_description = 'Image Size'
    
    def get_image_dimensions(self, obj):
        """Display image dimensions in admin list."""
        dimensions = obj.get_image_dimensions()
        if dimensions:
            return f"{dimensions[0]}x{dimensions[1]}"
        return "No image"
    get_image_dimensions.short_description = 'Image Dimensions'

admin.site.register(Blog, BlogAdmin)