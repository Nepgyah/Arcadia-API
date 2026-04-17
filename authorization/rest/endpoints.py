from main import settings

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import ArcadiaUser
from users.exceptions import UserNotFoundError

class AdminLoginView(APIView):

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if email is None:
            return Response(status=400, data={
                'detail': 'Missing email field'
            }) 
        
        if password is None:
            return Response(status=400, data={
                'detail': 'Missing password field'
            }) 
        
        try:
            target_user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                status=404,
                data={'detail': 'Invalid login credentials'}
            )
        
        admin_user = authenticate(username=target_user.username, password=password)

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
        access_expiry = timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        
        refresh_token = str(refresh)
        refresh_expiry = timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        
        response = Response(status=200, data={
            'detail':'Login Successful',
            'message': 'Login successful',
            'access_token': {
                'value': access_token,
                'expiry': access_expiry
            },
            'refresh_token': {
                'value': refresh_token,
                'expiry': refresh_expiry
            },
        })

        return response
    
class RefreshTokenView(APIView):
    
    def post(self, request):
        refresh_token = request.data.get('refresh_token', None)

        if refresh_token is None:
            return Response(status=400, data={
                'detail': 'Missing username field'
            }) 
        
        try:
            refreshed_data = RefreshToken(refresh_token)

            new_access_token = str(refreshed_data.access_token)
            access_expiry = timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

            new_refresh_token = str(refreshed_data)
            refresh_expiry = timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

            return Response(
                status=200,
                data={
                    'access_token': {
                        'value': new_access_token,
                        'expiry': access_expiry
                    },
                    'refresh_token': {
                        'value': new_refresh_token,
                        'expiry': refresh_expiry
                    },
                    'message': 'Tokens successfully refreshed'
                },
            )
        except Exception as e:
            return Response(status=400, data={'detail':'Error refreshing token'})