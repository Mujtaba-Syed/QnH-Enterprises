from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Blog
from .serializers import BlogSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = BlogSerializer
    pagination_class = PageNumberPagination
    # lookup_field = 'id'
    
    def get_queryset(self):
        """Allow filtering by id."""
        queryset = Blog.objects.filter(is_published=True).order_by('-created_at')
        return queryset
    
