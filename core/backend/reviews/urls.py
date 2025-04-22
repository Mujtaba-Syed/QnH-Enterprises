from django.urls import path
from .views import ReviewListAPIView, ReviewDetailAPIView

urlpatterns = [
    path('reviews/', ReviewListAPIView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),
]
