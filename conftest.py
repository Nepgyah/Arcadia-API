import pytest
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from accounts.models import ArcadiaProfile

@pytest.fixture
def admin_user_fixture():
    admin_user = User.objects.create_superuser(
        username='Admin',
        email='admin@d2x.org',
        password='TestPassword123'
    )
    return admin_user

@pytest.fixture
def arcadia_profile_fixture(admin_user_fixture):
    arcadia_user = ArcadiaProfile.objects.create(
        d2x_id = 1,
        username = 'TestUser',
        admin_account = admin_user_fixture
    )
    return arcadia_user

@pytest.fixture
def rest_client(arcadia_user_fixture):
    client = APIClient()
    refresh_token = RefreshToken.for_user(arcadia_user_fixture)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh_token.access_token))
    
    return client