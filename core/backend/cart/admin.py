from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]
    search_fields = ['user__username']
    list_filter = ['created_at']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ['product__name', 'cart__user__username']
    list_filter = ['product']

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
