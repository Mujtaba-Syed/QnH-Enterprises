from rest_framework import serializers
from .models import Product, FeaturedProducts, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for ProductImage model."""
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'order', 'is_active']


class ProductSerializer(serializers.ModelSerializer):
    additional_images = ProductImageSerializer(many=True, read_only=True)
    discounted_price = serializers.ReadOnlyField()
    has_discount = serializers.ReadOnlyField()
    all_images = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def get_all_images(self, obj):
        """Get all images including main image and additional images."""
        return obj.get_all_images()


class ProductDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for product detail page."""
    additional_images = ProductImageSerializer(many=True, read_only=True)
    discounted_price = serializers.ReadOnlyField()
    has_discount = serializers.ReadOnlyField()
    all_images = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'product_type', 'sku', 'price', 
            'brand', 'image', 'additional_images', 'all_images',
            'attributes', 'is_active', 'newly_added', 'best_seller', 
            'rating', 'discount_percentage', 'discount_text', 
            'discounted_price', 'has_discount', 'number_of_sales'
        ]
    
    def get_all_images(self, obj):
        """Get all images including main image and additional images."""
        return obj.get_all_images()


class FeaturedProductsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_image = serializers.ImageField(source='product.image')
    product_id = serializers.IntegerField(source='product.id')
    class Meta:
        model = FeaturedProducts
        fields = ['id', 'product_name', 'product_image', 'product_id', 'discount_percentage', 'discount_text']

class NewlyAddedProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'price', 'brand', 'product_type','description']

class BestSellerProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'price', 'brand', 'product_type', 'rating']


class ProductTypeCountSerializer(serializers.Serializer):
    product_type = serializers.CharField()
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
            'watches': 'fas fa-clock',
        }
        return icon_map.get(obj['product_type'], 'fas fa-box-open') 