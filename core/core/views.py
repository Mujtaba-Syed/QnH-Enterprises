from django.views.generic import TemplateView
import requests
from django.conf import settings


class HomeView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get(f'{settings.BASE_URL}/api/products/get-all-products/')
        
        if response.status_code == 200:
            products = response.json()
        else:
            products = []

        for product in products:
            if product['image']:
                if not product['image'].startswith("http"):
                    product['image'] = f'{settings.BASE_URL}{product["image"]}'
                    print('with media',product['image'])
                else:
                    product['image'] = f'{settings.BASE_URL}{product["image"]}'
                    print('without media',product['image'])
            else:
                product['image'] = ''

        categorized_products = {
            'all_products': products,
            'perfumes': [product for product in products if product['product_type'] == 'perfume'],
            'shirts': [product for product in products if product['product_type'] == 'shirt'],
            'mobile_accessories': [product for product in products if product['product_type'] == 'mobile_accessories'],
            'cars': [product for product in products if product['product_type'] == 'car'],
        }

        context['categorized_products'] = categorized_products
        return context

class PageNotFoundView(TemplateView):
    template_name = '404.html'

class CartView(TemplateView):
    template_name = 'cart.html'

class CheckoutView(TemplateView):
    template_name = 'checkout.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

class ShopDetailView(TemplateView):
    template_name = 'shop-detail.html'

class ShopView(TemplateView):
    template_name = 'shop.html'

class TestimonialView(TemplateView):
    template_name = 'testimonial.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'privacy-policy.html'

class TermsOfUseView(TemplateView):
    template_name = 'terms-of-use.html'

class SalesAndRefundPolicyView(TemplateView):
    template_name = 'sales-and-refund-policy.html'




