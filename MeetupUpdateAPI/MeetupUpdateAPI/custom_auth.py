from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth.models import User

class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        if not api_key:
            return None

        if api_key != settings.API_KEY:
            raise exceptions.AuthenticationFailed('Invalid API key')

        # You might want to use a different user or create one specifically for API access
        user, _ = User.objects.get_or_create(username='api_user')
        return (user, None)