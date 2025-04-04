from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'index.html'

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


    




