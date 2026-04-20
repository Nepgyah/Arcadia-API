import logging

from django.db import IntegrityError
import graphene_django_optimizer as gql_optimizer

from talent.models import Character
from users.models import ArcadiaUser
from asobu.models import Game, GameListEntry, GameCharacter, DLC
from asobu.exceptions import AsobuError, GameNotFoundError, AsobuNotFound

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
    def get_game_list_entry(user: ArcadiaUser, game_id: int, graphql_info):
            
        try:
            if graphql_info:
                query = gql_optimizer.query(
                    GameListEntry.objects.filter(user=user, game_id=game_id),
                    graphql_info
                )
                return query.get()
            else:
                return GameListEntry.objects.get(user=user, game_id=game_id)
        except GameListEntry.DoesNotExist:
            raise AsobuNotFound('Entry not found')
        
    @staticmethod
    def create_game_list_entry(user: ArcadiaUser, game: Game, status: int, **kwargs) -> GameListEntry:
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
        
    @staticmethod
    def update_game_list_entry(user: ArcadiaUser, game: Game, status: int, **kwargs) -> GameListEntry:
        try:
            entry = GameListEntry.objects.get(
                user=user,
                game=game
            )
            if status != entry.status:
                entry.status = status

            score = kwargs.pop('score', None)
            if score != entry.score:
                entry.score = score

            entry.save() 
            return entry
        except GameListEntry.DoesNotExist:
            raise AsobuNotFound('Entry not found')
        except IntegrityError as e:
            logger.error(e)
            raise AsobuError('An error occured updating the entry.')
        except Exception as e:
            print(e)
            raise AsobuError