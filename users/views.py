import os
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from dotenv import load_dotenv

from users.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny

load_dotenv()

class DemoLoginView(APIView):
    """
    Temp view: Simulates login and use of jwt token for auth
    """

    def post(self, request):
        user = User.objects.first()

        refresh = RefreshToken.for_user(user)

        refresh["arcadia_id"] = user.id
        refresh["username"] = "Demo Arcadia"
        refresh["provider"] = "local_dev"

        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({"detail": "Login successful"})

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
    
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            data= { 
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'picturePreset': 1
                }
            }, status=200)
    
class UpdateUser(APIView):
    permission_classes = [AllowAny]

    def post (self, request, id):
        try:
            arcadia_user = User.objects.get(d2x_id=id)
            arcadia_user.username = request.data.get('username')
            arcadia_user.save()
            return Response(status=200, data={'detail':'Arcadia username updated'})
        except User.DoesNotExist:
            return Response(status=400, data={'detail':'Invalid user id.'})