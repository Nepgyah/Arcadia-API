import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from graphene_django.utils.testing import graphql_query
from users.models import ArcadiaUser

@pytest.fixture
def arcadia_user_fixture():
    arcadia_user = ArcadiaUser.objects.create(
        d2x_id = 1,
        username = 'TestUser'
    )
    return arcadia_user

@pytest.fixture
def graphql_client(client):
    def func(query, variables=None, user=None):
        headers = {}
        if user:
            refresh_token = RefreshToken.for_user(user)
            headers['Authorization'] = f'Bearer {str(refresh_token.access_token)}'
                
        return graphql_query(
            query, 
            variables=variables, 
            client=client, 
            graphql_url='/graphql/',
            headers=headers
            )
    
    return func