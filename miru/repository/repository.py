import logging
from miru.models import (
    Anime, 
    AnimeCharacter,
    AniListData,
    MyAnimeListData,
    AnimeEpisode,
    AnimeCompany,
    AnimeListEntry,
    AnimeReview,
    FavoriteAnime,
    CustomAnimeList
)
from miru.exceptions import MiruNotFoundError, MiruError, MiruValidationError
from miru.serializer.serializers import AnimeListEntrySerializer, AnimeReviewSerializer, CustomAnimeListSerializer

logger = logging.getLogger(__name__)

class AnimeModule:
    
    @staticmethod
    def get_anime_count() -> int:
        return Anime.objects.count()

    @staticmethod
    def get_anime(anime_id: int) -> Anime:
        try:
            return Anime.objects.get(id=anime_id)
        except Anime.DoesNotExist:
            raise MiruNotFoundError(
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
            raise MiruNotFoundError(
                detail="Cannot find requested anilist data",
                code="miru_anilist_data_not_found"
            ) from None
        
    @staticmethod
    def get_mal_data(anime_id: int) -> MyAnimeListData:
        try:
            return MyAnimeListData.objects.get(anime_id=anime_id)
        except MyAnimeListData.DoesNotExist:
            raise MiruNotFoundError(
                detail="Cannot find requested MAL data",
                code="miru_mal_data_not_found"
            ) from None
        
    @staticmethod
    def get_episodes(anime_id: int) -> list[AnimeEpisode]:
        return AnimeEpisode.objects.filter(anime_id=anime_id)
    
class EpisodeModule:
    
    @staticmethod
    def get_episode(episode_id: int) -> AnimeEpisode:
        try:
            return AnimeEpisode.objects.get(id=episode_id)
        except AnimeEpisode.DoesNotExist:
            raise MiruNotFoundError(
                detail="Cannot find requested anime episode",
                code="miru_episode_not_found"
            ) from None

class CompanyModule:

    @staticmethod
    def get_company(company_id: int) -> AnimeCompany:
        try:
            AnimeCompany.objects.get(id=company_id)
        except AnimeCompany.DoesNotExist:
            raise MiruNotFoundError(
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
    
class ListModule:

    @staticmethod
    def create_entry(profile_id: int, anime_id: int, **details: dict) -> AnimeListEntry:
        data = {
            'profile_id': profile_id,
            'anime': anime_id,
            **details
        }

        serializer = AnimeListEntrySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()
    
    @staticmethod
    def get_entry(profile_id: int, anime_id: int) -> AnimeListEntry:
        try:
            return AnimeListEntry.objects.get(profile_id=profile_id, anime_id=anime_id)
        except AnimeListEntry.DoesNotExist:
            raise MiruNotFoundError(
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
    def get_user_list(profile_id: int) -> list[AnimeListEntry]:
        return AnimeListEntry.objects.filter(profile_id=profile_id)
    
    @staticmethod
    def get_user_list_count(profile_id: int) -> int:
        return AnimeListEntry.objects.filter(profile_id=profile_id).count()
    
    @staticmethod
    def get_custom_anime_list(profile_id: int, list_id: int) -> CustomAnimeList:
        try:
            return CustomAnimeList.objects.prefetch_related('anime').get(id=list_id, profile_id=profile_id)
        except CustomAnimeList.DoesNotExist:
            logger.info('Attempt to find custom anime list with id: %s', list_id)
            raise MiruNotFoundError('Cannot find anime list') from None

    @staticmethod
    def create_custom_anime_list(**data: dict) -> None:
        serializer = CustomAnimeListSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def update_custom_anime_list_details(custom_list: CustomAnimeList, **data: dict) -> CustomAnimeList:
        serializer = CustomAnimeListSerializer(
            custom_list, 
            data=data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def delete_custom_anime_list(custom_list: CustomAnimeList) -> None:
        custom_list.delete()

    @staticmethod
    def add_to_custom_anime_list(target_list: CustomAnimeList, anime: Anime) -> None:
        target_list.anime.add(anime)

    @staticmethod
    def remove_from_custom_anime_list(target_list: CustomAnimeList, anime: Anime) -> None:
        try:
            target_list.anime.remove(anime)
        except Exception as e:
            raise MiruError('An error occured removing the anime') from e

class ReviewModule:
    
    @staticmethod
    def get_review(profile_id: int, anime_id: int) -> AnimeReview | None:
        try:
            return AnimeReview.objects.get(
                profile_id=profile_id,
                anime_id=anime_id
            )
        except AnimeReview.DoesNotExist:
            return None

    @staticmethod
    def create(profile_id: int, anime_id: int, **details: dict) -> AnimeReview:
        data = {
            'profile_id': profile_id,
            'anime': anime_id,
            **details
        }

        serializer = AnimeReviewSerializer(data=data)
        if not serializer.is_valid():
            errors = serializer.errors["non_field_errors"]
            if errors[0].code == "unique":
                raise MiruValidationError('Review already exists')
            raise MiruError()
        
        return serializer.save()
    
    @staticmethod
    def update(review: AnimeReview, **data: dict) -> AnimeReview:
        serializer = AnimeReviewSerializer(
            review, 
            data=data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        return serializer.save()
    
    @staticmethod
    def delete(review: AnimeReview) -> AnimeReview:
        try:
            review.delete()
        except Exception as e:
            raise MiruError() from e

class FavoriteModule:

    @staticmethod
    def add_favorite_anime(profile_id: int, anime: Anime) -> None:
        try:
            FavoriteAnime.objects.create(
                profile_id=profile_id,
                anime=anime
            )
        except Exception as e:
            raise MiruValidationError('You have already favorited this anime') from e
    
    @staticmethod
    def remove_favorite_anime(profile_id: int, anime: Anime) -> None:
        try:
            favorite_target = FavoriteAnime.objects.get(
                profile_id=profile_id,
                anime=anime
            )
            favorite_target.delete()
        except FavoriteAnime.DoesNotExist:
            raise MiruValidationError('Could not find anime to remove from favorites') from None
        
    @staticmethod
    def get_favorite_anime(profile_id: int) -> list[FavoriteAnime]:
        return FavoriteAnime.objects.filter(profile_id=profile_id)
    
class MiruRepository:

    anime = AnimeModule()
    episode = EpisodeModule()
    company = CompanyModule()
    list = ListModule()
    review = ReviewModule()
    favorite = FavoriteModule()