from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import os
from dotenv import load_dotenv

from users.models import User
load_dotenv()

@ensure_csrf_cookie
def ObtainCSRFToken(request):
    return JsonResponse({"detail":'CSRF token sent'})

class HealthCheckView(APIView):
    
    def get(self, request):
        return Response(status=200, data={"detail":'Testing GET successful'})
    
    def post(self, request):
        return Response(status=200, data={"detail":'Testing POST successful'})
    
class ObtainD2XAuthorization(APIView):

    def post(self, request):
        auth_code = request.data.get('auth_code')

        print('Calling D2X API for exchange')
        d2x_response = requests.post(
            f"{os.environ.get("D2X_URL")}oauth/exchange/",
            data={
                'auth_code': auth_code,
                'client_id': 'arcadia-client',
                'client_secret': os.environ.get("CLIENT_SECRET")
            }
        )
        data = d2x_response.json()

        user = User.objects.create(
            d2x_id=data.get('d2x_id'),
            username=data.get('d2x_username')
        )

        print('Creating tokens for arcadia user')
        refresh = RefreshToken.for_user(user)

        refresh["username"] = user.username

        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response(status=200, data={'detail' : "Authorization from d2x granted"})

        print('Setting cookie')
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=bool(os.environ.get("COOKIE_SECURE")),
            samesite=os.environ.get("COOKIE_SAME_SITE"),
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=bool(os.environ.get("COOKIE_SECURE")),
            samesite=os.environ.get("COOKIE_SAME_SITE"),
        )

        return response