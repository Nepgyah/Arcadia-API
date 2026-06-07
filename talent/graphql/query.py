import strawberry
from talent.graphql.types import VoiceActorType, CharacterType
from talent.service import VoiceActorService, CharacterService

@strawberry.type
class TalentQuery:

    @strawberry.field
    def voice_actor(self, pk: int) -> VoiceActorType:
        return VoiceActorService.get_voice_actor(pk)
    
    @strawberry.field
    def character(self, pk: int) -> CharacterType:
        return CharacterService.get_character_by_id(pk)