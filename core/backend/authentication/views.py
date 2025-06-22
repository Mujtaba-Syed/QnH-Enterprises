from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .token import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .serializers import (
    UserRegistrationSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    UserProfileSerializer
)
from .email_helpers import send_verification_email

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'phone': user.phone
                    },
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                user = authenticate(
                    username=validated_data['username'],
                    password=validated_data['password']
                )
                if user:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_200_OK)
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            logout(request)
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = PasswordResetSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                email = validated_data['email']
                try:
                    user = User.objects.get(email=email)
                    send_verification_email(user, email)
                    return Response({'detail': 'Password reset link sent to your email.'}, 
                                    status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({'detail': 'User with this email does not exist.'},
                                  status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if not account_activation_token.check_token(user, token):
                return Response({'detail': 'Invalid or expired token.'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            serializer = PasswordResetConfirmSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                user.set_password(validated_data['new_password'])
                user.save()
                return Response({'detail': 'Password has been reset successfully.'},
                              status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        try:
            serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
