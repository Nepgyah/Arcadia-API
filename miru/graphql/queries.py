import strawberry

from .types import AnimeType

@strawberry.type
class MiruQuery:

    @strawberry.field
    def anime(self, pk: int) -> AnimeType:
        return None