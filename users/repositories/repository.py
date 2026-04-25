from users.models import ArcadiaUser
from users.exceptions import UserNotFoundError
from miru.models.list_entry import AnimeListEntry

class UserRepository:

    @staticmethod
    def get_user_by_id(user_id: int) -> ArcadiaUser:
        try:
            return ArcadiaUser.objects.get(id=user_id)
        except ArcadiaUser.DoesNotExist:
            raise UserNotFoundError()
        
    @staticmethod
    def get_user_list_stat(user_id: ArcadiaUser) -> dict:
        count = AnimeListEntry.objects.filter(user_id=user_id).count()
        return {
            'anime': count,
            'manga': 0, 
            'games': 0
        }