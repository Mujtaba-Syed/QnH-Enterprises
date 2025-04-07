from rest_framework import serializers
from .models import Product, FeaturedProducts

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class FeaturedProductsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_image = serializers.ImageField(source='product.image')
    class Meta:
        model = FeaturedProducts
        fields = ['id', 'product_name', 'product_image', 'discount_percentage', 'discount_text']

class NewlyAddedProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'price', 'brand', 'product_type','description']

class BestSellerProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'price', 'brand', 'product_type', 'rating']

