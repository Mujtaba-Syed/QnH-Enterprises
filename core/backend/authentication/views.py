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
from django.shortcuts import redirect
from django.conf import settings
from social_django.models import UserSocialAuth
from social_core.exceptions import AuthForbidden, AuthTokenError
import requests
import json

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

class GoogleOAuthView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Handle Google OAuth callback and return JWT tokens"""
        try:
            # Get the authorization code from the request
            code = request.GET.get('code')
            if not code:
                return Response({'detail': 'Authorization code not provided'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Exchange code for access token
            token_url = 'https://oauth2.googleapis.com/token'
            token_data = {
                'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': f"{settings.BASE_URL}/accounts/google-oauth/"
            }
            
            token_response = requests.post(token_url, data=token_data)
            if not token_response.ok:
                return Response({'detail': 'Failed to exchange code for token'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            token_info = token_response.json()
            access_token = token_info.get('access_token')
            
            # Get user info from Google
            user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
            headers = {'Authorization': f'Bearer {access_token}'}
            user_response = requests.get(user_info_url, headers=headers)
            
            if not user_response.ok:
                return Response({'detail': 'Failed to get user info from Google'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            user_info = user_response.json()
            email = user_info.get('email')
            first_name = user_info.get('given_name', '')
            last_name = user_info.get('family_name', '')
            google_id = user_info.get('id')
            
            if not email:
                return Response({'detail': 'Email not provided by Google'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Check if user exists, if not create one
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create new user
                username = email.split('@')[0]  # Use email prefix as username
                # Ensure username is unique
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=None  # No password for OAuth users
                )
                
                # Create social auth association
                UserSocialAuth.objects.create(
                    user=user,
                    provider='google-oauth2',
                    uid=google_id,
                    extra_data=user_info
                )
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            # Redirect to a page that will handle the tokens
            from django.shortcuts import redirect
            from urllib.parse import urlencode
            
            # Create a redirect URL with tokens as query parameters
            tokens_data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
            
            redirect_url = f"{settings.BASE_URL}/oauth-success/?{urlencode(tokens_data)}"
            return redirect(redirect_url)
            
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GoogleOAuthInitiateView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Redirect to Google OAuth authorization URL"""
        google_auth_url = 'https://accounts.google.com/o/oauth2/v2/auth'
        
        # Use the redirect URI from settings
        redirect_uri = f"{settings.BASE_URL}/accounts/google-oauth/"

        
        params = {
            'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': ' '.join(settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE),
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        auth_url = f"{google_auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        return Response({'auth_url': auth_url}, status=status.HTTP_200_OK)
