from typing import List
import strawberry_django
from talent.models import Character, VoiceActor
from talent.service import VoiceActorService

@strawberry_django.type
class AnimeRole:
    character: "CharacterType"
    anime: "AnimeType"

@strawberry_django.type(VoiceActor, fields="__all__")
class VoiceActorType:

    @strawberry_django.field
    def full_name(self) -> str:
        return self.full_name

    @strawberry_django.field
    def characters(self) -> List["CharacterType"]:
        return self.characters.all()

@strawberry_django.type(
    Character, 
    exclude=["voice_actor"]
)
class CharacterType:
    voice_actor: VoiceActorType = strawberry_django.field(field_name="voice_actor")

    @strawberry_django.field
    def full_name(self) -> str:
        return self.full_name
