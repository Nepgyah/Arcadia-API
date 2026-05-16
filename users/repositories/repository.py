from django.db.models import Q
from users.models import ArcadiaUser
from users.exceptions import UserNotFoundError
from miru.models.list_entry import AnimeListEntry
from asobu.models.list import GameListEntry

class UserRepository:

    @staticmethod
    def get_user(user_id: int) -> ArcadiaUser:
        try:
            return ArcadiaUser.objects.get(id=user_id)
        except ArcadiaUser.DoesNotExist:
            raise UserNotFoundError() from None

    @staticmethod
    def get_user_by_id(user_id: int) -> ArcadiaUser:
        try:
            return ArcadiaUser.objects.get(id=user_id)
        except ArcadiaUser.DoesNotExist:
            raise UserNotFoundError() from None
        
    @staticmethod
    def get_user_list_stat(user_id: int) -> dict:
        anime_count = AnimeListEntry.objects.filter(user_id=user_id, status=0).count()
        game_count = GameListEntry.objects.filter(user_id=user_id).filter(Q(status=0) | Q(status=4)).count()

        return {
            'anime': anime_count,
            'manga': 0, 
            'games': game_count
        }