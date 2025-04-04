from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
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
