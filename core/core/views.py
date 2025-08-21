from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.utils import timezone
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from backend.products.models import Product
import xml.etree.ElementTree as ET
from xml.dom import minidom
import requests
from django.conf import settings
from urllib.parse import urljoin


class HomeView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #to get all products
        response = requests.get(f'{settings.BASE_URL}/api/products/get-all-products/')
        
        if response.status_code == 200:
            data = response.json()
            products = data.get("results", [])
        else:
            products = []

        for product in products:
            image = product.get('image')
            if image:
                if image.startswith("http"):
                    product['image'] = image
                else:
                    product['image'] = urljoin(settings.BASE_URL, image)
            else:
                product['image'] = ''

        categorized_products = {
            'all_products': products,
            'perfumes': [product for product in products if product['product_type'] == 'perfume'],
            'shirts': [product for product in products if product['product_type'] == 'shirt'],
            'mobile_accessories': [product for product in products if product['product_type'] == 'mobile_accessories'],
            'cars': [product for product in products if product['product_type'] == 'car'],
            'watches': [product for product in products if product['product_type'] == 'watches'],
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

def custom_404(request, exception):
    """Custom 404 handler for all non-existent URLs"""
    return render(request, '404.html', status=404)

class CartView(TemplateView):
    template_name = 'cart.html'

class CheckoutView(TemplateView):
    template_name = 'checkout.html'

class ContactView(TemplateView):
    template_name = 'contact.html'


class ShopView(TemplateView):
    template_name = 'shop.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get parameters from request
        page = self.request.GET.get('page', 1)
        page_size = self.request.GET.get('page_size', 6)  
        search = self.request.GET.get('search', '')
        category = self.request.GET.get('category', '')
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')
        
        # Build API parameters for filtering
        api_params = {
            'page': page,
            'page_size': page_size
        }
        
        # Use the new filtering API if we have specific filters
        if category or min_price or max_price:
            filter_params = {}
            if category:
                filter_params['product_type'] = category
            if min_price:
                filter_params['min_price'] = min_price
            if max_price:
                filter_params['max_price'] = max_price
            if search:
                filter_params['search'] = search
                
            # Use the advanced filtering API
            response = requests.get(f'{settings.BASE_URL}/api/products/filter-products/', params=filter_params)
        else:
            # Use the regular products API with search
            if search:
                api_params['search'] = search
            
            response = requests.get(f'{settings.BASE_URL}/api/products/get-all-products/', params=api_params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Handle different response formats
            if 'results' in data:
                products = data.get("results", [])
                total_count = data.get('count', 0)
                
                # Calculate pagination for filtered results
                if category or min_price or max_price:
                    # For filtered results, we'll do client-side pagination
                    start_idx = (int(page) - 1) * int(page_size)
                    end_idx = start_idx + int(page_size)
                    products = products[start_idx:end_idx]
                    total_pages = (total_count + int(page_size) - 1) // int(page_size)
                else:
                    # For regular API, use server pagination
                    total_pages = data.get('pages', 0)
            else:
                products = data
                total_count = len(products)
                total_pages = 1
            
            current_page = int(page)
            
            # Generate page range for pagination
            page_range = list(range(1, total_pages + 1))
            
            pagination_info = {
                'count': total_count,
                'pages': total_pages,
                'current_page': current_page,
                'has_next': current_page < total_pages,
                'has_previous': current_page > 1,
                'next_page': current_page + 1 if current_page < total_pages else None,
                'previous_page': current_page - 1 if current_page > 1 else None,
                'page_range': page_range,
            }
        else:
            products = []
            pagination_info = {
                'count': 0,
                'pages': 0,
                'current_page': 1,
                'has_next': False,
                'has_previous': False,
                'next_page': None,
                'previous_page': None,
                'page_range': [],
            }

        # Process product images
        for product in products:
            image = product.get('image')
            if image:
                if image.startswith("http"):
                    product['image'] = image
                else:
                    product['image'] = urljoin(settings.BASE_URL, image)
            else:
                product['image'] = ''

        # Get category filters with counts
        response = requests.get(f'{settings.BASE_URL}/api/products/get-product-type-count/')
        if response.status_code == 200:
            side_cat_filters = response.json()
        else:
            side_cat_filters = []

        # Get featured products
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

        context['products'] = products
        context['pagination_info'] = pagination_info
        context['side_cat_filters'] = side_cat_filters
        context['current_search'] = search
        context['current_category'] = category
        context['current_min_price'] = min_price
        context['current_max_price'] = max_price
        context['featured_products'] = featured_products

        return context

class TestimonialView(TemplateView):
    template_name = 'testimonial.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
       
        context['client_review'] = client_review

        return context

class PrivacyPolicyView(TemplateView):
    template_name = 'privacy-policy.html'

class TermsOfUseView(TemplateView):
    template_name = 'terms-of-use.html'

class SalesAndRefundPolicyView(TemplateView):
    template_name = 'sales-and-refund-policy.html'

class AboutUsView(TemplateView):
    template_name = 'about-us.html'

class LoginView(TemplateView):
    template_name = 'login.html'

class RegisterView(TemplateView):
    template_name = 'register.html'

class OAuthSuccessView(TemplateView):
    template_name = 'oauth-success.html'

class SitemapView(TemplateView):
    def get(self, request, *args, **kwargs):
        # Create the XML structure
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        
        # Static pages
        static_pages = [
                    {'loc': 'https://qhenterprises.com/', 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': 'https://qhenterprises.com/shop/', 'priority': '0.9', 'changefreq': 'daily'},
        {'loc': 'https://qhenterprises.com/contact/', 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': 'https://qhenterprises.com/testimonial/', 'priority': '0.7', 'changefreq': 'weekly'},
        {'loc': 'https://qhenterprises.com/privacy-policy/', 'priority': '0.5', 'changefreq': 'yearly'},
        {'loc': 'https://qhenterprises.com/terms-of-use/', 'priority': '0.5', 'changefreq': 'yearly'},
        {'loc': 'https://qhenterprises.com/sales-and-refund-policy/', 'priority': '0.5', 'changefreq': 'yearly'},
        ]
        
        current_date = timezone.now().strftime('%Y-%m-%d')
        
        for page in static_pages:
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = page['loc']
            ET.SubElement(url, 'lastmod').text = current_date
            ET.SubElement(url, 'changefreq').text = page['changefreq']
            ET.SubElement(url, 'priority').text = page['priority']
        
        # Add product pages (if you have individual product pages)
        products = Product.objects.filter(is_active=True)
        for product in products:
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = f"https://qhenterprises.com/shop-detail/{product.id}/"
            ET.SubElement(url, 'lastmod').text = product.updated_at.strftime('%Y-%m-%d') if hasattr(product, 'updated_at') else current_date
            ET.SubElement(url, 'changefreq').text = 'weekly'
            ET.SubElement(url, 'priority').text = '0.8'
        
        # Create pretty XML
        rough_string = ET.tostring(urlset, 'unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        return HttpResponse(pretty_xml, content_type='application/xml')

class ProductDetailView(TemplateView):
    template_name = 'product-detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('product_id')
        response = requests.get(f'{settings.BASE_URL}/api/products/product-detail/{product_id}/')
        if response.status_code == 200:
            product = response.json()
        else:
            product = {}
        context['product'] = product
        return context