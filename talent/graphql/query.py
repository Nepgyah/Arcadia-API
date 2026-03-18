import graphene

from asobu.graphql.schema import GameCharacterType
from miru.graphql.schema import AnimeCharacterType
from talent.service.character import CharacterService
from talent.service.voice_actor import VoiceActorService

from .schema import (
    CharacterType,
    VoiceActorType
)

class VoiceActorResults(graphene.ObjectType):
    voice_actor = graphene.Field(VoiceActorType)
    related_anime = graphene.List(AnimeCharacterType)
    related_games = graphene.List(GameCharacterType)

class Query(graphene.ObjectType):

    character_by_id = graphene.Field(CharacterType, character_id=graphene.Int(required=True))
    voice_actor_by_id = graphene.Field(VoiceActorResults, va_id=graphene.ID(required=True))

    def resolve_character_by_id(self, _info, character_id):
        return CharacterService.get_character_by_id(character_id)
    
    def resolve_voice_actor_by_id(self, _info, va_id):
        voice_actor, characters =  VoiceActorService.get_voice_actor_by_id(va_id, True)

        related_anime = characters['animes']
        related_games = characters['games']

        return VoiceActorResults(
            voice_actor = voice_actor,
            related_anime = related_anime,
            related_games = related_games
        )