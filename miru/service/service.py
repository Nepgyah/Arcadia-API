from django.core.paginator import Paginator
from base.wrappers import require_profile
from miru.models import Anime, AnimeCompany, AnimeListEntry, AnimeReview, FavoriteAnime, CustomAnimeList
from miru.models.relations import AnimeCharacter
from miru.repository import MiruRepository
from talent.service import CharacterService, VoiceActorService

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
    def get_similar_anime(anime_id: int, count: int) -> list[Anime]:
        count = min(count, 10)
        count = max(count, 0)

        anime = MiruRepository.anime.get_anime(anime_id)
        similar_anime = MiruRepository.anime.get_similar_anime(anime, count)
        return similar_anime
    
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
    def create_entry(profile_id: int, anime_id: int, details: dict = None) -> AnimeListEntry:
        MiruRepository.anime.does_anime_exist(anime_id)
        return MiruRepository.list.create_entry(
            profile_id,
            anime_id,
            **details
        )

    @staticmethod
    def get_entry(profile_id: int, anime_id: int) -> AnimeListEntry:
        return MiruRepository.list.get_entry(profile_id, anime_id)

    @staticmethod
    def update_entry(profile_id: int, anime_id: int, details: dict = None) -> AnimeListEntry:
        entry = MiruRepository.list.get_entry(profile_id, anime_id)
        return MiruRepository.list.update_entry(
            entry,
            **details
        )
    
    @staticmethod
    def delete_entry(profile_id: int, anime_id: int) -> None:
        entry = MiruRepository.list.get_entry(profile_id, anime_id)
        MiruRepository.list.delete_entry(entry)

    @staticmethod
    def get_user_list(profile_id: int) -> dict:

        # user = UserService.get_user(profile_id)
        list_entries = MiruRepository.list.get_user_list(profile_id)
        user_anime_list = {
            'watching': list_entries.filter(status=0),
            'completed': list_entries.filter(status=1),
            'plan_to': list_entries.filter(status=2),
            'on_hold': list_entries.filter(status=3),
        }
        return user_anime_list
    
    @staticmethod
    def get_user_list_count(profile_id: int) -> int:
        return MiruRepository.list.get_user_list_count(profile_id)

    #TODO: Add custom anime list methods
    @staticmethod
    def get_custom_anime_list(profile_id: int, list_id: int) -> CustomAnimeList:
        return MiruRepository.list.get_custom_anime_list(profile_id, list_id)

    @staticmethod
    def create_custom_anime_list(profile_id: int, details = dict) -> None:
        details['profile_id'] = profile_id
        MiruRepository.list.create_custom_anime_list(**details)

    @staticmethod
    def update_custom_anime_list_details(profile_id: int, list_id: int, data: dict) -> None:
        custom_list = MiruRepository.list.get_custom_anime_list(profile_id, list_id)
        MiruRepository.list.update_custom_anime_list_details(custom_list, **data)

    @staticmethod
    def delete_custom_anime_list(profile_id: int, list_id: int) -> None:
        custom_list = MiruRepository.list.get_custom_anime_list(profile_id, list_id)
        MiruRepository.list.delete_custom_anime_list(custom_list)

    @staticmethod
    def add_to_custom_anime_list(profile_id: int, list_id: int, anime_id: int) -> None:
        custom_list = MiruRepository.list.get_custom_anime_list(profile_id, list_id)
        anime = MiruRepository.anime.get_anime(anime_id)
        MiruRepository.list.add_to_custom_anime_list(custom_list, anime)

    @staticmethod
    def remove_from_custom_anime_list(profile_id: int, list_id: int, anime_id: int) -> None:
        custom_list = MiruRepository.list.get_custom_anime_list(profile_id, list_id)
        anime = MiruRepository.anime.get_anime(anime_id)
        MiruRepository.list.remove_from_custom_anime_list(custom_list, anime)
    
class Character:

    @staticmethod
    def get_anime_roles(voice_actor_id: str):
        characters = VoiceActorService.get_voice_actor_roles(voice_actor_id)
        anime_roles = []
        
        for character in characters:
            character_appearances = AnimeCharacter.objects.filter(character=character).select_related('anime')
            if len(character_appearances):
                appearance_json = [
                    {
                        "role": appearance.get_role_display(),
                        "anime": appearance.anime
                    } for appearance in character_appearances
                ]
                temp = {
                    "character": character,
                    "appearances": appearance_json
                }
                anime_roles.append(temp)

        return anime_roles

class Review:

    @staticmethod
    def create(profile_id: int, anime_id: int, details: dict = None) -> AnimeReview:
        MiruRepository.anime.does_anime_exist(anime_id)
        return MiruRepository.review.create(
            profile_id,
            anime_id,
            **details
        )

    @staticmethod
    def get(profile_id: int, anime_id: int) -> AnimeReview:
        return MiruRepository.review.get_review(profile_id, anime_id)

    @staticmethod
    def update(profile_id: int, anime_id: int, details: dict = None) -> AnimeReview:
        entry = MiruRepository.review.get_review(profile_id, anime_id)
        return MiruRepository.review.update(
            entry,
            **details
        )
    
    @staticmethod
    def delete(profile_id: int, anime_id: int) -> None:
        entry = MiruRepository.review.get_review(profile_id, anime_id)
        MiruRepository.review.delete(entry)

class Favorite:
    
    @staticmethod
    @require_profile
    def add_favorite_anime(profile_id: int, anime_id: int) -> None:
        anime = MiruRepository.anime.get_anime(anime_id)
        MiruRepository.favorite.add_favorite_anime(profile_id, anime)

    @staticmethod
    @require_profile
    def remove_favorite_anime(profile_id: int, anime_id: int) -> None:
        anime = MiruRepository.anime.get_anime(anime_id)
        MiruRepository.favorite.remove_favorite_anime(profile_id, anime)

    @staticmethod
    @require_profile
    def get_favorite_anime(profile_id: int) -> list[FavoriteAnime]:
        return MiruRepository.favorite.get_favorite_anime(profile_id)
    
class MiruService:
    
    anime = AnimeService()
    list = ListService()
    character = Character()
    review = Review()
    favorite = Favorite()