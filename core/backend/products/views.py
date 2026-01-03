from django.db.models import Count, Q, Avg
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, FeaturedProducts
from .serializers import (ProductSerializer, 
                          FeaturedProductsSerializer, 
                          NewlyAddedProductsSerializer, 
                          BestSellerProductsSerializer,
                          ProductTypeCountSerializer,
                          ProductDetailSerializer
                          )


from rest_framework import status, pagination, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound, APIException
from drf_spectacular.utils import extend_schema
import random


class ProductFilter(filters.FilterSet):
    """Filter for products by type and price range."""
    product_type = filters.CharFilter(field_name='product_type', lookup_expr='exact')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    brand = filters.CharFilter(field_name='brand', lookup_expr='icontains')
    rating = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    
    class Meta:
        model = Product
        fields = ['product_type', 'min_price', 'max_price', 'brand', 'rating']


class ProductPagination(pagination.PageNumberPagination):
    page_size = 10 
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "pages": self.page.paginator.num_pages,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )


class ProductView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    pagination_class = ProductPagination 
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter
    serializer_class = ProductSerializer

    def get_queryset(self):
        try:
            queryset = Product.objects.filter(is_active=True).order_by('-created_at')
            if not queryset.exists():
                raise NotFound(detail="No active products found.")
            return queryset
        except Exception as e:
            raise APIException(detail=f"Failed to fetch products: {str(e)}")


