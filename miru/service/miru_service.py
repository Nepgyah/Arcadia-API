import logging

from django.core.paginator import Paginator

from users.services import UserService
from miru.repository.miru_repository import MiruRepository
from miru.models.anime import Anime
from miru.models.relations import (
    AnimeCharacter,
    AnimeEpisode
)
from miru.models.list_entry import AnimeListEntry
from users.models import ArcadiaUser
from miru.exceptions import MiruError

from talent.service.character import CharacterService

logger = logging.getLogger(__name__)

class MiruService:
    ''' Service layer to apply business logic to Miru '''

    @staticmethod
    def get_anime_by_id(anime_id: int) -> Anime:
        return MiruRepository.get_anime_by_id(anime_id)
        
    # SOON TO DEPRECATE
    @staticmethod
    def get_characters_by_anime(anime_id: int) -> list[AnimeCharacter]:
        return MiruRepository.get_characters_by_anime(anime_id)
        
    @staticmethod
    def get_anime_by_category(category: str, count: int) -> list[Anime]:
        """
        Retrieves anime sorted by a category, descending. Defaults to the first 5 if count is not provided.
        """

        if count is None:
            count = 5
        return MiruRepository.get_anime_by_category(category, count)
    
    @staticmethod
    def search_anime(filters: dict, sort: dict, pagination_input: dict):
        """
        Searches anime with optional filters and sorts.
        Filters are ignored with -1 input.

        Returns:
        - results: anime queryset based on the page
        - page_count: total number of pages created from pagination
        - pagination: current page of the paginated results
        - total: total number of items from the anime queryset
        """

        queryset = Anime.objects.all()
        
        if filters:
            if filters['type'] != -1:
                queryset = queryset.filter(type=filters['type'])
            if filters['status'] != -1:
                queryset = queryset.filter(status=filters['status'])
            if filters['title'] != '':
                #TODO: Add functionality to query multiple languages
                queryset = queryset.filter(title__icontains=filters['title'])

        if sort:
            direction = '' if sort['direction'] == 'asc' else '-'
            if sort['category'] != "":
                queryset = queryset.order_by(f'{direction}{sort['category']}')

        paginator = Paginator(queryset, per_page=pagination_input['per_page'])
        results = paginator.get_page(pagination_input['target_page']).object_list
        pagination_results = {
            'per_page': pagination_input['per_page'],
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
        }

        return results, pagination_results
    
    @staticmethod
    def add_anime_list_entry(user: ArcadiaUser, anime_id: int, status: int, details: dict) -> bool:

        anime = MiruRepository.get_anime_by_id(anime_id)
        return MiruRepository.create_anime_list_entry(user, anime, status, **details)
        
    @staticmethod
    def update_anime_list_entry(user: ArcadiaUser, anime_id: int, status: int, details: dict) -> bool:
        """
        Updates a current anime list entry based on user_id and anime_id combination

        Returns:
        - Boolean status (ok) of the operation
        """

        anime = MiruRepository.get_anime_by_id(anime_id)
        return MiruRepository.update_anime_list_entry(user, anime, status, details)


    @staticmethod
    def delete_anime_list_entry(user_id: int, anime_id: int) -> bool:
        """
        Deletes a current anime list entry based on user_id and anime_id combination

        Returns:
        - Boolean status (ok) of the operation
        """

        user = ArcadiaUser.objects.get(id=user_id)
        anime = MiruRepository.get_anime_by_id(anime_id)

        if anime is None or user is None:
            return False
        
        try:
            MiruRepository.delete_anime_list_entry(user, anime)
        except Exception:
            return False

        return True
    
    @staticmethod
    def get_anime_list_by_user_id(user_id: int) -> list[AnimeListEntry]:
        user = UserService.get_user_by_id(user_id)
        anime_list =  MiruRepository.get_anime_list_by_user_id(user)
        watching = anime_list.filter(status=0)
        completed = anime_list.filter(status=1)
        plan_to = anime_list.filter(status=2)
        on_hold = anime_list.filter(status=3)

        return watching, completed, plan_to, on_hold
    
    @staticmethod
    def get_anime_list_entry(user: ArcadiaUser, anime_id) -> AnimeListEntry:
        anime = MiruRepository.get_anime_by_id(anime_id)
        if anime is None or user is None:
            return None
        
        return MiruRepository.get_anime_list_entry(user, anime)
    
    @staticmethod
    def episodes_by_anime_id(anime_id: int) -> AnimeEpisode:
        return MiruRepository.episodes_by_anime_id(anime_id)
    
    @staticmethod
    def total_anime_count() -> int:
        return Anime.objects.all().count()
    
class AnimeService:

    @staticmethod
    def get_cast(anime_id: int) -> list:
        anime_characters = AnimeCharacter.objects.filter(anime=anime_id)


class MiruService:

    anime = AnimeService()