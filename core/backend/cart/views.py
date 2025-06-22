from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItem
from backend.products.models import Product
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer


class CartView(APIView):
    """
    Get user's cart
    """
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        """Get or create cart for user"""
        try:
            cart, created = Cart.objects.get_or_create(user=user)
            return cart
        except Exception as e:
            raise Exception(f"Error getting cart: {str(e)}")

    def get(self, request):
        """Get user's cart with all items"""
        try:
            cart = self.get_cart(request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve cart: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ClearCartView(APIView):
    """
    Clear all items from cart
    """
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        """Get cart for user"""
        try:
            cart = Cart.objects.get(user=user)
            return cart
        except Cart.DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Error getting cart: {str(e)}")

    def delete(self, request):
        """Clear all items from cart"""
        try:
            cart = self.get_cart(request.user)
            if not cart:
                return Response(
                    {'message': 'Cart does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            deleted_count, _ = cart.items.all().delete()
            if deleted_count == 0:
                return Response(
                    {'message': 'Cart was already empty'},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'message': f'Successfully cleared {deleted_count} items from cart'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to clear cart: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AddToCartView(APIView):
    """
    Add item to cart (create if not exists, update if exists)
    """
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        """Get or create cart for user"""
        try:
            cart, created = Cart.objects.get_or_create(user=user)
            return cart
        except Exception as e:
            raise Exception(f"Error getting cart: {str(e)}")

    def post(self, request):
        """Add item to cart"""
        try:
            serializer = AddCartItemSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            cart = self.get_cart(request.user)
            product_id = serializer.validated_data['product_id']
            quantity = 1

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {'error': 'Product not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
                cart_item.quantity += quantity
                cart_item.save()
                message = f'Updated quantity for {product.name}'
                status_code = status.HTTP_200_OK
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(
                    cart=cart, 
                    product=product, 
                    quantity=quantity
                )
                message = f'Added {product.name} to cart'
                status_code = status.HTTP_201_CREATED

            return Response({
                'message': message,
                'item': CartItemSerializer(cart_item).data
            }, status=status_code)

        except Exception as e:
            return Response(
                {'error': f'Failed to add item to cart: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RemoveFromCartView(APIView):
    """
    Remove specific item from cart
    """
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        """Get cart for user"""
        try:
            cart = Cart.objects.get(user=user)
            return cart
        except Cart.DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Error getting cart: {str(e)}")

    def delete(self, request, product_id):
        """Remove specific item from cart"""
        try:
            cart = self.get_cart(request.user)
            if not cart:
                return Response(
                    {'error': 'Cart does not exist'}, 
                    status=status.HTTP_404_NOT_FOUND
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


class UpdateCartItemView(APIView):
    """
    Increment quantity of specific item in cart by 1
    """
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        """Get cart for user"""
        try:
            cart = Cart.objects.get(user=user)
            return cart
        except Cart.DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Error getting cart: {str(e)}")

    def put(self, request, product_id):
        """Increment quantity of specific item in cart by 1"""
        try:
            cart = self.get_cart(request.user)
            if not cart:
                return Response(
                    {'error': 'Cart does not exist'}, 
                    status=status.HTTP_404_NOT_FOUND
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
                cart_item.quantity += 1
                cart_item.save()
                return Response({
                    'message': f'Updated quantity for {product.name}',
                    'item': CartItemSerializer(cart_item).data
                }, status=status.HTTP_200_OK)
            except CartItem.DoesNotExist:
                return Response(
                    {'error': 'Item not found in cart'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            return Response(
                {'error': f'Failed to update item: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DecreaseCartItemView(APIView):
    """
    Decrease quantity of specific item in cart by 1, remove if quantity becomes 0
    """
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        """Get cart for user"""
        try:
            cart = Cart.objects.get(user=user)
            return cart
        except Cart.DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Error getting cart: {str(e)}")

    def put(self, request, product_id):
        """Decrease quantity of specific item in cart by 1"""
        try:
            cart = self.get_cart(request.user)
            if not cart:
                return Response(
                    {'error': 'Cart does not exist'}, 
                    status=status.HTTP_404_NOT_FOUND
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


class DeleteCartView(APIView):
    """
    Delete complete cart (cart and all items)
    """
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        """Get cart for user"""
        try:
            cart = Cart.objects.get(user=user)
            return cart
        except Cart.DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Error getting cart: {str(e)}")

    def delete(self, request):
        """Delete complete cart"""
        try:
            cart = self.get_cart(request.user)
            if not cart:
                return Response(
                    {'message': 'Cart does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            cart.delete()
            return Response(
                {'message': 'Cart deleted successfully'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to delete cart: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
