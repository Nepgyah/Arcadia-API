import strawberry
import strawberry_django
# from .types import GameListEntryType

@strawberry_django.type
class AsobuMutation:

    @strawberry_django.mutation
    def add_to_game_list(self, info: strawberry.Info, game_id: int, details: dict) -> str:
        return str(info.context.request.user)
