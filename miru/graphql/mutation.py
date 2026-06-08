import strawberry
from main.graphql.types import MutationResponseType
from main.graphql.permissions import IsAuthenticated
from miru.service import MiruService
from miru.graphql.types import AnimeListEntryType

@strawberry.input
class AnimeListDetails:
    status: int | None = 0
    score: int | None = None
    current_episode: int | None = 0
    start_watch_date: str | None = None
    end_watch_date: str | None = None

@strawberry.type
class AnimeListResponseType(MutationResponseType):
    entry: AnimeListEntryType | None

@strawberry.type
class MiruMutation:

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
    