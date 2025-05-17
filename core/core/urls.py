"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import( HomeView, PageNotFoundView, CartView, CheckoutView, 
        ContactView, ShopDetailView, ShopView, TestimonialView, 
            PrivacyPolicyView, TermsOfUseView, SalesAndRefundPolicyView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('404/', PageNotFoundView.as_view(), name='404'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('shop-detail/', ShopDetailView.as_view(), name='shop-detail'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('testimonial/', TestimonialView.as_view(), name='testimonial'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-of-use/', TermsOfUseView.as_view(), name='terms-of-use'),
    path('sales-and-refund-policy/', SalesAndRefundPolicyView.as_view(), name='sales-and-refund-policy'),

    path('api/products/', include('backend.products.urls')),
    path('api/reviews/', include('backend.reviews.urls')),
    path('accounts/', include('backend.authentication.urls')),
    path('api/cart/', include('backend.cart.urls')),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)