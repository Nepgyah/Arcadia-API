import strawberry
import strawberry_django
from base.service import FranchiseService
from base.graphql.types import FranchiseType
from talent.graphql.types import CharacterType, VoiceActorType

from miru.models import Anime, AnimeCompany, AnimeCharacter
from miru.service import MiruService

@strawberry_django.type(
    AnimeCompany,
    fields="__all__"
)
class AnimeCompanyType:
    pass

@strawberry.type
class AnimeCharacterType:
    character: CharacterType
    role: str
    voice_actor: VoiceActorType | None

@strawberry_django.type(
    Anime, 
    exclude=['characters'],
    description="アニメ"
)
class AnimeType:
    franchise : FranchiseType | None
    studio: list[AnimeCompanyType]
    producer: list[AnimeCompanyType]

    @strawberry_django.field
    def cast(self) -> list[AnimeCharacterType]:
        characters = MiruService.anime.get_cast(self.id)
        return [
            AnimeCharacterType(
                character=character['character'],
                role=character['role'],
                voice_actor=character['voice_actor']
            )
            for character in characters
        ]
