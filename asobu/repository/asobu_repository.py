import logging
from django.db import IntegrityError, transaction
import psycopg2

from users.models import ArcadiaUser
from asobu.models import Game, GameListEntry, GameCharacter, DLC, Review
from asobu.exceptions import AsobuError, GameNotFoundError, AsobuNotFound

from asobu.serializers import GameListEntrySerializer

logger = logging.getLogger(__name__)

class GameRepository:

    @staticmethod
    def get_game(game_id):
        try:
            return Game.objects.get(id=game_id)
        except Game.DoesNotExist as e:
            raise GameNotFoundError(game_id=game_id) from e

    @staticmethod
    def check_game_exists(game_id):
        if Game.objects.filter(id=game_id).exists() is not True:
            raise AsobuNotFound('Game not found')

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
    def create_entry(user_id: int, game_id: int, **details) -> GameListEntry:
        data = {
            'user': user_id,
            'game': game_id,
            **details
        }

        serializer = GameListEntrySerializer(data=data)

        serializer.is_valid(raise_exception=True)
        return serializer.save()
        
    @staticmethod
    def get_entry(user_id: int, game_id: int) -> GameListEntry:
        try:
            return GameListEntry.objects.get(
                user_id=user_id,
                game_id=game_id
            )
        except GameListEntry.DoesNotExist as e:
            raise AsobuNotFound('Entry not found') from e
        
    @staticmethod
    def update_entry(entry: GameListEntry, **details) -> GameListEntry:
        serializer = GameListEntrySerializer(entry, data=details, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()
    
    @staticmethod
    def delete_entry(entry: GameListEntry) -> None:
        try:
            entry.delete()
        except Exception as e:
            raise AsobuError('Error deleting list entry') from e
        
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
    list = GameListEntryRepository()
    review = ReviewRepository()
