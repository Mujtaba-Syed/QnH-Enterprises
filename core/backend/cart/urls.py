from django.urls import path
from .views import (
    CartView, 
    ClearCartView, 
    AddToCartView, 
    RemoveFromCartView, 
    UpdateCartItemView, 
    DeleteCartView,
    DecreaseCartItemView,
    CreateGuestUserView,
    GuestAddToCartView,
    GuestCartView
)
from .guest_views import (
    GuestRemoveFromCartView,
    GuestDecreaseCartItemView
)

urlpatterns = [
    path('', CartView.as_view(), name='cart-detail'),
    path('clear/', ClearCartView.as_view(), name='clear-cart'),
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('decrease/<int:product_id>/', DecreaseCartItemView.as_view(), name='decrease-cart-item'),
    path('update/<int:product_id>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('delete/', DeleteCartView.as_view(), name='delete-cart'),
    # Guest cart endpoints
    path('guest/create/', CreateGuestUserView.as_view(), name='create-guest-user'),
    path('guest/add/', GuestAddToCartView.as_view(), name='guest-add-to-cart'),
    path('guest/', GuestCartView.as_view(), name='guest-cart-detail'),
    path('guest/remove/<int:product_id>/', GuestRemoveFromCartView.as_view(), name='guest-remove-from-cart'),
    path('guest/decrease/<int:product_id>/', GuestDecreaseCartItemView.as_view(), name='guest-decrease-cart-item'),
]