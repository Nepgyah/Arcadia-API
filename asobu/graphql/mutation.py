import strawberry
from main.graphql.types import MutationResponseType
from asobu.service import AsobuService
from asobu.graphql.types import GameListEntryType

@strawberry.input
class GameListDetails:
    status: int | None = 1
    score: int | None = None
    note: str | None = None
    start_play_date: str | None = None
    end_play_date: str | None = None

@strawberry.type
class GameListResponseType(MutationResponseType):
    entry: GameListEntryType | None

@strawberry.type
class AsobuMutation:

    @strawberry.mutation
    def add_game_list_entry(self, info: strawberry.Info, game_id: int, details: GameListDetails | None = None) -> GameListResponseType:
        if details is None:
            details_dict = {}
        else:
            details_dict = strawberry.asdict(details)

        entry = AsobuService.list.create_entry(
            info.context.user_id,
            game_id=game_id,
            details=details_dict
        )
        return GameListResponseType(
            message="Game entry added",
            detail="asobu_game_entry_created",
            entry=entry
        )
    
    @strawberry.mutation
    def update_game_list_entry(self, info: strawberry.Info, game_id: int, details: GameListDetails | None = None) -> GameListResponseType:
        if details is None:
            details_dict = {}
        else:
            details_dict = strawberry.asdict(details)

        entry = AsobuService.list.update_entry(
            info.context.user_id,
            game_id=game_id,
            details=details_dict
        )
        return GameListResponseType(
            message="Game entry updated",
            detail="asobu_game_entry_update",
            entry=entry
        )

    @strawberry.mutation
    def delete_game_list_entry(self, info: strawberry.Info, game_id: int) -> GameListResponseType:
        AsobuService.list.delete_entry(
            user_id=info.context.user_id,
            game_id=game_id
        )
        return GameListResponseType(
            message="Game entry deleted",
            detail="asobu_game_entry_deleted",
            entry=None
        )