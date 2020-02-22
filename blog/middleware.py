from .models import Post 
from django.utils.deprecation import MiddlewareMixin

class BlogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("Middleware executed")
        
