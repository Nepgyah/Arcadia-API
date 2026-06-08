import strawberry
import strawberry_django
from talent.graphql.types import VoiceActorType, CharacterType
from talent.service import VoiceActorService, CharacterService

@strawberry.type
class TalentQuery:

    @strawberry_django.field
    def voice_actor(self, pk: int) -> VoiceActorType:
        return VoiceActorService.get_voice_actor(pk)
    
    @strawberry_django.field
    def voice_actors(self, name: str) -> list[VoiceActorType]:
        return VoiceActorService.search_voice_actor(name)

    @strawberry_django.field
    def character(self, pk: int) -> CharacterType:
        return CharacterService.get_character(pk)
    
    @strawberry_django.field
    def characters(self, name: str) -> list[CharacterType]:
        return CharacterService.search_characters(name)