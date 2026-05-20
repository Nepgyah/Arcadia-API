from django.core.paginator import Paginator
from users.services import UserService
from miru.models import Anime, AnimeCompany, AnimeListEntry
from miru.repository import MiruRepository
from talent.service.character import CharacterService

class AnimeService:

    @staticmethod
    def get_anime(anime_id: int) -> Anime:
        return MiruRepository.anime.get_anime(anime_id)
    
    @staticmethod
    def search_anime(filters: dict = None, sort: dict = None, pagination: dict = None) -> list[Anime]:
        queryset = Anime.objects.all()

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
    
class ListService:

    @staticmethod
    def create_entry(user_id: int, anime_id: int, details: dict = None) -> AnimeListEntry:
        MiruRepository.anime.does_anime_exist(anime_id)
        return MiruRepository.list.create_entry(
            user_id,
            anime_id,
            **details
        )

    @staticmethod
    def get_entry(user_id: int, anime_id: int) -> AnimeListEntry:
        return MiruRepository.list.get_entry(user_id, anime_id)

    @staticmethod
    def update_entry(user_id: int, anime_id: int, details: dict = None) -> AnimeListEntry:
        entry = MiruRepository.list.get_entry(user_id, anime_id)
        return MiruRepository.list.update_entry(
            entry,
            **details
        )
    
    @staticmethod
    def delete_entry(user_id: int, anime_id: int) -> None:
        entry = MiruRepository.list.get_entry(user_id, anime_id)
        MiruRepository.list.delete_entry(entry)

    @staticmethod
    def get_user_list(user_id: int) -> dict:

        user = UserService.get_user(user_id)
        list_entries = MiruRepository.list.get_user_list(user_id)
        user_anime_list = {
            'watching': list_entries.filter(status=0),
            'completed': list_entries.filter(status=1),
            'plan_to': list_entries.filter(status=2),
            'on_hold': list_entries.filter(status=3),
        }
        return user, user_anime_list
    
class MiruService:
    
    anime = AnimeService()
    list = ListService()