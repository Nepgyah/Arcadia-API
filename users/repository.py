from .models import ArcadiaUser

class UserRepository:

    @staticmethod
    def get_user_by_id(user_id: int) -> ArcadiaUser:
        try:
            return ArcadiaUser.objects.get(id=user_id)
        except ArcadiaUser.DoesNotExist:
            raise Exception(f'Cannot find user with id: {user_id}')