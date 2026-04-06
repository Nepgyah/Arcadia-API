import pytest
from graphene_django.utils.testing import graphql_query
from users.models import ArcadiaUser

@pytest.fixture
def graphql_client(client):
    def func(query, variables=None):
        return graphql_query(query, variables=variables, client=client, graphql_url='/graphql/')
    return func

@pytest.fixture
def arcadia_user_fixture():
    arcadia_user = ArcadiaUser.objects.create(
        d2x_id = 1,
        username = 'TestUser'
    )
    return arcadia_user