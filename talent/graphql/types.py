from typing import List
import strawberry_django
from talent.models import Character, VoiceActor

@strawberry_django.type(VoiceActor, fields="__all__")
class VoiceActorType:

    @strawberry_django.field
    def full_name(self) -> str:
        return self.full_name

    @strawberry_django.field
    def roles(self) -> List["CharacterType"]:
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
