from rest_framework import serializers
from .models import Cart, CartItem
from backend.products.models import Product
from decimal import Decimal


class ProductMiniSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']

    def get_price(self, obj):
        return f"{obj.price:.2f} $"  # Assumes obj.price is Decimal


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductMiniSerializer()
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total']

    def get_total(self, obj):
        total = obj.product.price * obj.quantity  # Decimal * int
        return f"{total:.2f} $"


class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.SerializerMethodField()
    shipping = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items', 'subtotal', 'shipping', 'total']

    def get_subtotal(self, obj):
        subtotal = sum(item.product.price * item.quantity for item in obj.items.all())
        return f"{subtotal:.2f}"

    def get_shipping(self, obj):
        return f"{Decimal('53.00'):.2f}"  # Flat rate shipping

    def get_total(self, obj):
        subtotal = sum(item.product.price * item.quantity for item in obj.items.all())
        total = subtotal + Decimal('53.00')
        return f"{total:.2f}"
