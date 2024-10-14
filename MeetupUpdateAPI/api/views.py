from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import MeetupIcalModel
from django.http import JsonResponse
from .utils.database_crud import rate_limited_auto_update

# TODO: maybe add allowed_origins in the future
class MeetupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("GET request received")
        print(f"User: {request.user}")
        print(f"Auth: {request.auth}")
        print(f"Headers: {request.META}")
        
        if not request.user.is_authenticated:
            return Response({"error": "Authentication failed"}, status=401)

        # updates database each time it is called but limited to 1 per hour. 
        rate_limited_auto_update()
        # returns all items from the database
        meetups = MeetupIcalModel.objects.all()
        meetup_data = list(meetups.values('meetupUUID', 'summary', 'description', 'start_time', 'end_time'))
        return JsonResponse({'meetups': meetup_data})