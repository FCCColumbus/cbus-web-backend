from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import MeetupIcalModel
from django.http import JsonResponse
from .utils.database_crud import rate_limited_auto_update
import logging

# TODO: maybe add allowed_origins in the future
# TODO: add logging
# setup logger
logger = logging.getLogger(__name__)

class MeetupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info("GET request received - User: %s, Auth: %s", 
            request.user, request.auth)

        
        if not request.user.is_authenticated:
            logger.warning("Authentication failed")
            return Response({"error": "Authentication failed"}, status=401)

        # updates database each time it is called but limited to 1 per hour. 
        rate_limited_auto_update()
        # returns all items from the database
        meetups = MeetupIcalModel.objects.all()
        meetup_data = list(meetups.values('meetupUUID', 'summary', 'description', 'start_time', 'end_time'))
        return JsonResponse({'meetups': meetup_data})