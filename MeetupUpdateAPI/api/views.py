from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
from .models import MeetupIcalModel
from django.views.decorators.http import require_GET
from django.conf import settings

def check_origin(view_func):
    def wrapped_view(request, *args, **kwargs):
        # Check API Key
        if request.GET.get('api_key') != settings.SECRET_KEY:
            return JsonResponse({'error': 'Invalid API key'}, status=403)

        # Check Referer
        referer = request.META.get('HTTP_REFERER', '')
        if not referer.startswith(settings.ALLOWED_ORIGIN):
            return JsonResponse({'error': 'Unauthorized origin'}, status=403)

        return view_func(request, *args, **kwargs)
    return wrapped_view


class MeetupView(View):
    @method_decorator(require_GET)
    @method_decorator(check_origin)
    def get(self, request):
        # Your logic for GET requests
        meetups = MeetupIcalModel.objects.all()
        meetup_data = list(meetups.values('uid', 'summary', 'description', 'start_time', 'end_time'))
        return JsonResponse({'meetups': meetup_data})

    @method_decorator(check_origin)
    def post(self, request):
        # Your logic for POST requests
        return JsonResponse({"message": "POST request received"})