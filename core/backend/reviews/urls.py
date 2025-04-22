from django.urls import path
from .views import ProductReviewListAPIView, AddReviewAPIView

urlpatterns = [
    path('products/<int:product_id>/reviews/', ProductReviewListAPIView.as_view(), name='product-review-list'),
    path('products/<int:product_id>/reviews/add/', AddReviewAPIView.as_view(), name='add-review'),
]
