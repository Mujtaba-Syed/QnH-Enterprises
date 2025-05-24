from django.urls import path
from .views import (ProductReviewListAPIView, AddReviewAPIView, ActiveReviewsApiView)

urlpatterns = [
    path('<int:product_id>/product-reviews/', ProductReviewListAPIView.as_view(), name='product-review-list'),
    path('<int:product_id>/reviews-add/', AddReviewAPIView.as_view(), name='add-review'),
    path('active-reviews/', ActiveReviewsApiView.as_view(), name='active-reviews' ),
]
