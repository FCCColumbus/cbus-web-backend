from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth.models import User

class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        print("APIKeyAuthentication called")

        # Check Host header
        host = request.META.get('HTTP_HOST')
        if host not in settings.ALLOWED_HOSTS:
            raise exceptions.AuthenticationFailed('Invalid host')

        api_key = request.META.get('HTTP_X_API_KEY')
        print(f"Received API key: {api_key}")
        
        if not api_key:
            print("No API key provided")
            return None

        if api_key != settings.API_KEY:
            print(f"Invalid API key. Expected: {settings.API_KEY}, Received: {api_key}")
            raise exceptions.AuthenticationFailed('Invalid API key')

        print("Authentication successful")
        user, _ = User.objects.get_or_create(username='api_user')
        return (user, None)