from miru.models import (
    Anime, 
    AnimeCharacter,
    AniListData,
    MyAnimeListData,
    AnimeEpisode,
    AnimeCompany,
    AnimeListEntry
)
from miru.exceptions import MiruNotFound, MiruError
from miru.serializers import AnimeListEntrySerializer

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
    def get_characters(anime_id: int) -> list[AnimeCharacter]:
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

class CompanyRepository:

    @staticmethod
    def get_company(company_id: int) -> AnimeCompany:
        try:
            AnimeCompany.objects.get(id=company_id)
        except AnimeCompany.DoesNotExist:
            raise MiruNotFound(
                detail="Cannot find requested anime company",
                code="miru_anime_company_not_found"
            ) from None

    @staticmethod
    def get_companies(company_id_list: list[int]) -> list[AnimeCompany]:
        return AnimeCompany.objects.filter(id__in=company_id_list)

    @staticmethod
    def get_producers() -> list[AnimeCompany]:
        return AnimeCompany.objects.filter(produced_animes__isnull=False).distinct()
    
    @staticmethod
    def get_studios() -> list[AnimeCharacter]:
        return AnimeCompany.objects.filter(studio_animes__isnull=False).distinct()
    
class AnimeListEntryRepository:

    @staticmethod
    def create_entry(user_id: int, anime_id: int, **details: dict) -> AnimeListEntry:
        data = {
            'user': user_id,
            'anime': anime_id,
            **details
        }

        serializer = AnimeListEntrySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()
    
    @staticmethod
    def get_entry(user_id: int, anime_id: int) -> AnimeListEntry:
        try:
            AnimeListEntry.objects.get(user_id=user_id, anime_id=anime_id)
        except AnimeListEntry.DoesNotExist:
            raise MiruNotFound(
                detail="Cannot find requested anime list entry",
                code="miru_anime_list_entry_not_found"
            ) from None
        
    @staticmethod
    def update_entry(entry: AnimeListEntry, **data: dict) -> AnimeListEntry:
        serializer = AnimeListEntrySerializer(
            entry, 
            data=data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        return serializer.save()
    
    @staticmethod
    def delete_entry(entry: AnimeListEntry) -> AnimeListEntry:
        try:
            entry.delete()
        except Exception as e:
            raise MiruError() from e

    @staticmethod
    def get_user_list(user_id: int) -> list[AnimeListEntry]:
        return AnimeListEntry.objects.filter(user_id=user_id)
    
class MiruRepository:

    anime = AnimeRepository()
    episode = EpisodeRepository()
    company = CompanyRepository()