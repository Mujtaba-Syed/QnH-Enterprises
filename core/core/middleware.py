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
        if request.get_host().startswith('0.0.0.0'):
            path = request.path
            query_string = request.GET.urlencode()
            
            redirect_url = f"http://www.qhenterprises.com{path}"
            if query_string:
                redirect_url += f"?{query_string}"
            
            return HttpResponseRedirect(redirect_url)
        
        response = self.get_response(request)
        return response


class ProxyMiddleware:
    """
    Middleware to handle proxy headers for CSRF protection
    This ensures Django properly handles requests coming through a reverse proxy
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Handle proxy headers
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
        
        if 'HTTP_X_FORWARDED_PROTO' in request.META:
            request.META['wsgi.url_scheme'] = request.META['HTTP_X_FORWARDED_PROTO']
        
        if 'HTTP_X_FORWARDED_HOST' in request.META:
            request.META['HTTP_HOST'] = request.META['HTTP_X_FORWARDED_HOST']
        
        response = self.get_response(request)
        return response 