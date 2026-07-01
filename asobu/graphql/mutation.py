import strawberry
from base.graphql.response import MutationResponseType
from main.graphql.permissions import IsAuthenticated
from asobu.service import AsobuService
from asobu.graphql.types import GameListEntryType, GameReviewType

@strawberry.input
class GameListDetails:
    status: int | None = 0
    score: int | None = None
    note: str | None = None
    start_play_date: str | None = None
    end_play_date: str | None = None

@strawberry.type
class GameListResponseType(MutationResponseType):
    entry: GameListEntryType | None

@strawberry.type
class GameReviewResponseType(MutationResponseType):
    review: GameReviewType | None

@strawberry.type
class AsobuMutation:

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_game_list_entry(self, info: strawberry.Info, game_id: int, details: GameListDetails | None = None) -> GameListResponseType:
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
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
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

    @strawberry.mutation(permission_classes=[IsAuthenticated])
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
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_game_review(self, info: strawberry.Info, game_id: int, text: str) -> GameReviewResponseType:
        review = AsobuService.review.create_review(
            info.context.user_id,
            game_id,
            text
        )

        return GameReviewResponseType(
            message="Review created",
            detail="asobu_game_review_created",
            review=review
        )
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_game_review(self, info: strawberry.Info, game_id: int, text: str) -> GameReviewResponseType:
        review = AsobuService.review.update_review(
            info.context.user_id,
            game_id,
            text
        )
        
        return GameReviewResponseType(
            message="Review updated",
            detail="asobu_game_review_update",
            review=review
        )
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def delete_game_review(self, info: strawberry.Info, game_id: int) -> None:
        AsobuService.review.delete_review(
            info.context.user_id,
            game_id,
        )

        return GameReviewResponseType(
            message="Review deleted",
            detail="asobu_game_review_deleted",
            review=None
        )
