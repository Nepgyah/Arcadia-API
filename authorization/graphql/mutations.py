
import os
import graphene
from main import settings
from dotenv import load_dotenv
from django.utils import timezone

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import ArcadiaUser
from authorization.graphql.schema import TokenType
from authorization.exceptions import AuthorizationError

load_dotenv()

class AdminLoginMutation(graphene.Mutation):
    refresh_token = graphene.String()
    access_token = graphene.String()

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
            raise AuthorizationError('Invalid credentials', code='auth_error_invalid_credentials')
        
        try:
            arcadia_user = ArcadiaUser.objects.get(admin_user=admin_user)
        except ArcadiaUser.DoesNotExist:
            raise Exception('Arcadia user not found')
        
        refresh = RefreshToken.for_user(arcadia_user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        return AdminLoginMutation(
            access_token = access_token,
            refresh_token = refresh_token
        )
        
class Mutation(graphene.ObjectType):
    admin_login = AdminLoginMutation.Field()