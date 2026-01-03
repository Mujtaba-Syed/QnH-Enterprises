from django.urls import path
from .views import TestEmailView, TestOrderEmailView

urlpatterns = [
    path('test-email/', TestEmailView.as_view(), name='test-email'),
    path('test-order-email/', TestOrderEmailView.as_view(), name='test-order-email'),
]

