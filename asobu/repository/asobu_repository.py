import logging

from asobu.models import Game, GameListEntry, GameCharacter, DLC, Review
from asobu.exceptions import AsobuError, AsobuNotFound
from asobu.serializers import GameListEntrySerializer

logger = logging.getLogger(__name__)

class GameRepository:

    @staticmethod
    def get_game_count() -> int:
        return Game.objects.count()

    @staticmethod
    def get_game(game_id):
        try:
            return Game.objects.get(id=game_id)
        except Game.DoesNotExist as e:
            raise AsobuNotFound(f"Unable to find game with id: {game_id}") from e

    @staticmethod
    def does_game_exist(game_id):
        return Game.objects.filter(id=game_id).exists()

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
    def create_entry(profile_id: int, game_id: int, **details) -> GameListEntry:
        data = {
            'profile_id': profile_id,
            'game': game_id,
            **details
        }

        serializer = GameListEntrySerializer(data=data)

        serializer.is_valid(raise_exception=True)
        return serializer.save()
        
    @staticmethod
    def get_entry(profile_id: int, game_id: int) -> GameListEntry:
        try:
            return GameListEntry.objects.get(
                profile_id=profile_id,
                game_id=game_id
            )
        except GameListEntry.DoesNotExist:
            return None
        
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
    def get_user_list(profile_id: int) -> list[GameListEntry]:
        return GameListEntry.objects.filter(profile_id=profile_id)
    
class ReviewRepository:

    @staticmethod
    def create_review(profile_id: int, game_id, text: str) -> Review:
        return Review.objects.create(
            profile_id=profile_id,
            game_id=game_id,
            text=text
        )

    @staticmethod
    def get_review(profile_id: int, game_id: int) -> Review:
        try:
            return Review.objects.get(
                profile_id=profile_id,
                game_id=game_id
            )
        except Review.DoesNotExist as e:
            raise AsobuNotFound('Unable to find review') from e
    
    @staticmethod
    def update_review(review: Review, text: str = None) -> Review:
        if text is None or text == '':
            raise AsobuError('Review text cannot be empty')
        
        review.text = text
        review.save()
        return review
    
    @staticmethod
    def delete_review(review: Review) -> None:
        try:
            review.delete()
        except Exception as e:
            raise AsobuError('An error occured deleting the review') from e
        
class AsobuRepository:

    game = GameRepository()
    list = GameListEntryRepository()
    review = ReviewRepository()
