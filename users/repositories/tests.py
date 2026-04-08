import pytest
from users.repositories.repository import UserRepository
from users.exceptions import UserNotFoundError

@pytest.mark.django_db
class TestRepository:

    @staticmethod
    def test_get_user(arcadia_user_fixture):
        user = UserRepository.get_user_by_id(arcadia_user_fixture.id)
        assert user == arcadia_user_fixture

    @staticmethod
    def test_get_user_not_found(arcadia_user_fixture):
        non_existend_id = -1
        with pytest.raises(UserNotFoundError) as exception:
            UserRepository.get_user_by_id(non_existend_id)

        assert exception.value.status_code == 404
        assert str(non_existend_id) in exception.value.detail