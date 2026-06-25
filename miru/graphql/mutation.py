import strawberry
from main.graphql.types import MutationResponseType
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

@strawberry.type
class AnimeListResponseType(MutationResponseType):
    entry: AnimeListEntryType | None

@strawberry.type
class AnimeReviewResponseType(MutationResponseType):
    entry: AnimeReviewType | None

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
    def create_anime_review(self, info: strawberry.Info, anime_id: int, details: AnimeListDetails | None = None) -> AnimeReviewResponseType:
        if details is None:
            details_dict = {}
        else:
            details_dict = strawberry.asdict(details)

        entry = MiruService.review.create(
            info.context.user_id,
            anime_id=anime_id,
            details=details_dict
        )

        return AnimeReviewResponseType(
            entry=entry,
            message="Anime review added",
            detail="miru_anime_review_created"
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_anime_review(self, info: strawberry.Info, anime_id: int, details: AnimeListDetails | None = None) -> AnimeReviewResponseType:
        if details is None:
            details_dict = {}
        else:
            details_dict = strawberry.asdict(details)

        entry = MiruService.review.update(
            info.context.user_id,
            anime_id=anime_id,
            details=details_dict
        )

        return AnimeReviewResponseType(
            entry=entry,
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
            entry=None,
            message="Anime review deleted",
            detail="miru_anime_review_deleted"
        )
    