class FilteredProductsAPIView(APIView):
    """API for advanced filtering of products by type and price range."""
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    
    @extend_schema(
        summary="Filter Products",
        description="Advanced filtering of products by type, price range, brand, rating, season, and gender",
        responses={200: ProductSerializer(many=True)},
        tags=['Products']
    )
    def get(self, request):
        try:
            product_type = request.query_params.get('product_type')
            min_price = request.query_params.get('min_price')
            max_price = request.query_params.get('max_price')
            brand = request.query_params.get('brand')
            rating = request.query_params.get('rating')
            season = request.query_params.get('season')  # summer or winter
            gender = request.query_params.get('gender')  # male or female
            
            queryset = Product.objects.filter(is_active=True)
            
            if product_type:
                queryset = queryset.filter(product_type=product_type)
            
            if min_price:
                try:
                    min_price = float(min_price)
                    queryset = queryset.filter(price__gte=min_price)
                except ValueError:
                    return Response(
                        {'error': 'Invalid min_price parameter'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            if max_price:
                try:
                    max_price = float(max_price)
                    queryset = queryset.filter(price__lte=max_price)
                except ValueError:
                    return Response(
                        {'error': 'Invalid max_price parameter'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            if brand:
                queryset = queryset.filter(brand__icontains=brand)
            
            if rating:
                try:
                    rating = int(rating)
                    queryset = queryset.filter(rating__gte=rating)
                except ValueError:
                    return Response(
                        {'error': 'Invalid rating parameter'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Filter by season (for clothing products)
            if season:
                queryset = queryset.filter(attributes__season=season)
            
            # Filter by gender (for clothing products)
            if gender:
                queryset = queryset.filter(attributes__gender=gender)
            
            if not queryset.exists():
                return Response(
                    {'message': 'No products found with the specified filters', 'results': []},
                    status=status.HTTP_200_OK
                )
            
            serializer = ProductSerializer(queryset, many=True)
            return Response({
                'count': queryset.count(),
                'filters_applied': {
                    'product_type': product_type,
                    'min_price': min_price,
                    'max_price': max_price,
                    'brand': brand,
                    'rating': rating,
                    'season': season,
                    'gender': gender
                },
                'results': serializer.data
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to filter products: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductsByTypeAPIView(APIView):
    """API to get products filtered by specific product type."""
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    
    @extend_schema(
        summary="Get Products by Type",
        description="Get all products filtered by a specific product type",
        responses={200: ProductSerializer(many=True)},
        tags=['Products']
    )
    def get(self, request, product_type):
        try:
            valid_types = [choice[0] for choice in Product.TYPE_CHOICES]
            if product_type not in valid_types:
                return Response(
                    {'error': f'Invalid product type. Valid types are: {", ".join(valid_types)}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            products = Product.objects.filter(
                product_type=product_type, 
                is_active=True
            )
            
            if not products.exists():
                return Response(
                    {'message': f'No {product_type} products found', 'results': []},
                    status=status.HTTP_200_OK
                )
            
            serializer = ProductSerializer(products, many=True)
            return Response({
                'product_type': product_type,
                'count': products.count(),
                'results': serializer.data
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch {product_type} products: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductsByPriceRangeAPIView(APIView):
    """API to get products filtered by price range."""
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    
    @extend_schema(
        summary="Get Products by Price Range",
        description="Get products filtered by minimum and maximum price",
        responses={200: ProductSerializer(many=True)},
        tags=['Products']
    )
    def get(self, request):
        try:
            min_price = request.query_params.get('min_price', 0)
            max_price = request.query_params.get('max_price')
            
            try:
                min_price = float(min_price)
                if max_price:
                    max_price = float(max_price)
                    if min_price > max_price:
                        return Response(
                            {'error': 'min_price cannot be greater than max_price'}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
            except ValueError:
                return Response(
                    {'error': 'Invalid price parameters. Must be numeric.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            queryset = Product.objects.filter(is_active=True, price__gte=min_price)
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            
            if not queryset.exists():
                return Response(
                    {'message': f'No products found in price range RS{min_price} - RS{max_price if max_price else "∞"}', 'results': []},
                    status=status.HTTP_200_OK
                )
            
            serializer = ProductSerializer(queryset, many=True)
            return Response({
                'price_range': {
                    'min_price': min_price,
                    'max_price': max_price
                },
                'count': queryset.count(),
                'results': serializer.data
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to filter products by price: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FeaturedProdcutsApiView(APIView):
    serializer_class = FeaturedProductsSerializer
    
    @extend_schema(
        summary="Get Featured Products",
        description="Get all featured products",
        responses={200: FeaturedProductsSerializer(many=True)},
        tags=['Products']
    )
    def get(self, request):
        try:
            featured_products = FeaturedProducts.objects.all()
            serializer = FeaturedProductsSerializer(featured_products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NewlyAddedProductsApiView(APIView):
    serializer_class = NewlyAddedProductsSerializer
    
    @extend_schema(
        summary="Get Newly Added Products",
        description="Get all newly added products",
        responses={200: NewlyAddedProductsSerializer(many=True)},
        tags=['Products']
    )
    def get(self, request):
        try:
            newly_added_products = Product.objects.filter(newly_added=True)
            serializer = NewlyAddedProductsSerializer(newly_added_products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BestSellerProductsApiView(APIView):
    serializer_class = BestSellerProductsSerializer
    
    @extend_schema(
        summary="Get Best Seller Products",
        description="Get all best seller products",
        responses={200: BestSellerProductsSerializer(many=True)},
        tags=['Products']
    )
    def get(self, request):
        try:
            best_seller_products = Product.objects.filter(best_seller=True)
            serializer = BestSellerProductsSerializer(best_seller_products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductTypeCountAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ProductTypeCountSerializer
    
    @extend_schema(
        summary="Get Product Type Counts",
        description="Get count of products by each product type",
        responses={200: ProductTypeCountSerializer(many=True)},
        tags=['Products']
    )
    def get(self, request):
        product_counts = Product.objects.values('product_type').annotate(count=Count('id'))

        count_dict = {item['product_type']: item['count'] for item in product_counts}

        full_data = [
            {
                'product_type': key,
                'count': count_dict.get(key, 0)
            }
            for key, _ in Product.TYPE_CHOICES
        ]

        serializer = ProductTypeCountSerializer(full_data, many=True)
        return Response(serializer.data)


class ProductDetailAPIView(APIView):
    """API for getting detailed product information including all images."""
    permission_classes = [AllowAny]
    serializer_class = ProductDetailSerializer
    
    @extend_schema(
        summary="Get Product Details",
        description="Get detailed information about a specific product including images and reviews",
        responses={200: ProductDetailSerializer},
        tags=['Products']
    )
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            
            # Get product reviews
            try:
                reviews = product.reviews.filter(is_active=True).order_by('-created_at')
            except Exception as e:
                # If there's an issue with reviews, continue without them
                reviews = []
                print(f"Warning: Could not fetch reviews for product {product_id}: {e}")
            
            # Serialize product with all details
            try:
                product_serializer = ProductDetailSerializer(product)
                product_data = product_serializer.data
            except Exception as e:
                return Response(
                    {'error': f'Failed to serialize product: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Prepare response data
            response_data = {
                'product': product_data,
                'reviews': {
                    'count': len(reviews) if reviews else 0,
                    'average_rating': 0,
                    'reviews': []
                }
            }
            
            # Calculate average rating if reviews exist
            if reviews:
                try:
                    avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
                    response_data['reviews']['average_rating'] = avg_rating
                except Exception as e:
                    print(f"Warning: Could not calculate average rating: {e}")
                    response_data['reviews']['average_rating'] = 0
            
            # Add review details if needed
            if reviews:
                for review in reviews[:10]:  # Limit to 10 most recent reviews
                    try:
                        review_data = {
                            'id': review.id,
                            'name': review.name,
                            'rating': review.rating,
                            'description': review.description,
                            'image': None,
                            'created_at': review.created_at
                        }
                        
                        # Safely get image URL
                        if review.image:
                            try:
                                review_data['image'] = review.image.url
                            except Exception:
                                review_data['image'] = None
                        
                        response_data['reviews']['reviews'].append(review_data)
                    except Exception as e:
                        print(f"Warning: Could not serialize review {review.id}: {e}")
                        continue
            
            return Response(response_data)
            
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found or inactive'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch product details: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RandomProductsAPIView(APIView):
    """API for getting random products for product slider."""
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    
    @extend_schema(
        summary="Get Random Products",
        description="Get random products for product slider (up to 8 products)",
        responses={200: ProductSerializer(many=True)},
        tags=['Products']
    )
    def get(self, request):
        try:
            products = Product.objects.filter(is_active=True)
            
            product_list = list(products)
            random.shuffle(product_list)
            
            random_products = product_list[:8]
            
            serializer = ProductSerializer(random_products, many=True)
            
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch random products: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
