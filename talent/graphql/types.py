import strawberry
import strawberry_django

from talent.models import Character, VoiceActor

@strawberry_django.type(VoiceActor, fields="__all__")
class VoiceActorType:
    pass

@strawberry_django.type(Character, fields="__all__")
class CharacterType:
    pass
