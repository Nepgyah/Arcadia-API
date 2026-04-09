from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import ArcadiaUser

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
        
        response = Response(status=200, data={
            'detail':'Login Successful',
            'access_token': access_token,
            'refresh_token': refresh_token
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
            new_refresh_token = str(refreshed_data)

            return Response(
                status=200,
                data={
                    'access_token': new_access_token,
                    'refresh_token': new_refresh_token,
                    'message': 'Tokens successfully refreshed'
                },
            )
        except Exception as e:
            return Response(status=400, data={'detail':'Error refreshing token'})