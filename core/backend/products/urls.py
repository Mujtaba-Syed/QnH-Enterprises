from django.urls import path
from .views import (ProductView, 
                    FeaturedProdcutsApiView,
                    NewlyAddedProductsApiView, 
                    BestSellerProductsApiView,
                    ProductTypeCountAPIView,
                    FilteredProductsAPIView,
                    ProductsByTypeAPIView,
                    ProductsByPriceRangeAPIView
) 

urlpatterns = [
    path('get-all-products/', ProductView.as_view({'get': 'list'}), name='get-products'),
    path('get-featured-products/', FeaturedProdcutsApiView.as_view(), name='get-featured-products'),
    path('get-newly-added-products/', NewlyAddedProductsApiView.as_view(), name='get-newly-added-products'),
    path('get-best-seller-products/', BestSellerProductsApiView.as_view(), name='get-best-seller-products'),
    path('get-product-type-count/', ProductTypeCountAPIView.as_view(), name='get-product-type-count'),
    
    # New filtering endpoints
    path('filter-products/', FilteredProductsAPIView.as_view(), name='filter-products'),
    path('products-by-type/<str:product_type>/', ProductsByTypeAPIView.as_view(), name='products-by-type'),
    path('products-by-price/', ProductsByPriceRangeAPIView.as_view(), name='products-by-price'),
]