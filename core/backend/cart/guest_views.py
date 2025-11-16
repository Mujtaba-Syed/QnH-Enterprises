from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Cart, CartItem, GuestUser
from backend.products.models import Product
from .serializers import CartItemSerializer


class GuestRemoveFromCartView(APIView):
    """
    Remove specific item from guest cart
    """
    permission_classes = [AllowAny]
    
    def get_cart(self, guest_token):
        """Get cart for guest user"""
        try:
            guest_user = GuestUser.objects.get(guest_token=guest_token)
            if guest_user.is_expired():
                return None, "Guest session expired"
            
            cart, created = Cart.objects.get_or_create(guest_user=guest_user)
            return cart, None
        except GuestUser.DoesNotExist:
            return None, "Invalid guest token"
        except Exception as e:
            return None, f"Error getting cart: {str(e)}"

    def delete(self, request, product_id):
        """Remove specific item from guest cart"""
        try:
            guest_token = request.headers.get('X-Guest-Token')
            if not guest_token:
                return Response(
                    {'error': 'Guest token required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cart, error = self.get_cart(guest_token)
            if error:
                return Response(
                    {'error': error},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {'error': 'Product not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
                product_name = cart_item.product.name
                cart_item.delete()
                return Response({
                    'message': f'Successfully removed {product_name} from cart'
                }, status=status.HTTP_200_OK)
            except CartItem.DoesNotExist:
                return Response(
                    {'error': 'Item not found in cart'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            return Response(
                {'error': f'Failed to remove item from cart: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GuestDecreaseCartItemView(APIView):
    """
    Decrease quantity of specific item in guest cart by 1, remove if quantity becomes 0
    """
    permission_classes = [AllowAny]
    
    def get_cart(self, guest_token):
        """Get cart for guest user"""
        try:
            guest_user = GuestUser.objects.get(guest_token=guest_token)
            if guest_user.is_expired():
                return None, "Guest session expired"
            
            cart, created = Cart.objects.get_or_create(guest_user=guest_user)
            return cart, None
        except GuestUser.DoesNotExist:
            return None, "Invalid guest token"
        except Exception as e:
            return None, f"Error getting cart: {str(e)}"

    def put(self, request, product_id):
        """Decrease quantity of specific item in guest cart by 1"""
        try:
            guest_token = request.headers.get('X-Guest-Token')
            if not guest_token:
                return Response(
                    {'error': 'Guest token required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cart, error = self.get_cart(guest_token)
            if error:
                return Response(
                    {'error': error},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {'error': 'Product not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
                cart_item.quantity -= 1
                
                if cart_item.quantity <= 0:
                    cart_item.delete()
                    return Response({
                        'message': f'Removed {product.name} from cart (quantity reached 0)'
                    }, status=status.HTTP_200_OK)
                else:
                    cart_item.save()
                    return Response({
                        'message': f'Decreased quantity for {product.name}',
                        'item': CartItemSerializer(cart_item).data
                    }, status=status.HTTP_200_OK)
                    
            except CartItem.DoesNotExist:
                return Response(
                    {'error': 'Item not found in cart'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            return Response(
                {'error': f'Failed to decrease item: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
