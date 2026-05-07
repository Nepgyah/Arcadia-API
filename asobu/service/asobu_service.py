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
    def get_game_list_entry(user: ArcadiaUser, game_id: Game) -> GameListEntry:
        return AsobuRepository.get_game_list_entry(user, game_id, None)
    
    @staticmethod
    def update_game_list_entry(user: ArcadiaUser, game_id: Game, status: int, details: dict) -> GameListEntry:
        game = AsobuRepository.get_game_by_id(game_id)
        return AsobuRepository.update_game_list_entry(user, game, status, **details)

    @staticmethod
    def total_game_count() -> int:
        return Game.objects.all().count()
    
    @staticmethod
    def get_game_list_by_user(user: ArcadiaUser):
        gamelist_entries = AsobuRepository.get_game_list_by_user(user)
        playing = gamelist_entries.filter(status=0)
        completed = gamelist_entries.filter(status=1)
        plan_to  = gamelist_entries.filter(status=2)
        on_hold = gamelist_entries.filter(status=3)
        replaying = gamelist_entries.filter(status=4)

        return {
            'playing': playing,
            'completed': completed,
            'plan_to': plan_to,
            'on_hold': on_hold,
            'replaying': replaying 
        }