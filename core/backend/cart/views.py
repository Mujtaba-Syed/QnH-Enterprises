from django.db import models
from django.contrib.auth.models import User
from backend.products.models import Product
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItem
from backend.products.models import Product
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer


class BaseCartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_cart(self, user, cart_id=None):
        try:
            if cart_id:
                return Cart.objects.get(user=user, id=cart_id)
            return Cart.objects.get(user=user, is_active=True)
        except Cart.DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Error getting cart: {str(e)}")
    
    def get_item(self, cart, product_id):
        try:
            return CartItem.objects.get(cart=cart, product__id=product_id)
        except CartItem.DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Error getting cart item: {str(e)}")


class UserCartListView(BaseCartView):
    def get(self, request):
        try:
            carts = Cart.objects.filter(user=request.user, is_deleted=False)
            serializer = CartSerializer(carts, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve user carts: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CartDetailView(BaseCartView):
    def get(self, request, cart_id=None):
        try:
            cart = self.get_cart(request.user, cart_id)
            if not cart:
                return Response(
                    {'error': 'Cart not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve cart: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, cart_id=None):
        try:
            cart = self.get_cart(request.user, cart_id)
            if not cart:
                return Response(
                    {'error': 'Cart not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Update cart status (active/inactive)
            is_active = request.data.get('is_active')
            if is_active is not None:
                cart.is_active = is_active
                cart.save()
            
            # Update completion status
            is_completed = request.data.get('is_completed')
            if is_completed is not None:
                cart.is_completed = is_completed
                cart.save()
            
            return Response(CartSerializer(cart).data)
        except Exception as e:
            return Response(
                {'error': f'Failed to update cart: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, cart_id=None):
        try:
            cart = self.get_cart(request.user, cart_id)
            if not cart:
                return Response(
                    {'error': 'Cart not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Soft delete (set is_deleted flag)
            cart.is_deleted = True
            cart.is_active = False
            cart.save()
            
            return Response(
                {'message': 'Cart deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to delete cart: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CartItemView(BaseCartView):
    def post(self, request):
        try:
            serializer = AddCartItemSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            cart = self.get_cart(request.user)
            if not cart:
                cart = Cart.objects.create(user=request.user)

            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

            item = self.get_item(cart, product_id)
            if item:
                item.quantity += quantity
                item.save()
                return Response(CartItemSerializer(item).data, status=status.HTTP_200_OK)
            else:
                item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
                return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': f'Failed to add item to cart: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CartItemDetailView(BaseCartView):
    def put(self, request, product_id):
        try:
            serializer = AddCartItemSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            cart = self.get_cart(request.user)
            if not cart:
                return Response({'error': 'Active cart not found'}, status=status.HTTP_404_NOT_FOUND)

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
            if not cart:
                return Response({'error': 'Active cart not found'}, status=status.HTTP_404_NOT_FOUND)

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


class CartClearView(BaseCartView):
    def delete(self, request):
        try:
            cart = self.get_cart(request.user)
            if not cart:
                return Response(
                    {'message': 'No active cart to clear'},
                    status=status.HTTP_204_NO_CONTENT
                )

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