from miru.models import Anime, AnimeCompany
from miru.repository import MiruRepository
from talent.service.character import CharacterService

class AnimeService:

    @staticmethod
    def get_anime(anime_id: int) -> Anime:
        return MiruRepository.anime.get_anime(anime_id)
    
    @staticmethod
    def get_cast(anime_id: int) -> list:
        character_relations = MiruRepository.anime.get_characters(anime_id)
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
    
class CompanyService:

    @staticmethod
    def get_producers(company_id_list: list[int]) -> list[AnimeCompany]:
        return MiruRepository.company.get_companies(company_id_list)
    
class MiruService:
    
    anime = AnimeService()