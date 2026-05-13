import strawberry_django
from strawberry import auto
from asobu.models import Game


@strawberry_django.type(Game)
class GameType:
    id: auto
    title: auto
    score: auto
    users: auto
    slug: auto
    created_at: auto
    updated_at: auto
    bg_image_path: auto
    status: auto