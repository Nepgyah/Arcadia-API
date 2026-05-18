from miru.models import (
    Anime, 
    AnimeCharacter,
    AniListData,
    MyAnimeListData,
    AnimeEpisode
)
from miru.exceptions import MiruNotFound

class AnimeRepository:
    
    @staticmethod
    def get_anime(anime_id: int) -> Anime:
        try:
            return Anime.objects.get(id=anime_id)
        except Anime.DoesNotExist:
            raise MiruNotFound(
                detail="Cannot find requested anime",
                code="miru_anime_not_found"
            ) from None

    @staticmethod
    def does_anime_exist(anime_id: int) -> bool:
        return Anime.objects.filter(id=anime_id).exists()

    @staticmethod
    def get_character(anime_id: int) -> list[AnimeCharacter]:
        return AnimeCharacter.objects.filter(anime_id=anime_id)
    
    @staticmethod
    def get_anilist_data(anime_id: int) -> AniListData:
        try:
            return AniListData.objects.get(anime_id=anime_id)
        except AniListData.DoesNotExist:
            raise MiruNotFound(
                detail="Cannot find requested anilist data",
                code="miru_anilist_data_not_found"
            ) from None
        
    @staticmethod
    def get_mal_data(anime_id: int) -> MyAnimeListData:
        try:
            return MyAnimeListData.objects.get(anime_id=anime_id)
        except MyAnimeListData.DoesNotExist:
            raise MiruNotFound(
                detail="Cannot find requested MAL data",
                code="miru_mal_data_not_found"
            ) from None
        
    @staticmethod
    def get_episodes(anime_id: int) -> list[AnimeEpisode]:
        return AnimeEpisode.objects.filter(anime_id=anime_id)
    
class EpisodeRepository:
    
    @staticmethod
    def get_episode(episode_id: int) -> AnimeEpisode:
        try:
            return AnimeEpisode.objects.get(id=episode_id)
        except AnimeEpisode.DoesNotExist:
            raise MiruNotFound(
                detail="Cannot find requested anime episode",
                code="miru_episode_not_found"
            ) from None

class MiruRepository:

    anime = AnimeRepository()
    episode = EpisodeRepository()