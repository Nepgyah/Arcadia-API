import graphene

from .schema import (
    CharacterType,
    VoiceActorType
)

from talent.service.character import CharacterService
from talent.service.voice_actor import VoiceActorService

class Query(graphene.ObjectType):

    character_by_id = graphene.Field(CharacterType, id=graphene.Int(required=True))
    voice_actor_by_id = graphene.Field(VoiceActorType, id=graphene.ID(required=True))

    def resolve_character_by_id(self, info, id):
        return CharacterService.get_character_by_id(id)
    
    def resolve_voice_actor_by_id(self, info, id):
        return VoiceActorService.get_voice_actor_by_id(id)