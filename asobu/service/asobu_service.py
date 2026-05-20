from django.core.paginator import Paginator
from users.services import UserService
from asobu.models import Game, GameListEntry, DLC, Review
from asobu.exceptions import AsobuError
from asobu.repository import AsobuRepository
from talent.service.character import CharacterService

class GameService:

    @staticmethod
    def get_game(game_id: int) -> Game:
        return AsobuRepository.game.get_game(game_id)

    @staticmethod
    def get_cast(game_id: int) -> list:
        """
        Returns a dict containing details for a cast of characters.

        keys:
            - character: Character details
            - role: "main" or "supporting"
            - voice_actor: Voice Actor details
        """
        
        character_relations = AsobuRepository.game.get_character_relations(game_id)
        char_ids = [rel.character_id for rel in character_relations]

        character_map = CharacterService.get_characters_by_id(
            char_ids, 
            get_va_data=True
        )

        game_characters = []
        for relation in character_relations:
            data = {}
            character = character_map.get(relation.character_id)
            data['character'] = character
            data['role'] = relation.get_role_display()
            data['voice_actor'] = character.voice_actor
            game_characters.append(data)

        return game_characters

    @staticmethod
    def get_dlc(game_id: int) -> list[DLC]:
        AsobuRepository.game.check_game_exists(game_id)
        return AsobuRepository.game.get_dlc(game_id)

    @staticmethod
    def get_reviews(game_id: int) -> list[Review]:
        AsobuRepository.game.check_game_exists(game_id)
        return AsobuRepository.game.get_reviews(game_id)

    @staticmethod
    def search_games(filters: dict = None, sort: dict = None, pagination: dict = None):
        queryset = Game.objects.all()

        if filters:
            if filters['type'] != -1:
                queryset = queryset.filter(type=filters['type'])
            if filters['status'] != -1:
                queryset = queryset.filter(status=filters['status'])
            if filters['title'] != '':
                queryset = queryset.filter(title__icontains=filters['title'])

        if sort:
            direction = '' if sort['direction'] == 'asc' else '-'
            if sort['category'] != '':
                queryset = queryset.order_by(f'{direction}{sort["category"]}')

        if pagination:
            paginator = Paginator(queryset, per_page=pagination['per_page'])
            results = paginator.get_page(pagination['target_page']).object_list
            pagination_results = {
                'per_page': pagination['per_page'],
                'total_pages': paginator.num_pages,
                'total_items': paginator.count
            }
            return results, pagination_results
        
        return queryset, None
    
class ListService:

    @staticmethod
    def create_entry(user_id: int, game_id: int, details: dict = None) -> GameListEntry:
        
        AsobuRepository.game.check_game_exists(game_id)
        return AsobuRepository.list.create_entry(
            user_id=user_id,
            game_id=game_id,
            **details
        )

    @staticmethod
    def get_entry(user_id: int, game_id: int) -> GameListEntry:
        return AsobuRepository.list.get_entry(user_id, game_id)

    @staticmethod
    def update_entry(user_id: int, game_id: int, details: dict = None) -> GameListEntry:

        entry = AsobuRepository.list.get_entry(user_id, game_id)
        return AsobuRepository.list.update_entry(entry, **details)

    @staticmethod
    def delete_entry(user_id: int, game_id: int) -> None:
        entry = AsobuRepository.list.get_entry(user_id, game_id)
        AsobuRepository.list.delete_entry(entry)

    @staticmethod
    def get_user_list(user_id: int) -> dict:
        """
            Returns the user and a dict of filtered list entires by status
        """
        
        user = UserService.get_user(user_id)
        list_entries = AsobuRepository.list.get_user_list(user_id)
        user_game_list = {
            'playing': list_entries.filter(status=0),
            'completed': list_entries.filter(status=1),
            'plan_to': list_entries.filter(status=2),
            'on_hold': list_entries.filter(status=3),
            'replaying': list_entries.filter(status=4) 
        }
        return user, user_game_list
        
class ReviewService:

    @staticmethod
    def create_review(user_id: int, game_id: int, text: str = None) -> Review:
        if text is None or text == '':
            raise AsobuError('Review text cannot be empty')

        return AsobuRepository.review.create_review(
            user_id=user_id,
            game_id=game_id,
            text=text
        )
    
    @staticmethod
    def get_review(user_id: int, game_id: int) -> Review:
        return AsobuRepository.review.get_review(user_id, game_id)

    @staticmethod
    def update_review(user_id: int, game_id: int, text: str = None) -> Review:
        if text is None or text == '':
            raise AsobuError('Review text cannot be empty')
        
        review = AsobuRepository.review.get_review(user_id, game_id)
        return AsobuRepository.review.update_review(review, text)
    
    @staticmethod
    def delete_review(user_id: int, game_id: int) -> None:
        review = AsobuRepository.review.get_review(user_id, game_id)
        return AsobuRepository.review.delete_review(review)

class AsobuService:

    game = GameService()
    list = ListService()
    review = ReviewService()