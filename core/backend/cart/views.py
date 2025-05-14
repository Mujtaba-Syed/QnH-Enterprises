from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItem
from backend.products.models import Product
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        try:
            cart, created = Cart.objects.get_or_create(user=user)
            return cart
        except Exception as e:
            raise Exception(f"Error getting cart: {str(e)}")

    def get(self, request):
        try:
            cart = self.get_cart(request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve cart: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        try:
            cart = self.get_cart(request.user)
            deleted_count, _ = cart.items.all().delete()
            if deleted_count == 0:
                return Response(
                    {'message': 'Cart was already empty'},
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {'message': 'Cart cleared successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to clear cart: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        try:
            cart, _ = Cart.objects.get_or_create(user=user)
            return cart
        except Exception as e:
            raise Exception(f"Error getting cart: {str(e)}")

    def post(self, request):
        try:
            serializer = AddCartItemSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            cart = self.get_cart(request.user)
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

            try:
                item = CartItem.objects.get(cart=cart, product=product)
                item.quantity += quantity
                item.save()
                return Response(CartItemSerializer(item).data, status=status.HTTP_200_OK)
            except CartItem.DoesNotExist:
                item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
                return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': f'Failed to add item to cart: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CartItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        try:
            cart, _ = Cart.objects.get_or_create(user=user)
            return cart
        except Exception as e:
            raise Exception(f"Error getting cart: {str(e)}")

    def get_item(self, cart, product_id):
        try:
            return CartItem.objects.get(cart=cart, product__id=product_id)
        except CartItem.DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Error getting cart item: {str(e)}")

    def put(self, request, product_id):
        try:
            serializer = AddCartItemSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            cart = self.get_cart(request.user)
            item = self.get_item(cart, product_id)

            if not item:
                return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

            quantity = serializer.validated_data['quantity']
            if quantity <= 0:
                return Response({'error': 'Quantity must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)

            item.quantity = quantity
            item.save()
            return Response(CartItemSerializer(item).data)

        except Exception as e:
            return Response(
                {'error': f'Failed to update item: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, product_id):
        try:
            cart = self.get_cart(request.user)
            item = self.get_item(cart, product_id)

            if not item:
                return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

            item.delete()
            return Response({'message': 'Item removed successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {'error': f'Failed to remove item: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
