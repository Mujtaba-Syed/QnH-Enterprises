from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    UserProfileView,
    GoogleOAuthView,
    GoogleOAuthInitiateView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('google-oauth/', GoogleOAuthView.as_view(), name='google-oauth'),
    path('google-oauth-initiate/', GoogleOAuthInitiateView.as_view(), name='google-oauth-initiate'),
]