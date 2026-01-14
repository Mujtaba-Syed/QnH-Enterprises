from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin for OrderItem."""
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal', 'unit_price_after_discount', 'created_at', 'updated_at')
    fields = ('product', 'product_name', 'product_sku', 'quantity', 'price', 'discount_percentage', 'subtotal', 'unit_price_after_discount', 'created_at', 'updated_at')
    can_delete = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model."""
    
    list_display = (
        'order_number', 
        'full_name', 
        'mobile', 
        'email',
        'total_amount', 
        'payment_status', 
        'order_status', 
        'payment_method',
        'created_at',
        'is_guest_order'
    )
    
    list_filter = (
        'order_status',
        'payment_status',
        'payment_method',
        'is_guest_order',
        'created_at',
        'country',
        'city'
    )
    
    search_fields = (
        'order_number',
        'first_name',
        'last_name',
        'email',
        'mobile',
        'address',
        'city',
        'tracking_number'
    )
    
    readonly_fields = (
        'order_number',
        'created_at',
        'updated_at',
        'get_total_items',
        'is_paid',
        'is_delivered',
        'full_name'
    )
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'is_guest_order', 'created_at', 'updated_at')
        }),
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'full_name', 'email', 'mobile')
        }),
        ('Billing Address', {
            'fields': ('address', 'city', 'country', 'zipcode')
        }),
        ('Shipping Address', {
            'fields': ('ship_to_different_address', 'shipping_address', 'shipping_city', 'shipping_country', 'shipping_zipcode'),
            'classes': ('collapse',)
        }),
        ('Order Details', {
            'fields': ('order_notes', 'total_amount', 'get_total_items')
        }),
        ('Payment Information', {
            'fields': (
                'payment_method',
                'payment_status',
                'payment_transaction_id',
                'payment_receipt',
                'payment_date',
                'is_paid'
            )
        }),
        ('Order Status & Tracking', {
            'fields': (
                'order_status',
                'tracking_number',
                'tracking_url',
                'confirmed_at',
                'shipped_at',
                'delivered_at',
                'is_delivered'
            )
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [OrderItemInline]
    
    date_hierarchy = 'created_at'
    
    ordering = ('-created_at',)
    
    def get_total_items(self, obj):
        """Display total items in order."""
        return obj.get_total_items
    get_total_items.short_description = 'Total Items'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for OrderItem model."""
    
    list_display = (
        'id',
        'order',
        'product',
        'product_name',
        'quantity',
        'price',
        'discount_percentage',
        'subtotal',
        'unit_price_after_discount',
        'created_at'
    )
    
    list_filter = (
        'created_at',
        'discount_percentage',
        'order__order_status',
        'order__payment_status'
    )
    
    search_fields = (
        'order__order_number',
        'product_name',
        'product_sku',
        'product__name'
    )
    
    readonly_fields = (
        'subtotal',
        'unit_price_after_discount',
        'created_at',
        'updated_at'
    )
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order',)
        }),
        ('Product Information', {
            'fields': ('product', 'product_name', 'product_sku')
        }),
        ('Pricing', {
            'fields': ('quantity', 'price', 'discount_percentage', 'subtotal', 'unit_price_after_discount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-created_at',)
