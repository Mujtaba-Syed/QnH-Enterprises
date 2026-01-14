from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal
from backend.products.models import Product

User = get_user_model()


class Order(models.Model):
    """Model to track customer orders with billing and payment information."""
    
    # Payment Status Choices
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('due', 'Due'),
        ('partial', 'Partially Paid'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ]
    
    # Order Status Choices
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('booked', 'Booked'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]
    
    # Payment Method Choices
    PAYMENT_METHOD_CHOICES = [
        ('jazzcash', 'Jazzcash'),
        ('bank_transfer', 'Bank Transfer'),
        ('whatsapp', 'WhatsApp'),
        ('cash_on_delivery', 'Cash on Delivery'),
        ('other', 'Other'),
    ]
    
    # Order Information
    order_number = models.CharField(max_length=50, unique=True, editable=False, help_text="Unique order identifier")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', help_text="User who placed the order (if logged in)")
    
    # Customer Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=20)
    
    # Billing Address
    address = models.TextField(help_text="House Number and Street Name")
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Pakistan')
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    
    # Shipping Address (if different)
    ship_to_different_address = models.BooleanField(default=False)
    shipping_address = models.TextField(blank=True, null=True)
    shipping_city = models.CharField(max_length=100, blank=True, null=True)
    shipping_country = models.CharField(max_length=100, blank=True, null=True)
    shipping_zipcode = models.CharField(max_length=20, blank=True, null=True)
    
    # Order Details
    order_notes = models.TextField(blank=True, null=True, help_text="Additional notes from customer")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], help_text="Total order amount")
    
    # Payment Information
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='whatsapp')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_transaction_id = models.CharField(max_length=200, blank=True, null=True, help_text="Transaction ID from payment gateway")
    payment_receipt = models.FileField(upload_to='payment_receipts/', blank=True, null=True, help_text="Payment receipt image/document")
    payment_date = models.DateTimeField(blank=True, null=True, help_text="Date when payment was received")
    
    # Order Status and Tracking
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    tracking_number = models.CharField(max_length=100, blank=True, null=True, unique=True, help_text="Shipping/tracking number")
    tracking_url = models.URLField(blank=True, null=True, help_text="URL to track the order")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(blank=True, null=True, help_text="When order was confirmed")
    shipped_at = models.DateTimeField(blank=True, null=True, help_text="When order was shipped")
    delivered_at = models.DateTimeField(blank=True, null=True, help_text="When order was delivered")
    
    # Additional Fields
    is_guest_order = models.BooleanField(default=False, help_text="True if order was placed without login")
    admin_notes = models.TextField(blank=True, null=True, help_text="Internal notes for admin use")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['order_status']),
            models.Index(fields=['payment_status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        """Generate unique order number if not provided."""
        if not self.order_number:
            # Generate order number: ORD-YYYYMMDD-HHMMSS-XXXX
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            # Get last order number to increment
            last_order = Order.objects.order_by('-id').first()
            if last_order and last_order.id:
                sequence = str(last_order.id + 1).zfill(4)
            else:
                sequence = '0001'
            self.order_number = f"ORD-{timestamp}-{sequence}"
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        """Return customer's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def get_total_items(self):
        """Return total number of items in the order."""
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0
    
    @property
    def is_paid(self):
        """Check if order is fully paid."""
        return self.payment_status == 'paid'
    
    @property
    def is_delivered(self):
        """Check if order is delivered."""
        return self.order_status == 'delivered'


class OrderItem(models.Model):
    """Model to track individual products in an order."""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_items')
    product_name = models.CharField(max_length=255, help_text="Product name at time of order (snapshot)")
    product_sku = models.CharField(max_length=100, blank=True, null=True, help_text="Product SKU at time of order")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], help_text="Price per unit at time of order")
    discount_percentage = models.PositiveIntegerField(default=0, help_text="Discount percentage applied at time of order")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], help_text="Subtotal for this item (quantity * price after discount)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        indexes = [
            models.Index(fields=['order', 'product']),
        ]
    
    def __str__(self):
        return f"{self.product_name} x{self.quantity} - Order #{self.order.order_number}"
    
    def save(self, *args, **kwargs):
        """Calculate subtotal before saving."""
        # Calculate price after discount
        if self.discount_percentage > 0:
            discount_amount = (self.price * self.discount_percentage) / 100
            discounted_price = self.price - discount_amount
        else:
            discounted_price = self.price
        
        # Calculate subtotal
        self.subtotal = discounted_price * self.quantity
        
        # Update product name and SKU if product exists
        if self.product:
            if not self.product_name:
                self.product_name = self.product.name
            if not self.product_sku:
                self.product_sku = self.product.sku
        
        super().save(*args, **kwargs)
    
    @property
    def unit_price_after_discount(self):
        """Return unit price after discount."""
        if self.discount_percentage > 0:
            discount_amount = (self.price * self.discount_percentage) / 100
            return self.price - discount_amount
        return self.price
