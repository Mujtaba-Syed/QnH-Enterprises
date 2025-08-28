from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    # image_size = serializers.SerializerMethodField()
    # image_dimensions = serializers.SerializerMethodField()
    # optimization_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'content', 'image', 
            'meta_description', 'keywords', 'is_published',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            return obj.image.url
        return None
    def get_image_size(self, obj):
        """Get image size in MB."""
        return obj.get_image_size()
    
    def get_image_dimensions(self, obj):
        """Get image dimensions."""
        dimensions = obj.get_image_dimensions()
        if dimensions:
            return f"{dimensions[0]}x{dimensions[1]}"
        return None
    
    def get_optimization_info(self, obj):
        """Get image optimization information."""
        return obj.get_optimization_info()