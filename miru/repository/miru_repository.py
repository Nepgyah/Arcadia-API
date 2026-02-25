from miru.models import (
    Anime,
    AnimeCharacter,
    AnimeListEntry
)

class MiruRepository:
    ''' Repository layer to work with Anime, AnimeCharacters, etc '''

    @staticmethod
    def get_anime_by_id(id):
        try:
            return Anime.objects.get(id=id)
        except Anime.DoesNotExist:
            return None
        
    @staticmethod
    def get_characters_by_anime(id):
        """
            Returns a list of characters related to an anime.

            Return None if no characters found
        """

        try:
            anime = Anime.objects.get(id=id)
            return AnimeCharacter.objects.filter(anime=anime)
        except Anime.DoesNotExist:
            return []
        
    @staticmethod
    def get_anime_by_category(category, count):
        return Anime.objects.order_by(category)[:5]
    
    @staticmethod
    def create_anime_list_entry(user, anime, status, details):
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
    def update_anime_list_entry(user, anime, status, details):
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
    def delete_anime_list_entry(user, anime):
        AnimeListEntry.objects.get(user=user, anime=anime).delete()

    @staticmethod
    def get_anime_list_by_user_id(user):
        anime_list = AnimeListEntry.objects.filter(user=user)
        return anime_list
    
    @staticmethod
    def get_anime_list_entry(user, anime):
        try:
            return AnimeListEntry.objects.get(user=user, anime=anime)
        except AnimeListEntry.DoesNotExist:
            return None