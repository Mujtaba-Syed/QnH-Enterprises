from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.
class HomeView(View):
    def get(self, request):
        return HttpResponse("Welcome to the Home Page")
    
    
# make a list view, a get request to get all reviews make its serializer