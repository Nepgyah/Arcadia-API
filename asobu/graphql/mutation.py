import strawberry
import strawberry_django
# from .types import GameListEntryType

@strawberry.input
class GameListDetails:
    status: int | None
    score: int | None
    note: str | None
    start_play_date: str | None
    end_play_date: str | None

@strawberry.type
class AsobuMutation:

    @strawberry.mutation
    def add_to_game_list(self, info: strawberry.Info, game_id: int, details: GameListDetails | None = None) -> str:
        return str(info.context.request.user)
