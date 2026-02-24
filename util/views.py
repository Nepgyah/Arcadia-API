from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

@ensure_csrf_cookie
def ObtainCSRFToken(request):
    return JsonResponse({"detail":'CSRF token sent'})

class HealthCheckView(APIView):
    
    def get(self, request):
        return Response(status=200, data={"detail":'Testing GET successful'})
    
    def post(self, request):
        return Response(status=200, data={"detail":'Testing POST successful'})
    