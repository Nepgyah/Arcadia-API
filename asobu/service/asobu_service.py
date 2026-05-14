from users.models import ArcadiaUser
from asobu.models import Game, GameListEntry, DLC
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
        return AsobuRepository.game.get_dlc(game_id)

class AsobuService:

    game = GameService()