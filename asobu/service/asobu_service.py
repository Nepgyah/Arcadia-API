from users.models import ArcadiaUser
from asobu.models import Game, GameListEntry
from asobu.repository import AsobuRepository

class AsobuService:

    @staticmethod
    def get_game_by_id(game_id: int) -> Game:
        return AsobuRepository.get_game_by_id(game_id=game_id)

    @staticmethod
    def create_game_list_entry(user: ArcadiaUser, game_id: Game, status: int, details: dict) -> GameListEntry:
        game = AsobuRepository.get_game_by_id(game_id)
        return AsobuRepository.create_game_list_entry(user, game, status, **details)

    @staticmethod
    def update_game_list_entry(user: ArcadiaUser, game_id: Game, status: int, details: dict) -> GameListEntry:
        game = AsobuRepository.get_game_by_id(game_id)
        return AsobuRepository.update_game_list_entry(user, game, status, **details)

    @staticmethod
    def total_game_count() -> int:
        return Game.objects.all().count()