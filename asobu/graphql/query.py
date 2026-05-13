import strawberry
import strawberry_django
from asobu.graphql.types import GameType
from asobu.service.asobu_service import AsobuService

@strawberry.type
class AsobuQuery:

    @strawberry_django.field
    def game(self, pk: int) -> GameType:
        return AsobuService.game.get_game(game_id=pk)