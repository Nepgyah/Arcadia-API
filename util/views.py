import requests
import os
from main import settings

from django.utils import timezone
from django.middleware.csrf import get_token
from django.http import JsonResponse
from dotenv import load_dotenv

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from users.models import User

load_dotenv()

class ObtainD2XAuthorization(APIView):

    def post(self, request):
        auth_code = request.data.get('auth_code')

        try:
            d2x_response = requests.post(
                f"{os.environ.get("D2X_URL")}oauth/exchange/",
                data={
                    'auth_code': auth_code,
                    'client_id': 'arcadia-client',
                    'client_secret': os.environ.get("CLIENT_SECRET")
                },
                timeout=30
            )
            if (d2x_response.ok):
                data = d2x_response.json()
                d2x_id = data.get('d2x_id')
            else:
                return Response(
                    status=500,
                    data={'detail': f"D2X API: {d2x_response.json().get('detail')}"}
                )
        except ConnectionError:
            return Response(
                status=500,
                data={'detail':'Failure to connect to D2X API'}
            )
        except TimeoutError:
            return Response(
                status=500,
                data={'detail':'Connection to D2X API timed out'}
            )
        except Exception:
            return Response(
                status=500,
                data={'detail':'D2X API Error'}
            )
        try:
            user = User.objects.get(d2x_id=d2x_id)
        except User.DoesNotExist:
            user = User.objects.create(
                d2x_id=data.get('d2x_id'),
                username=data.get('d2x_username')
            )

        refresh = RefreshToken.for_user(user)

        refresh["username"] = user.username

        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        access_expiry = timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        access = {
            'key': 'access_token',
            'value': access_token,
            'httponly': True,
            'secure': bool(os.environ.get("COOKIE_SECURE")),
            'samesite': os.environ.get("COOKIE_SAME_SITE"),
            'expires': access_expiry,
            'path': '/',
        }

        refresh_expiry = timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        refresh = {
            'key': 'refresh_token',
            'value': refresh_token,
            'httponly': True,
            'secure': bool(os.environ.get("COOKIE_SECURE")),
            'samesite': os.environ.get("COOKIE_SAME_SITE"),
            'expires': refresh_expiry,
            'path': '/',
        }
        
        response = Response(status=200, data={
            'detail':'Token refreshed',
            'access_token': access,
            'refresh_token': refresh
        })

        return response
        # return response