import strawberry_django
from strawberry import auto, ID
from base.models import Franchise, Genre

@strawberry_django.type(Franchise)
class FranchiseType:
    id: ID
    name: auto
    slug: auto
    socials: auto

    @strawberry_django.field
    def cover_image(self) -> str:
        return self.cover_image_url

@strawberry_django.type(Genre)
class GenreType:
    id: ID
    name: auto