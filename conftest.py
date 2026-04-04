import pytest
from users.models import ArcadiaUser

@pytest.fixture
def arcadia_user_fixture():
    arcadia_user = ArcadiaUser.objects.create(
        d2x_id = 1,
        username = 'TestUser'
    )
    return arcadia_user