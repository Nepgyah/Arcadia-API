from django.core.paginator import Paginator
from miru.repository.miru_repository import MiruRepository
from miru.models import Anime, AnimeCharacter, AnimeListEntry, AnimeEpisode
from users.models import User

class MiruService:
    ''' Service layer to apply business logic to Miru '''

    @staticmethod
    def get_anime_by_id(anime_id: int) -> Anime:
        return MiruRepository.get_anime_by_id(anime_id)
    
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
    def search_anime(filters: dict, sort: dict, pagination: dict):
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

        paginator = Paginator(queryset, per_page=pagination['per_page'])
        results = paginator.get_page(pagination['current_page']).object_list
        page_count = paginator.num_pages
        total = paginator.count

        return results, page_count, pagination['current_page'], total
    
    @staticmethod
    def add_anime_list_entry(user_id: int, anime_id: int, status: int, details: dict) -> bool:
        """
        Creates an anime list entry based on user_id and anime_id combination

        Returns:
        - Boolean status (ok) of the operation
        """

        user = User.objects.get(id=user_id)
        anime = MiruRepository.get_anime_by_id(anime_id)

        if anime is None or user is None:
            return False
        try:
            MiruRepository.create_anime_list_entry(user, anime, status, details)
        except Exception:
            # TODO: Handle errors such as uniqueness, etc
            return False
        
        return True

    @staticmethod
    def update_anime_list_entry(user_id: int, anime_id: int, status: int, details: dict) -> bool:
        """
        Updates a current anime list entry based on user_id and anime_id combination

        Returns:
        - Boolean status (ok) of the operation
        """
        
        user = User.objects.get(id=user_id)
        anime = MiruRepository.get_anime_by_id(anime_id)

        if anime is None or user is None:
            return False
        try:
            MiruRepository.update_anime_list_entry(user, anime, status, details)
        except Exception:
            # TODO: Handle errors such as uniqueness, etc
            return False
        
        return True

    @staticmethod
    def delete_anime_list_entry(user_id: int, anime_id: int) -> bool:
        """
        Deletes a current anime list entry based on user_id and anime_id combination

        Returns:
        - Boolean status (ok) of the operation
        """

        user = User.objects.get(id=user_id)
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
        user = User.objects.get(id=user_id)
        anime_list =  MiruRepository.get_anime_list_by_user_id(user)
        watching = anime_list.filter(status=0)
        completed = anime_list.filter(status=1)
        plan_to = anime_list.filter(status=2)
        on_hold = anime_list.filter(status=3)

        return watching, completed, plan_to, on_hold
    
    @staticmethod
    def get_anime_list_entry(user_id, anime_id) -> AnimeListEntry:
        user = User.objects.get(id=user_id)
        anime = MiruRepository.get_anime_by_id(anime_id)
        if anime is None or user is None:
            return None
        
        return MiruRepository.get_anime_list_entry(user, anime)
    
    @staticmethod
    def episodes_by_anime_id(anime_id: int) -> AnimeEpisode:
        return MiruRepository.episodes_by_anime_id(anime_id)