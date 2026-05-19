import strawberry
import strawberry_django
from strawberry_django.optimizer import optimize
from miru.models import Anime
from .types import AnimeType

@strawberry.type
class MiruQuery:
    
    @strawberry_django.field
    def anime(self, info: strawberry.Info, pk: int) -> AnimeType:
        qs = Anime.objects.filter(id=pk)
        qs = optimize(qs, info)
        return qs.get()
    