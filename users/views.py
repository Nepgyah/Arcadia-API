import os
from main import settings
from dotenv import load_dotenv
from django.utils import timezone
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import ArcadiaUser
from users.serializers import UserSerializer

load_dotenv()

class UserView(APIView):

    def get(self, request):
        try:
            user = ArcadiaUser.objects.get(id=request.user.id)

            return Response(
                status=200,
                data={
                    'detail': 'User data successfully sent',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'picturePreset': user.picture_preset
                    }
                }
            )
        except ArcadiaUser.DoesNotExist:
            return None
        
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_data = UserSerializer(request.user).data
        return Response(
            status=200,
            data={
                'user', user_data
            }
        )