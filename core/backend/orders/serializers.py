from rest_framework import serializers
from .models import Order, OrderItem
from backend.products.models import Product
from decimal import Decimal


class OrderItemSerializer(serializers.Serializer):
    """Serializer for order items in request."""
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(min_value=1, required=True)
    
    def validate_product_id(self, value):
        """Validate that product exists and is active."""
        try:
            product = Product.objects.get(id=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Product with ID {value} does not exist or is not active.")
        return value


class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating a new order."""
    
    # Customer Information
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    mobile = serializers.CharField(max_length=20, required=True)
    
    # Billing Address
    address = serializers.CharField(required=True)
    city = serializers.CharField(max_length=100, required=True)
    country = serializers.CharField(max_length=100, required=False, default='Pakistan')
    zipcode = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    # Shipping Address (optional)
    ship_to_different_address = serializers.BooleanField(required=False, default=False)
    shipping_address = serializers.CharField(required=False, allow_blank=True)
    shipping_city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    shipping_country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    shipping_zipcode = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    # Order Details
    order_notes = serializers.CharField(required=False, allow_blank=True)
    payment_method = serializers.ChoiceField(
        choices=Order.PAYMENT_METHOD_CHOICES,
        required=False,
        default='whatsapp'
    )
    
    # Order Items
    items = OrderItemSerializer(many=True, required=True)
    
    def validate_items(self, value):
        """Validate that items list is not empty."""
        if not value or len(value) == 0:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value
    
    def validate(self, attrs):
        """Validate shipping address if ship_to_different_address is True."""
        if attrs.get('ship_to_different_address'):
            if not attrs.get('shipping_address') or not attrs.get('shipping_city'):
                raise serializers.ValidationError(
                    "Shipping address and city are required when shipping to a different address."
                )
        return attrs


class OrderItemReadSerializer(serializers.ModelSerializer):
    """Serializer for reading order items."""
    product_name = serializers.CharField(read_only=True)
    product_sku = serializers.CharField(read_only=True)
    unit_price_after_discount = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name', 'product_sku', 
            'quantity', 'price', 'discount_percentage', 
            'subtotal', 'unit_price_after_discount'
        ]
        read_only_fields = ['id', 'subtotal']
    
    def get_unit_price_after_discount(self, obj):
        """Return unit price after discount."""
        return str(obj.unit_price_after_discount)


class OrderReadSerializer(serializers.ModelSerializer):
    """Serializer for reading order details."""
    items = OrderItemReadSerializer(many=True, read_only=True)
    full_name = serializers.CharField(read_only=True)
    get_total_items = serializers.IntegerField(read_only=True)
    is_paid = serializers.BooleanField(read_only=True)
    is_delivered = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'first_name', 'last_name', 
            'full_name', 'email', 'mobile', 'address', 'city', 
            'country', 'zipcode', 'ship_to_different_address',
            'shipping_address', 'shipping_city', 'shipping_country',
            'shipping_zipcode', 'order_notes', 'total_amount',
            'payment_method', 'payment_status', 'payment_transaction_id',
            'order_status', 'tracking_number', 'tracking_url',
            'items', 'get_total_items', 'is_paid', 'is_delivered',
            'created_at', 'updated_at', 'confirmed_at', 'shipped_at',
            'delivered_at', 'is_guest_order'
        ]
        read_only_fields = [
            'id', 'order_number', 'created_at', 'updated_at',
            'confirmed_at', 'shipped_at', 'delivered_at'
        ]

