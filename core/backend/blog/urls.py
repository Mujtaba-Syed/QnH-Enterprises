from django.urls import path
from .views import BlogViewSet

urlpatterns = [
    path('', BlogViewSet.as_view({'get': 'list'}), name='blog-list'),
    path('<int:pk>/', BlogViewSet.as_view({'get': 'retrieve'}), name='blog-detail'),
]