import logging

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
    def get_dlc(game_id: int) -> list:
        return DLC.objects.filter(game_id=game_id)

    @staticmethod
    def get_reviews(game_id: int) -> list:
        return GameListEntry.objects.filter(
            game_id=game_id,
            is_private=False
        )

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
                review=kwargs.pop('review', None),
                start_play_date=kwargs.pop('start_play_date', None),
                end_play_date=kwargs.pop('end_play_date', None)
            )  

        except Exception as e:
            logger.warning(e)
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
    def create_review(user: ArcadiaUser, game: Game, **fields: dict) -> Review:
        review_text = fields.pop('text', None)

        if not review_text:
            raise AsobuError('A review cannot be empty')
        
        review = Review(
            user=user,
            game=game,
            text=fields.pop('text')
        ) 
        review.objects.create()
        return review

    @staticmethod
    def get_review(review_id: int) -> Review:
        try:
            return GameListEntry.objects.get(id=review_id)
        except Review.DoesNotExist as e:
            raise AsobuNotFound('Review not found') from e
        
    @staticmethod
    def update_review(review_id: int, user_id: int, **kwargs) -> Review:
        try:
            review = Review.objects.get(id=review_id, user_id=user_id)
            review.text = kwargs.pop('review', None)
            review.save()

            return review
        
        except GameListEntry.DoesNotExist as e:
            raise AsobuNotFound('Review not found') from e

    @staticmethod
    def delete_review(review_id: int, user_id: int) -> None:
        try:
            review = Review.objects.get(id=review_id, user_id=user_id)
            review.delete()
        except Review.DoesNotExist as e:
            raise AsobuNotFound('Cannot find review') from e
        
class AsobuRepository:

    game = GameRepository()
    list_entry = GameListEntryRepository()
    review = ReviewRepository()
