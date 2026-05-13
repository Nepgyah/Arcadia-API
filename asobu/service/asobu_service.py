from users.models import ArcadiaUser
from asobu.models import Game, GameListEntry
from asobu.repository import AsobuRepository
from talent.service.character import CharacterService

class AsobuServiceDeprecate:

    @staticmethod
    def get_game_by_id(game_id: int) -> Game:
        return AsobuRepository.get_game_by_id(game_id=game_id)

    @staticmethod
    def create_game_list_entry(user: ArcadiaUser, game_id: Game, status: int, details: dict) -> GameListEntry:
        game = AsobuRepository.game.get_game(game_id)
        return AsobuRepository.list_entry.create_entry(user, game, status, **details)

    @staticmethod
    def get_game_list_entry(user: ArcadiaUser, game_id: Game) -> GameListEntry:
        return AsobuRepository.list_entry.get_entry(user, game_id, None)
    
    @staticmethod
    def update_game_list_entry(user: ArcadiaUser, game_id: Game, status: int, details: dict) -> GameListEntry:
        game = AsobuRepository.game.get_game(game_id)
        return AsobuRepository.list_entry.update_entry(user, game, status, **details)

    @staticmethod
    def total_game_count() -> int:
        return Game.objects.all().count()
    
    @staticmethod
    def get_game_list_by_user(user: ArcadiaUser):
        gamelist_entries = AsobuRepository.list_entry.get_user_list(user.id)
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

class AsobuService:

    game = GameService()