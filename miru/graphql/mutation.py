import strawberry
from base.graphql.inputs import MediaReviewInput
from main.graphql.types import MutationResponseType, BaseMutationResponse
from main.graphql.permissions import IsAuthenticated
from miru.service import MiruService
from miru.graphql.types import AnimeListEntryType, AnimeReviewType

@strawberry.input
class AnimeListDetails:
    status: int | None = 0
    current_episode: int | None = 0
    start_watch_date: str | None = None
    note: str | None = None
    end_watch_date: str | None = None

@strawberry.input
class CustomAnimeListDetailsInput:
    title: str | None = None
    description: str | None = None

@strawberry.type
class AnimeListResponseType(MutationResponseType):
    entry: AnimeListEntryType | None

@strawberry.type
class AnimeReviewResponseType(MutationResponseType):
    review: AnimeReviewType | None

@strawberry.type
class MiruFavoriteResponseType(MutationResponseType):
    pass

@strawberry.type
class MiruMutation:

    # List Entries
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_anime_list_entry(self, info: strawberry.Info, anime_id: int, details: AnimeListDetails | None = None) -> AnimeListResponseType:
        if details is None:
            details_dict = {}
        else:
            details_dict = strawberry.asdict(details)

        entry = MiruService.list.create_entry(
            info.context.user_id,
            anime_id=anime_id,
            details=details_dict
        )

        return AnimeListResponseType(
            entry=entry,
            message="Anime entry added",
            detail="miru_anime_entry_created"
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_anime_list_entry(self, info: strawberry.Info, anime_id: int, details: AnimeListDetails | None = None) -> AnimeListResponseType:
        if details is None:
            details_dict = {}
        else:
            details_dict = strawberry.asdict(details)

        entry = MiruService.list.update_entry(
            info.context.user_id,
            anime_id=anime_id,
            details=details_dict
        )

        return AnimeListResponseType(
            entry=entry,
            message="Anime entry updated",
            detail="miru_anime_entry_updated"
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def delete_anime_list_entry(self, info: strawberry.Info, anime_id: int) -> AnimeListResponseType:
        MiruService.list.delete_entry(
            info.context.user_id,
            anime_id=anime_id,
        )

        return AnimeListResponseType(
            entry=None,
            message="Anime entry deleted",
            detail="miru_anime_entry_deleted"
        )
    
    ## Reviews
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_anime_review(self, info: strawberry.Info, anime_id: int, details: MediaReviewInput | None = None) -> AnimeReviewResponseType:
        if details is None:
            details_dict = {}
        else:
            details_dict = strawberry.asdict(details)

        review = MiruService.review.create(
            info.context.user_id,
            anime_id=anime_id,
            details=details_dict
        )

        return AnimeReviewResponseType(
            review=review,
            message="Anime review added",
            detail="miru_anime_review_created"
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_anime_review(self, info: strawberry.Info, anime_id: int, details: MediaReviewInput | None = None) -> AnimeReviewResponseType:
        if details is None:
            details_dict = {}
        else:
            details_dict = strawberry.asdict(details)

        review = MiruService.review.update(
            info.context.user_id,
            anime_id=anime_id,
            details=details_dict
        )

        return AnimeReviewResponseType(
            review=review,
            message="Anime review updated",
            detail="miru_anime_review_updated"
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def delete_anime_review(self, info: strawberry.Info, anime_id: int) -> AnimeReviewResponseType:
        MiruService.review.delete(
            info.context.user_id,
            anime_id=anime_id,
        )

        return AnimeReviewResponseType(
            review=None,
            message="Anime review deleted",
            detail="miru_anime_review_deleted"
        )
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def add_favorite_anime(self, info: strawberry.Info, anime_id: int) -> MiruFavoriteResponseType:
        MiruService.favorite.add_favorite_anime(info.context.user_id, anime_id)
        return MutationResponseType(
            message="You favorited an anime",
            detail="miru_anime_favorited"
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def remove_favorite_anime(self, info: strawberry.Info, anime_id: int) -> MiruFavoriteResponseType:
        MiruService.favorite.remove_favorite_anime(info.context.user_id, anime_id)
        return MutationResponseType(
            message="You unfavorited an anime",
            detail="miru_anime_unfavorited"
        )
    
    # Custom Anime List
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_custom_anime_list(self, info: strawberry.Info, details: CustomAnimeListDetailsInput) -> BaseMutationResponse:
        details_dict = strawberry.asdict(details)
        MiruService.list.create_custom_anime_list(info.context.user_id, details_dict)

        return BaseMutationResponse(
            message="You created a custom anime list",
            detail="miru_custom_anime_list_created"
        )
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_custom_anime_list(self, info: strawberry.Info, list_id: int, details: CustomAnimeListDetailsInput) -> BaseMutationResponse:
        details_dict = strawberry.asdict(details)
        MiruService.list.update_custom_anime_list_details(info.context.user_id, list_id, details_dict)

        return BaseMutationResponse(
            message="You updated a custom anime list",
            detail="miru_custom_anime_list_updated"
        )
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def delete_custom_anime_list(self, info: strawberry.Info, list_id: int) -> BaseMutationResponse:
        MiruService.list.delete_custom_anime_list(info.context.user_id, list_id)
        
        return BaseMutationResponse(
            message="You deleted a custom anime list",
            detail="miru_custom_anime_list_deleted"
        )
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def add_to_custom_anime_list(self, info: strawberry.Info, list_id: int, anime_id: int) -> BaseMutationResponse:
        MiruService.list.add_to_custom_anime_list(info.context.user_id, list_id, anime_id)

        return BaseMutationResponse(
            message="You added an anime to your list",
            detail="miru_custom_anime_list_anime_added"
        )
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def remove_from_custom_anime_list(self, info: strawberry.Info, list_id: int, anime_id: int) -> BaseMutationResponse:
        MiruService.list.remove_from_custom_anime_list(info.context.user_id, list_id, anime_id)

        return BaseMutationResponse(
            message="You removed an anime to your list",
            detail="miru_custom_anime_list_anime_removed"
        )