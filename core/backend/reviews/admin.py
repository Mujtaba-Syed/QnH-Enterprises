from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'is_active', 'created_at', 'updated_at')  # Added is_active
    list_filter = ('rating', 'is_active', 'created_at') 
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
