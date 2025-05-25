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


class ProductTypeCountSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()
    count = serializers.IntegerField()
    icon_class = serializers.SerializerMethodField()
    def get_name(self, obj):
        type_dict = dict(Product.TYPE_CHOICES)
        return type_dict.get(obj['product_type'], obj['product_type'])
    
    def get_icon_class(self, obj):
        icon_map = {
            'perfume': 'fas fa-wine-bottle',
            'shirt': 'fas fa-tshirt',
            'car': 'fas fa-car',
            'mobile_accessories': 'fas fa-mobile-alt',
        }
        return icon_map.get(obj['product_type'], 'fas fa-box-open') 