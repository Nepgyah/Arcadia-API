import strawberry_django

from talent.models import Character, VoiceActor

@strawberry_django.type(VoiceActor, fields="__all__")
class VoiceActorType:

    @strawberry_django.field
    def full_name(self) -> str:
        return self.full_name

@strawberry_django.type(Character, fields="__all__")
class CharacterType:
    
    @strawberry_django.field
    def full_name(self) -> str:
        return self.full_name
