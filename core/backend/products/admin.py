from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'product_type','newly_added', 'best_seller', 'is_active')
    list_filter = ('product_type', 'is_active')
    search_fields = ('name', 'description')




admin.site.register(Product, ProductAdmin)
admin.site.register(FeaturedProducts)
