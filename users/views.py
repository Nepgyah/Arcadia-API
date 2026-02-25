from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from users.models import User
from rest_framework.permissions import IsAuthenticated
class DemoLoginView(APIView):
    """
    Temp view: Simulates login and use of jwt token for auth
    """

    def post(self, request):
        print('Demo API called')
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
            secure=False,  # True in production
            samesite="Lax"
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="Lax"
        )

        return response
    
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            data= { 
                'user': {
                    'id': request.user.id,
                    'username': 'Arcadia Demo',
                    'picturePreset': 1
                }
            }, status=200)