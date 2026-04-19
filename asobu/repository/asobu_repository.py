import logging

from talent.models import Character
from users.models import ArcadiaUser
from asobu.models import Game, GameListEntry, GameCharacter, DLC
from asobu.exceptions import AsobuError, GameNotFoundError

logger = logging.getLogger(__name__)

class AsobuRepository:

    @staticmethod
    def get_game_by_id(game_id):
        try:
            return Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            raise GameNotFoundError(game_id=game_id)
    
    @staticmethod
    def get_dlc_by_game(game_id: int) -> list:
        return DLC.objects.filter(game_id=game_id)

    @staticmethod
    def get_characters_by_game(game_id: int) -> list:
        return GameCharacter.objects.filter(game_id=game_id)

    @staticmethod
    def create_asobu_list_entry(user: ArcadiaUser, game: Game, status: int, **kwargs) -> GameListEntry:
        try:
            return GameListEntry.objects.create(
                user=user,
                game=game,
                status=status,
                score=kwargs.pop('score', None),
                note=kwargs.pop('note', None),
                review=kwargs.pop('review', None),
                start_play_date=kwargs.pop('start_play_date', None),
                end_play_date=kwargs.pop('end_play_date', None)
            )  

        except Exception as e:
            logger.warning(e)
            raise AsobuError
    