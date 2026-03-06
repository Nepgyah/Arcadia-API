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

        response = Response(status=200, data={'detail' : "Authorization from d2x granted"})

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