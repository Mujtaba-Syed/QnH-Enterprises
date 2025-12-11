from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Review
from .serializers import ReviewSerializer
from backend.products.models import Product
from django.shortcuts import get_object_or_404

class ProductReviewListAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            reviews = Review.objects.filter(product=product, is_active=True)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)


class AddReviewAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            
            data = {}
            
            if 'name' in request.data:
                data['name'] = request.data['name']
            if 'description' in request.data:
                data['description'] = request.data['description']
            if 'rating' in request.data:
                data['rating'] = request.data['rating']
            
            if 'image' in request.FILES:
                data['image'] = request.FILES['image']
            if 'whtsapp_image' in request.FILES:
                data['whtsapp_image'] = request.FILES['whtsapp_image']
            
            data['product'] = product.id
            
            serializer = ReviewSerializer(data=data)
            if serializer.is_valid():
                review = serializer.save()
                review.is_active = False
                review.save()
                
                if not product.is_active:
                    product.is_active = True
                    product.save()
                
                return Response({
                    "message": "Review submitted successfully!",
                    "review_id": review.id,
                    "product_activated": not product.is_active
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Unable to add review: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class ActiveReviewsApiView(APIView):

    def get(self, request):
        try:
            reviews = Review.objects.filter(is_active=True)
            if not reviews.exists():
                return Response({"message": "No active reviews found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)