from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderReadSerializer
from backend.products.models import Product
from decimal import Decimal

User = get_user_model()


class CreateOrderAPIView(APIView):
    """
    API endpoint to create a new order.
    Sets order_status to 'pending' and payment_status to 'pending' by default.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Create a new order with order items.
        
        Expected payload:
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "mobile": "03001234567",
            "address": "123 Main St",
            "city": "Lahore",
            "country": "Pakistan",
            "zipcode": "54000",
            "ship_to_different_address": false,
            "order_notes": "Please handle with care",
            "payment_method": "whatsapp",
            "items": [
                {
                    "product_id": 1,
                    "quantity": 2
                },
                {
                    "product_id": 2,
                    "quantity": 1
                }
            ]
        }
        """
        try:
            serializer = CreateOrderSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            validated_data = serializer.validated_data
            items_data = validated_data.pop('items')
            
            # Calculate total amount
            total_amount = Decimal('0.00')
            order_items_data = []
            
            for item_data in items_data:
                product_id = item_data['product_id']
                quantity = item_data['quantity']
                
                try:
                    product = Product.objects.get(id=product_id, is_active=True)
                except Product.DoesNotExist:
                    return Response(
                        {'error': f'Product with ID {product_id} does not exist or is not active.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Get price and discount
                price = product.price
                discount_percentage = product.discount_percentage
                
                # Calculate price after discount
                if discount_percentage > 0:
                    discount_amount = (price * Decimal(discount_percentage)) / Decimal('100')
                    item_price = price - discount_amount
                else:
                    item_price = price
                
                # Calculate subtotal for this item
                item_subtotal = item_price * quantity
                total_amount += item_subtotal
                
                # Store item data for later creation
                order_items_data.append({
                    'product': product,
                    'product_name': product.name,
                    'product_sku': product.sku,
                    'quantity': quantity,
                    'price': price,
                    'discount_percentage': discount_percentage,
                    'subtotal': item_subtotal
                })
            
            # Get user if authenticated
            user = None
            if request.user.is_authenticated:
                user = request.user
            
            # Determine if guest order
            is_guest_order = user is None
            
            # Create order
            order = Order.objects.create(
                user=user,
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data.get('email', ''),
                mobile=validated_data['mobile'],
                address=validated_data['address'],
                city=validated_data['city'],
                country=validated_data.get('country', 'Pakistan'),
                zipcode=validated_data.get('zipcode', ''),
                ship_to_different_address=validated_data.get('ship_to_different_address', False),
                shipping_address=validated_data.get('shipping_address', ''),
                shipping_city=validated_data.get('shipping_city', ''),
                shipping_country=validated_data.get('shipping_country', ''),
                shipping_zipcode=validated_data.get('shipping_zipcode', ''),
                order_notes=validated_data.get('order_notes', ''),
                total_amount=total_amount,
                payment_method=validated_data.get('payment_method', 'whatsapp'),
                payment_status='pending',  # Set to pending by default
                order_status='pending',  # Set to pending by default
                is_guest_order=is_guest_order
            )
            
            # Create order items
            for item_data in order_items_data:
                OrderItem.objects.create(
                    order=order,
                    product=item_data['product'],
                    product_name=item_data['product_name'],
                    product_sku=item_data['product_sku'],
                    quantity=item_data['quantity'],
                    price=item_data['price'],
                    discount_percentage=item_data['discount_percentage'],
                    subtotal=item_data['subtotal']
                )
            
            # Serialize and return the created order
            order_serializer = OrderReadSerializer(order)
            
            return Response(
                {
                    'message': 'Order created successfully',
                    'order': order_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {'error': f'Failed to create order: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
