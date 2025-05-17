from django.urls import path
from .views import (UserCartListView, CartDetailView, CartItemView, 
                   CartItemDetailView, CartClearView)

urlpatterns = [
    path('carts/', UserCartListView.as_view(), name='user-carts'),
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/<int:cart_id>/', CartDetailView.as_view(), name='specific-cart-detail'),
    path('cart/items/', CartItemView.as_view(), name='cart-items'),
    path('cart/items/<int:product_id>/', CartItemDetailView.as_view(), name='cart-item-detail'),
    path('cart/clear/', CartClearView.as_view(), name='clear-cart'),
]