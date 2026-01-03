from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)


def send_order_confirmation_email(order, customer_email, customer_name=None):
    """
    Send order confirmation email to customer
    
    Args:
        order: Order object
        customer_email: Customer email address
        customer_name: Optional customer name
    """
    try:
        if not customer_email:
            logger.error("Customer email is missing for order confirmation")
            return False

        subject = f"Order Confirmation - Order #{order.id if hasattr(order, 'id') else 'N/A'}"
        
        # Create a simple text email message
        message = f"""
Hello {customer_name or 'Customer'},

Thank you for your order!

Order Details:
- Order ID: {order.id if hasattr(order, 'id') else 'N/A'}
- Order Date: {order.created_at if hasattr(order, 'created_at') else 'N/A'}
- Total Amount: {order.total if hasattr(order, 'total') else 'N/A'}

We have received your order and will process it shortly. You will receive another email once your order has been shipped.

If you have any questions, please don't hesitate to contact us.

Best regards,
QnH Enterprises Team
        """

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[customer_email],
            reply_to=[settings.DEFAULT_FROM_EMAIL],
        )
        email.send()
        logger.info(f"Order confirmation email sent successfully to {customer_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send order confirmation email to {customer_email}: {str(e)}")
        return False


def send_order_status_update_email(order, customer_email, customer_name=None, status=None):
    """
    Send order status update email to customer
    
    Args:
        order: Order object
        customer_email: Customer email address
        customer_name: Optional customer name
        status: New order status
    """
    try:
        if not customer_email:
            logger.error("Customer email is missing for order status update")
            return False

        subject = f"Order Status Update - Order #{order.id if hasattr(order, 'id') else 'N/A'}"
        
        message = f"""
Hello {customer_name or 'Customer'},

Your order status has been updated!

Order Details:
- Order ID: {order.id if hasattr(order, 'id') else 'N/A'}
- New Status: {status or (order.status if hasattr(order, 'status') else 'N/A')}

We will keep you updated on your order progress.

If you have any questions, please don't hesitate to contact us.

Best regards,
QnH Enterprises Team
        """

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[customer_email],
            reply_to=[settings.DEFAULT_FROM_EMAIL],
        )
        email.send()
        logger.info(f"Order status update email sent successfully to {customer_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send order status update email to {customer_email}: {str(e)}")
        return False


def send_order_notification_to_admin(order, admin_email=None):
    """
    Send order notification email to admin
    
    Args:
        order: Order object
        admin_email: Admin email address (defaults to settings.ADMINS)
    """
    try:
        if not admin_email:
            # Get admin email from settings
            if hasattr(settings, 'ADMINS') and settings.ADMINS:
                admin_email = settings.ADMINS[0][1]
            else:
                logger.error("Admin email is not configured")
                return False

        subject = f"New Order Received - Order #{order.id if hasattr(order, 'id') else 'N/A'}"
        
        message = f"""
New Order Received!

Order Details:
- Order ID: {order.id if hasattr(order, 'id') else 'N/A'}
- Customer: {order.customer if hasattr(order, 'customer') else 'N/A'}
- Total Amount: {order.total if hasattr(order, 'total') else 'N/A'}
- Order Date: {order.created_at if hasattr(order, 'created_at') else 'N/A'}

Please process this order as soon as possible.

Best regards,
QnH Enterprises System
        """

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[admin_email],
            reply_to=[settings.DEFAULT_FROM_EMAIL],
        )
        email.send()
        logger.info(f"Order notification email sent successfully to admin: {admin_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send order notification email to admin: {str(e)}")
        return False


def send_order_shipped_email(order, customer_email, customer_name=None, tracking_number=None):
    """
    Send order shipped notification email to customer
    
    Args:
        order: Order object
        customer_email: Customer email address
        customer_name: Optional customer name
        tracking_number: Optional tracking number
    """
    try:
        if not customer_email:
            logger.error("Customer email is missing for order shipped notification")
            return False

        subject = f"Your Order Has Been Shipped - Order #{order.id if hasattr(order, 'id') else 'N/A'}"
        
        tracking_info = ""
        if tracking_number:
            tracking_info = f"\nTracking Number: {tracking_number}\n"
        
        message = f"""
Hello {customer_name or 'Customer'},

Great news! Your order has been shipped!

Order Details:
- Order ID: {order.id if hasattr(order, 'id') else 'N/A'}
{tracking_info}
Your order is on its way to you. You should receive it soon.

If you have any questions, please don't hesitate to contact us.

Best regards,
QnH Enterprises Team
        """

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[customer_email],
            reply_to=[settings.DEFAULT_FROM_EMAIL],
        )
        email.send()
        logger.info(f"Order shipped email sent successfully to {customer_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send order shipped email to {customer_email}: {str(e)}")
        return False

