from django.views.generic import TemplateView
import requests
from django.conf import settings


class HomeView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #to get all products
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

        #to get featured products
        response = requests.get(f'{settings.BASE_URL}/api/products/get-featured-products/')
        if response.status_code == 200:
            featured_products = response.json()
        else:
            featured_products = []
        
        for product in featured_products:
            if product['product_image']:
                if not product['product_image'].startswith("http"):
                    product['product_image'] = f'{settings.BASE_URL}{product["product_image"]}'
                else:
                    product['product_image'] = f'{settings.BASE_URL}{product["product_image"]}' 
            else:
                product['product_image'] = ''
        
   
        #to get newly added products
        response = requests.get(f'{settings.BASE_URL}/api/products/get-newly-added-products/')
        if response.status_code == 200:
            newly_added_products = response.json()
        else:
            newly_added_products = []

        for product in newly_added_products:
            if product['image']:
                if not product['image'].startswith("http"):
                    product['image'] = f'{settings.BASE_URL}{product["image"]}'
                else:
                    product['image'] = f'{settings.BASE_URL}{product["image"]}'
            else:
                product['image'] = ''
        #to get best seller products
        response = requests.get(f'{settings.BASE_URL}/api/products/get-best-seller-products/')
        if response.status_code == 200:
            best_seller_products = response.json()
        else:
            best_seller_products = []
            
        for product in best_seller_products:
            if product['image']:
                if not product['image'].startswith("http"):
                    product['image'] = f'{settings.BASE_URL}{product["image"]}'
                else:
                    product['image'] = f'{settings.BASE_URL}{product["image"]}'
            else:
                product['image'] = ''
                    
        #for testimonial section
        response= requests.get(f'{settings.BASE_URL}/api/reviews/active-reviews/')
        if response.status_code ==200:
            client_review=response.json()
        else:
            client_review= []
        for product in client_review:
            if product['image']:
                if not product['image'].startswith("http"):
                    product['image'] = f'{settings.BASE_URL}{product["image"]}'
                else:
                    product['image'] = f'{settings.BASE_URL}{product["image"]}'
            else:
                product['image'] = ''
        context['categorized_products'] = categorized_products
        context['featured_products'] = featured_products
        context['newly_added_products'] = newly_added_products
        context['best_seller_products'] = best_seller_products
        context['client_review'] = client_review

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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get(f'{settings.BASE_URL}/api/products/get-product-type-count/')
        if response.status_code == 200:
            side_cat_filters = response.json()
        else:
            side_cat_filters = []
        context['side_cat_filters'] = side_cat_filters

        return context

class TestimonialView(TemplateView):
    template_name = 'testimonial.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'privacy-policy.html'

class TermsOfUseView(TemplateView):
    template_name = 'terms-of-use.html'

class SalesAndRefundPolicyView(TemplateView):
    template_name = 'sales-and-refund-policy.html'


class LoginView(TemplateView):
    template_name = 'login.html'

class RegisterView(TemplateView):
    template_name = 'register.html'

