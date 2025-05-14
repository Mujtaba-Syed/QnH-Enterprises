from django.urls import path
from .views import CartDetailView, CartItemView, CartItemDetailView

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart-detail'),
    path('items/', CartItemView.as_view(), name='cart-item-list'),
    path('items/<int:product_id>/', CartItemDetailView.as_view(), name='cart-item-detail'),
]