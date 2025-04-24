from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'rating', 'is_active', 'created_at', 'updated_at') 
    list_filter = ('product', 'rating', 'is_active', 'created_at') 
    search_fields = ('name', 'description', 'product__name') 
    readonly_fields = ('created_at', 'updated_at')
