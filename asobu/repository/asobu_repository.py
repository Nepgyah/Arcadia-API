import logging
from django.db import IntegrityError, transaction
import psycopg2
import graphene_django_optimizer as gql_optimizer
from users.models import ArcadiaUser
from asobu.models import Game, GameListEntry, GameCharacter, DLC, Review
from asobu.exceptions import AsobuError, GameNotFoundError, AsobuNotFound

logger = logging.getLogger(__name__)

class GameRepository:

    @staticmethod
    def get_game(game_id):
        try:
            return Game.objects.get(id=game_id)
        except Game.DoesNotExist as e:
            raise GameNotFoundError(game_id=game_id) from e

    @staticmethod
    def get_characters(game_id):
        return GameCharacter.objects.filter(game_id=game_id)
    
    @staticmethod
    def get_character_relations(game_id):
        return GameCharacter.objects.filter(game_id=game_id)

    @staticmethod
    def get_dlc(game_id: int) -> list:
        return DLC.objects.filter(game_id=game_id)

    @staticmethod
    def get_reviews(game_id: int) -> list:
        return Review.objects.filter(game_id=game_id)

class GameListEntryRepository:

    @staticmethod
    def create_entry(user: ArcadiaUser, game: Game, status: int, **kwargs) -> GameListEntry:
        try:
            return GameListEntry.objects.create(
                user=user,
                game=game,
                status=status,
                score=kwargs.pop('score', None),
                note=kwargs.pop('note', None),
                start_play_date=kwargs.pop('start_play_date', None),
                end_play_date=kwargs.pop('end_play_date', None)
            )  

        except Exception as e:
            logger.exception(e)
            raise AsobuError from e
        
    @staticmethod
    def get_entry(user: ArcadiaUser, game_id: int, graphql_info: dict) -> GameListEntry:
        try:
            if graphql_info:
                query = gql_optimizer.query(
                    GameListEntry.objects.filter(user=user, game_id=game_id),
                    graphql_info
                )
                return query.get()
            return GameListEntry.objects.get(user=user, game_id=game_id)
        
        except GameListEntry.DoesNotExist:
            return None

    @staticmethod
    def update_entry(user: ArcadiaUser, game: Game, status: int, **kwargs) -> GameListEntry:
        try:
            entry = GameListEntry.objects.get(user=user, game=game)
            entry.status = status
            entry.score = kwargs.pop('score', None)
            entry.note = kwargs.pop('note', None)
            entry.start_play_date = kwargs.pop('start_play_date', None)
            entry.end_play_date = kwargs.pop('end_play_date', None)
            entry.save()
            return entry
        
        except Exception as e:
            logger.exception(e)
            raise AsobuError from e
    
    @staticmethod
    def delete_game_list_entry(user: ArcadiaUser, entry_id: int) -> None:
        try:
            GameListEntry.objects.get(id=entry_id, user=user,).delete()
        except GameListEntry.DoesNotExist:
            raise AsobuNotFound('Cannot find game entry') from None
        except Exception as e:
            logging.error(e)
            raise AsobuError('An error occured deleting the entry') from e
        
    @staticmethod
    def get_user_list(user_id: int) -> list:
        return GameListEntry.objects.filter(user_id=user_id)
    
class ReviewRepository:

    @staticmethod
    def create_review(user_id: int, game_id: int, review_text: str) -> Review:

        if not review_text or review_text == '':
            raise AsobuError('A review cannot be empty')
        try:
            with transaction.atomic():
                return Review.objects.create(
                    user_id=user_id,
                    game_id=game_id,
                    text=review_text
                )
            
        except psycopg2.errors.ForeignKeyViolation as e:
            raise AsobuError(code=404, detail='Game not found') from e
        
        except IntegrityError as e:
            error_str = str(e).lower()
            
            if 'unique constraint' in error_str:
                raise AsobuError(code=409, detail='Review already exists') from e
            
            raise AsobuError(code=500, detail='Unexpected error creating game') from e

    @staticmethod
    def get_review_by_user(user_id: int, game_id: int) -> Review:
        try:
            return Review.objects.get(user_id=user_id, game_id=game_id)
        except Review.DoesNotExist:
            return None

    @staticmethod
    def get_review(review_id: int) -> Review:
        try:
            return Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return None
        
    @staticmethod
    def update_review(user_id: int, game_id: int, review_text: str) -> Review:
        if review_text is None or review_text == '':
            raise AsobuError('Review text cannot be empty')
        try:
            review = Review.objects.get(game_id=game_id, user_id=user_id)
            review.text = review_text
            review.save()

            return review
        
        except Review.DoesNotExist as e:
            raise AsobuNotFound('Cannot find review to update') from e

    @staticmethod
    def delete_review(user_id: int, game_id: int) -> None:
        try:
            review = Review.objects.get(user_id=user_id, game_id=game_id)
            review.delete()
        except Review.DoesNotExist as e:
            raise AsobuNotFound('Cannot find review') from e
        
class AsobuRepository:

    game = GameRepository()
    list_entry = GameListEntryRepository()
    review = ReviewRepository()
