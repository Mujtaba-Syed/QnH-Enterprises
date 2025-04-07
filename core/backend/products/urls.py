from django.urls import path
from .views import ProductView, FeaturedProdcutsApiView,NewlyAddedProductsApiView, BestSellerProductsApiView

urlpatterns = [
    path('get-all-products/', ProductView.as_view(), name='get-products'),
    path('get-featured-products/', FeaturedProdcutsApiView.as_view(), name='get-featured-products'),
    path('get-newly-added-products/', NewlyAddedProductsApiView.as_view(), name='get-newly-added-products'),
    path('get-best-seller-products/', BestSellerProductsApiView.as_view(), name='get-best-seller-products'),
]