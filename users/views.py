import os
from main import settings
from dotenv import load_dotenv
from django.utils import timezone
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import ArcadiaUser

load_dotenv()

class AdminLoginView(APIView):

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username is None:
            return Response(status=400, data={
                'detail': 'Missing username field'
            }) 
        
        if password is None:
            return Response(status=400, data={
                'detail': 'Missing password field'
            }) 
        
        admin_user = authenticate(username=username, password=password)

        if admin_user is None:
            return Response(status=400, data={
                'detail': 'Invalid login credentials'
            }) 
        
        try:
            arcadia_user = ArcadiaUser.objects.get(admin_user=admin_user)
        except ArcadiaUser.DoesNotExist:
            return Response(
                status=404,
                data={'detail': 'Admin test user not found'}
            )


        refresh = RefreshToken.for_user(arcadia_user)
        refresh['username'] = arcadia_user.username
        
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
