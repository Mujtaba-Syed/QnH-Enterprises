from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, FeaturedProducts
from .serializers import ProductSerializer, FeaturedProductsSerializer, NewlyAddedProductsSerializer, BestSellerProductsSerializer
from rest_framework import status

class ProductView(APIView):
    def get(self, request):
        try:
            products = Product.objects.filter(is_active=True)
            if not products:
                return Response({'error': 'No active products found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FeaturedProdcutsApiView(APIView):
    def get(self, request):
        try:
            featured_products = FeaturedProducts.objects.all()
            serializer = FeaturedProductsSerializer(featured_products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NewlyAddedProductsApiView(APIView):
    def get(self, request):
        try:
            newly_added_products = Product.objects.filter(newly_added=True)
            serializer = NewlyAddedProductsSerializer(newly_added_products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BestSellerProductsApiView(APIView):
    def get(self, request):
        try:
            best_seller_products = Product.objects.filter(best_seller=True)
            serializer = BestSellerProductsSerializer(best_seller_products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
