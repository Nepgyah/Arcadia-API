from strawberry import auto
import strawberry_django

from miru.models import Anime
@strawberry_django.type(
    Anime, 
    exclude=['characters'],
    description="アニメ"
)
class AnimeType:
    pass