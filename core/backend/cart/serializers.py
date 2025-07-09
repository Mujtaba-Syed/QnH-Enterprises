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
        return f"{obj.price:.2f}"  


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductMiniSerializer()
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total']

    def get_total(self, obj):
        total = obj.product.price * obj.quantity  
        return f"{total:.2f} "


class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(
        help_text="ID of the product to add to cart"
    )

    def validate_product_id(self, value):
        """Validate that product exists"""
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist")
        return value


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(
        min_value=1,
        help_text="New quantity for the cart item"
    )


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items', 'subtotal', 'total', 'item_count', 'total_quantity']

    def get_subtotal(self, obj):
        subtotal = sum(item.product.price * item.quantity for item in obj.items.all())
        return f"{subtotal:.2f}"

    def get_total(self, obj):
        subtotal = sum(item.product.price * item.quantity for item in obj.items.all())
        return f"{subtotal:.2f}"

    def get_item_count(self, obj):
        """Get total number of unique items in cart"""
        return obj.items.count()

    def get_total_quantity(self, obj):
        """Get total quantity of all items in cart (sum of all quantities)"""
        return sum(item.quantity for item in obj.items.all())
