import strawberry
import strawberry_django
from strawberry import auto
from asobu.models import Game
from base.models import Franchise
from base.graphql.types import FranchiseType

@strawberry_django.type(Game, description="Video games from the asobu app")
class GameType:
    id: auto
    title: auto
    score: auto
    users: auto
    slug: auto
    created_at: auto
    updated_at: auto
    bg_image_path: auto
    status: strawberry.auto

    @strawberry_django.field
    def franchise(self) -> FranchiseType:
        return Franchise.objects.get(id=self.franchise.id)