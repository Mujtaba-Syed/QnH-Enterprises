from django.urls import path
from .views import HomeView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    #path('get-all-reviews/', ReviewView.as_view(), name='get-reviews'),
]