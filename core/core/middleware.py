from django.http import HttpResponseRedirect
from django.conf import settings


class ZeroZeroRedirectMiddleware:
    """
    Middleware that automatically redirects requests from 0.0.0.0 to localhost
    This allows users to click on the terminal URL and get redirected to the correct address
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is coming from 0.0.0.0
        if request.get_host().startswith('0.0.0.0'):
            # Get the current path and query parameters
            path = request.path
            query_string = request.GET.urlencode()
            
            # Build the redirect URL with localhost
            redirect_url = f"http://localhost:8000{path}"
            if query_string:
                redirect_url += f"?{query_string}"
            
            return HttpResponseRedirect(redirect_url)
        
        # If not 0.0.0.0, continue with normal processing
        response = self.get_response(request)
        return response 