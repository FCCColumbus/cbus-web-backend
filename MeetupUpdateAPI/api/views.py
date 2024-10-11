from django.utils.decorators import method_decorator
from django.http import JsonResponse
# from django.views import View
from .models import MeetupIcalModel
from django.views.decorators.http import require_GET
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


def check_origin(view_func):
    print("check_origin decorator called")
    def wrapped_view(request, *args, **kwargs):
    #     # Check Referer
    #     referer = request.META.get('HTTP_REFERER', '')
    #     if not referer:
    # # Handle the case where the referrer is not present
    #         return JsonResponse({'error': 'Referrer header missing'}, status=403)
    #     if referer not in settings.ALLOWED_ORIGIN:
    #         return JsonResponse({'error': 'Unauthorized origin'}, status=403)

        return view_func(request, *args, **kwargs)
    return wrapped_view


class MeetupView(APIView):
    # @method_decorator(require_GET)
    # @method_decorator(check_origin)
    def get(self, request):
        # Your logic for GET requests
        print("GET request received")
        print(f"User: {request.user}")
        print(f"Auth: {request.auth}")
        
        if not request.user.is_authenticated:
            return Response({"error": "Authentication failed"}, status=401)

        meetups = MeetupIcalModel.objects.all()
        meetup_data = list(meetups.values('meetupUUID', 'summary', 'description', 'start_time', 'end_time'))
        return JsonResponse({'meetups': meetup_data})