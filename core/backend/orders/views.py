from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .email_helpers import (
    send_order_confirmation_email,
    send_order_status_update_email,
    send_order_notification_to_admin,
    send_order_shipped_email
)
import logging

logger = logging.getLogger(__name__)


class TestEmailView(APIView):
    """
    Test endpoint to verify email configuration
    Only available when DEBUG=True for security
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Test Email Configuration",
        description="Send a test email to verify email configuration. Only available in DEBUG mode.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'email': {
                        'type': 'string',
                        'format': 'email',
                        'description': 'Email address to send test email to',
                        'example': 'test@example.com'
                    }
                },
                'required': ['email']
            }
        },
        responses={
            200: {
                'description': 'Test email sent successfully',
                'content': {
                    'application/json': {
                        'example': {
                            'success': True,
                            'message': 'Test email sent successfully to test@example.com',
                            'email_settings': {
                                'backend': 'django.core.mail.backends.smtp.EmailBackend',
                                'host': 'smtp.hostinger.com',
                                'port': 587,
                                'from_email': 'noreply@qhenterprises.com',
                                'use_tls': True,
                                'use_ssl': False
                            }
                        }
                    }
                }
            },
            403: {
                'description': 'Email testing is only available in DEBUG mode',
                'content': {
                    'application/json': {
                        'example': {
                            'error': 'Email testing is only available in DEBUG mode'
                        }
                    }
                }
            },
            500: {
                'description': 'Failed to send test email',
                'content': {
                    'application/json': {
                        'example': {
                            'success': False,
                            'error': 'Error message',
                            'message': 'Failed to send test email. Check your email configuration and logs.'
                        }
                    }
                }
            }
        },
        tags=['Email Testing']
    )
    def post(self, request):
        """
        Test email sending with a simple email
        POST data: {"email": "test@example.com"}
        """
        if not settings.DEBUG:
            return Response(
                {'error': 'Email testing is only available in DEBUG mode'},
                status=status.HTTP_403_FORBIDDEN
            )

        test_email = request.data.get('email', 'test@example.com')
        
        try:
            # Test basic email sending
            subject = "Test Email from QnH Enterprises"
            message = """
This is a test email from your QnH Enterprises application.

If you received this email, your email configuration is working correctly!

Email Settings:
- Backend: {backend}
- Host: {host}
- Port: {port}
- From: {from_email}
            """.format(
                backend=settings.EMAIL_BACKEND,
                host=getattr(settings, 'EMAIL_HOST', 'N/A'),
                port=getattr(settings, 'EMAIL_PORT', 'N/A'),
                from_email=settings.DEFAULT_FROM_EMAIL
            )

            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[test_email],
            )
            email.send()

            return Response({
                'success': True,
                'message': f'Test email sent successfully to {test_email}',
                'email_settings': {
                    'backend': settings.EMAIL_BACKEND,
                    'host': getattr(settings, 'EMAIL_HOST', 'N/A'),
                    'port': getattr(settings, 'EMAIL_PORT', 'N/A'),
                    'from_email': settings.DEFAULT_FROM_EMAIL,
                    'use_tls': getattr(settings, 'EMAIL_USE_TLS', False),
                    'use_ssl': getattr(settings, 'EMAIL_USE_SSL', False),
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Failed to send test email: {str(e)}")
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Failed to send test email. Check your email configuration and logs.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestOrderEmailView(APIView):
    """
    Test endpoint to verify order email functions
    Only available when DEBUG=True for security
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Test Order Email Functions",
        description="Test various order-related email functions. Only available in DEBUG mode.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'email': {
                        'type': 'string',
                        'format': 'email',
                        'description': 'Customer email address',
                        'example': 'customer@example.com'
                    },
                    'name': {
                        'type': 'string',
                        'description': 'Customer name',
                        'example': 'John Doe'
                    },
                    'type': {
                        'type': 'string',
                        'enum': ['confirmation', 'status', 'admin', 'shipped', 'all'],
                        'description': 'Type of email to test',
                        'example': 'confirmation'
                    },
                    'admin_email': {
                        'type': 'string',
                        'format': 'email',
                        'description': 'Admin email for admin notification test',
                        'example': 'admin@example.com'
                    }
                },
                'required': ['email']
            }
        },
        responses={
            200: {
                'description': 'Order email tests completed',
                'content': {
                    'application/json': {
                        'example': {
                            'success': True,
                            'message': 'Order email tests completed',
                            'results': {
                                'confirmation': True,
                                'status': True,
                                'admin': True,
                                'shipped': True
                            },
                            'email_type': 'all'
                        }
                    }
                }
            },
            403: {
                'description': 'Email testing is only available in DEBUG mode',
                'content': {
                    'application/json': {
                        'example': {
                            'error': 'Email testing is only available in DEBUG mode'
                        }
                    }
                }
            },
            500: {
                'description': 'Failed to send test order emails',
                'content': {
                    'application/json': {
                        'example': {
                            'success': False,
                            'error': 'Error message',
                            'message': 'Failed to send test order emails. Check your email configuration and logs.'
                        }
                    }
                }
            }
        },
        tags=['Email Testing']
    )
    def post(self, request):
        """
        Test order email functions
        POST data: {
            "email": "test@example.com",
            "name": "Test Customer",
            "type": "confirmation" | "status" | "admin" | "shipped"
        }
        """
        if not settings.DEBUG:
            return Response(
                {'error': 'Email testing is only available in DEBUG mode'},
                status=status.HTTP_403_FORBIDDEN
            )

        test_email = request.data.get('email', 'test@example.com')
        test_name = request.data.get('name', 'Test Customer')
        email_type = request.data.get('type', 'confirmation')

        # Create a mock order object
        class MockOrder:
            def __init__(self):
                self.id = 12345
                self.created_at = '2024-01-01 12:00:00'
                self.total = 999.99
                self.status = 'Processing'
                self.customer = test_name

        mock_order = MockOrder()
        results = {}

        try:
            if email_type == 'confirmation' or email_type == 'all':
                results['confirmation'] = send_order_confirmation_email(
                    mock_order, test_email, test_name
                )

            if email_type == 'status' or email_type == 'all':
                results['status'] = send_order_status_update_email(
                    mock_order, test_email, test_name, 'Shipped'
                )

            if email_type == 'admin' or email_type == 'all':
                admin_email = request.data.get('admin_email', None)
                results['admin'] = send_order_notification_to_admin(
                    mock_order, admin_email
                )

            if email_type == 'shipped' or email_type == 'all':
                results['shipped'] = send_order_shipped_email(
                    mock_order, test_email, test_name, 'TRACK123456'
                )

            return Response({
                'success': True,
                'message': f'Order email tests completed',
                'results': results,
                'email_type': email_type
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Failed to send test order emails: {str(e)}")
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Failed to send test order emails. Check your email configuration and logs.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
