
import os
import graphene
from main import settings
from dotenv import load_dotenv
from django.utils import timezone

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import ArcadiaUser
from authorization.graphql.schema import TokenType

load_dotenv()

class AdminLoginMutation(graphene.Mutation):
    refresh_token = graphene.Field(TokenType)
    access_token = graphene.Field(TokenType)

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    @classmethod
    def mutate(cls, _root, info, username = None, password = None):
        if username is None:
            raise Exception('Missing username')
        if password is None:
            raise Exception('Missing password')
        
        admin_user = authenticate(username=username, password=password)

        if admin_user is None:
            raise Exception('Admin user not found')
        
        try:
            arcadia_user = ArcadiaUser.objects.get(admin_user=admin_user)
        except ArcadiaUser.DoesNotExist:
            raise Exception('Arcadia user not found')
        
        refresh = RefreshToken.for_user(arcadia_user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        access_expiry = timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        access_data = {
            'key': 'access_token',
            'value': access_token,
            'httponly': True,
            'secure': bool(os.environ.get("COOKIE_SECURE")),
            'samesite': os.environ.get("COOKIE_SAME_SITE"),
            'expires': access_expiry,
            'path': '/',
        }

        refresh_expiry = timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        refresh_data = {
            'key': 'refresh_token',
            'value': refresh_token,
            'httponly': True,
            'secure': bool(os.environ.get("COOKIE_SECURE")),
            'samesite': os.environ.get("COOKIE_SAME_SITE"),
            'expires': refresh_expiry,
            'path': '/',
        }
        
        return AdminLoginMutation(
            access_token = access_data,
            refresh_token = refresh_data
        )
        
class Mutation(graphene.ObjectType):
    admin_login = AdminLoginMutation.Field()