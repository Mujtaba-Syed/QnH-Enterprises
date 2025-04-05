from django.urls import path
from .views import ProductView

urlpatterns = [
    path('get-all-products/', ProductView.as_view(), name='get-products'),
]