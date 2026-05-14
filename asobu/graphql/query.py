import strawberry
import strawberry_django
from asobu.graphql.types import GameType
from asobu.service.asobu_service import AsobuService

@strawberry.type
class AsobuQuery:

    @strawberry_django.field
    def game(self, info: strawberry.Info, pk: int) -> GameType:
        print(info.context.get("user_id"))
        return AsobuService.game.get_game(game_id=pk)