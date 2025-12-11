from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Review
from .serializers import ReviewSerializer
from backend.products.models import Product
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

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
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            user = request.user
            
            # Verify user exists in User model (check if it's an actual registered user)
            try:
                user_exists = User.objects.filter(id=user.id).exists()
                if not user_exists:
                    return Response({
                        "error": "You are not eligible to post a review as we are not able to fetch your purchasing record.",
                        "eligible": False
                    }, status=status.HTTP_403_FORBIDDEN)
            except Exception:
                return Response({
                    "error": "You are not eligible to post a review as we are not able to fetch your purchasing record.",
                    "eligible": False
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Check if user already reviewed this product
            existing_review = Review.objects.filter(user=user, product=product).first()
            if existing_review:
                return Response({
                    "error": "You have already submitted a review for this product.",
                    "review_id": existing_review.id
                }, status=status.HTTP_400_BAD_REQUEST)
            
            data = {}
            
            # Auto-populate name from user if not provided
            if 'name' in request.data and request.data['name']:
                data['name'] = request.data['name']
            else:
                # Use user's full name or username as fallback
                if user.first_name or user.last_name:
                    data['name'] = f"{user.first_name} {user.last_name}".strip()
                else:
                    data['name'] = user.username
            
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
                # Link review to authenticated user
                review.user = user
                review.is_active = False  # Reviews need admin approval
                review.save()
                
                if not product.is_active:
                    product.is_active = True
                    product.save()
                
                return Response({
                    "message": "Review submitted successfully! It will be reviewed before being published.",
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