from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import MeetupIcalModel
from django.http import JsonResponse
from django.conf import settings
from functools import wraps
from django.utils.decorators import method_decorator

def check_origin(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        origin = request.META.get('HTTP_ORIGIN')
        if origin not in settings.CORS_ALLOWED_ORIGINS:
            return JsonResponse({'error': 'Unauthorized origin'}, status=403)
        return view_func(request, *args, **kwargs)
    return wrapped_view
    
class MeetupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("GET request received")
        print(f"User: {request.user}")
        print(f"Auth: {request.auth}")
        print(f"Headers: {request.META}")
        
        if not request.user.is_authenticated:
            return Response({"error": "Authentication failed"}, status=401)

        meetups = MeetupIcalModel.objects.all()
        meetup_data = list(meetups.values('meetupUUID', 'summary', 'description', 'start_time', 'end_time'))
        return JsonResponse({'meetups': meetup_data})