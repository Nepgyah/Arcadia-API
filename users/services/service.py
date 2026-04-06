from users.repositories import UserRepository
from users.models import ArcadiaUser

class UserService:

    @staticmethod
    def get_user_by_id(user_id: int) -> ArcadiaUser:
        return UserRepository.get_user_by_id(user_id)