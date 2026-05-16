import strawberry
from main.graphql.types import PaginationResultsType, SortInput, PaginationInput
from main.graphql.permissions import IsAuthenticated
from asobu.graphql.types import (
    GameType,
    DLCType,
    GameReviewType
)
from asobu.service.asobu_service import AsobuService

@strawberry.input
class GameFilterInput:
    title: str | None = ""
    type: int | None = -1
    status: int | None = -1

@strawberry.type
class SearchGamesResult:
    results: list[GameType]
    pagination: PaginationResultsType

@strawberry.type
class AsobuQuery:

    @strawberry.field
    def game(self, pk: int) -> GameType:
        return AsobuService.game.get_game(game_id=pk)
    
    @strawberry.field
    def games(
        self, 
        filters: GameFilterInput | None = None, 
        sort: SortInput | None = None, 
        pagination: PaginationInput | None = None
    ) -> SearchGamesResult:
        
        if filters is not None:
            filters = strawberry.asdict(filters)
        
        if sort is not None:
            sort = strawberry.asdict(sort)

        if pagination is not None:
            pagination = strawberry.asdict(pagination)

        games, pagination_results = AsobuService.game.search_games(
            filters,
            sort,
            pagination
        )

        return SearchGamesResult(
            results=games,
            pagination=pagination_results
        )
    
    @strawberry.field
    def dlcs(self, game_pk: int) -> list[DLCType]:
        return AsobuService.game.get_dlc(game_id=game_pk)
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    def game_review(self, info: strawberry.Info, game_id: int) -> GameReviewType:
        return AsobuService.review.get_review(
            info.context.user_id,
            game_id
        )