from django.db.models import Count, Q
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, FeaturedProducts
from .serializers import (ProductSerializer, 
                          FeaturedProductsSerializer, 
                          NewlyAddedProductsSerializer, 
                          BestSellerProductsSerializer,
                          ProductTypeCountSerializer
                          )


from rest_framework import status, pagination, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound, APIException


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
    page_size = 100
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "pages": self.page.paginator.num_pages,
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
            queryset = Product.objects.filter(is_active=True)
            if not queryset.exists():
                raise NotFound(detail="No active products found.")
            return queryset
        except Exception as e:
            raise APIException(detail=f"Failed to fetch products: {str(e)}")


class FilteredProductsAPIView(APIView):
    """API for advanced filtering of products by type and price range."""
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            product_type = request.query_params.get('product_type')
            min_price = request.query_params.get('min_price')
            max_price = request.query_params.get('max_price')
            brand = request.query_params.get('brand')
            rating = request.query_params.get('rating')
            
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
                    'rating': rating
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


class ProductTypeCountAPIView(APIView):
    permission_classes = [AllowAny]
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
