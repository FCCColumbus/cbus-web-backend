from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth.models import User
import logging


logger = logging.getLogger(__name__)

class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

# TODO: add when production url is ready
        # # Check Host header
        # host = request.META.get('HTTP_HOST')
        # if host not in settings.ALLOWED_HOSTS:
        #     logger.warning(f"Invalid host: {host}")
        #     raise exceptions.AuthenticationFailed('Invalid host')

        api_key = request.META.get('HTTP_X_API_KEY')
        logger.info(f"API key: {api_key} is authentic") 
        if not api_key:
            logger.warning(f"API key not provided from {request.META.get('REMOTE_ADDR')}")
            return None
        if api_key != settings.API_KEY:
            logger.warning(
                "Invalid API key attempt - Host: %s, Path: %s, Method: %s, IP: %s",
                request.get_host(),
                request.path,
                request.method,
                request.META.get('REMOTE_ADDR')
            )
            raise exceptions.AuthenticationFailed('Invalid API key')


        logger.info(f"{request.get_host()}'s authentication successful")
        user, _ = User.objects.get_or_create(username='api_user')
        return (user, None)