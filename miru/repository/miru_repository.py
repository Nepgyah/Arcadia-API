from miru.models.anime import Anime
from miru.models.relations import (
    AnimeCharacter,
    AnimeEpisode
)
from miru.models.list_entry import AnimeListEntry
from users.models import User

class MiruRepository:
    ''' Repository layer to work with Anime, AnimeCharacters, etc '''

    @staticmethod
    def get_anime_by_id(anime_id: int) -> Anime:
        try:
            return Anime.objects.select_related(
                'season',
                'studio'
            ).prefetch_related(
                'genres'
            ).get(id=anime_id)
        except Anime.DoesNotExist:
            return None
        
    @staticmethod
    def get_characters_by_anime(anime_id: int) -> list[AnimeCharacter]:
        """
            Returns a list of characters related to an anime.

            Return None if no characters found
        """

        try:
            anime = Anime.objects.get(id=anime_id)
            return AnimeCharacter.objects.filter(anime=anime)
        except Anime.DoesNotExist:
            return []
        
    @staticmethod
    def get_anime_by_category(category: str, count: int) -> list[Anime]: 
        return Anime.objects.order_by(category)[:count]
    
    @staticmethod
    def create_anime_list_entry(user: User, anime: Anime, status: int, details: dict) -> None:
        animeEntry = AnimeListEntry(
            user = user,
            anime = anime,
            status = status
        )
        if details.get('current_episode')  is not None:
            animeEntry.current_episode = details['current_episode']

        if details.get('score')  is not None:
            animeEntry.score = details.get('score')

        if details.get('start_watch_date') is not None:
            animeEntry.start_watch_date = details.get('start_watch_date')

        if details.get('end_watch_date') is not None:
            animeEntry.end_watch_date = details.get('end_watch_date')

        animeEntry.save()

    @staticmethod
    def update_anime_list_entry(user: User, anime: Anime, status: int, details: dict) -> None:
        animeEntry = AnimeListEntry.objects.get(user=user, anime=anime)
        
        if status != animeEntry.status:
            animeEntry.status = status

        if details.get('current_episode') is not None:
            animeEntry.current_episode = details['current_episode']

        if details.get('score') is not None:
            animeEntry.score = details.get('score')

        if details.get('start_watch_date') is not None:
            animeEntry.start_watch_date = details.get('start_watch_date')

        if details.get('end_watch_date') is not None:
            animeEntry.end_watch_date = details.get('end_watch_date')

        animeEntry.save()
        
    @staticmethod
    def delete_anime_list_entry(user: User, anime: Anime) -> None:
        AnimeListEntry.objects.get(user=user, anime=anime).delete()

    @staticmethod
    def get_anime_list_by_user_id(user: User) -> list[AnimeListEntry]:
        anime_list = AnimeListEntry.objects.filter(user=user)
        return anime_list
    
    @staticmethod
    def get_anime_list_entry(user: User, anime: Anime) -> AnimeListEntry:
        try:
            return AnimeListEntry.objects.get(user=user, anime=anime)
        except AnimeListEntry.DoesNotExist:
            return None
        
    @staticmethod
    def episodes_by_anime_id(anime_id: int) -> list[AnimeEpisode]:
        return AnimeEpisode.objects.filter(anime_id=anime_id)