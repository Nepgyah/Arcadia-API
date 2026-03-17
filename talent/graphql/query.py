import graphene

from .schema import (
    CharacterType,
    VoiceActorType
)
from asobu.graphql.schema import GameCharacterType
from miru.graphql.schema import AnimeCharacterType
from talent.service.character import CharacterService
from talent.service.voice_actor import VoiceActorService

class VoiceActorResults(graphene.ObjectType):
    voice_actor = graphene.Field(VoiceActorType)
    related_anime = graphene.List(AnimeCharacterType)
    related_games = graphene.List(GameCharacterType)

class Query(graphene.ObjectType):

    character_by_id = graphene.Field(CharacterType, id=graphene.Int(required=True))
    voice_actor_by_id = graphene.Field(VoiceActorResults, id=graphene.ID(required=True))

    def resolve_character_by_id(self, info, id):
        return CharacterService.get_character_by_id(id)
    
    def resolve_voice_actor_by_id(self, info, id):
        voice_actor, characters =  VoiceActorService.get_voice_actor_by_id(id, True)

        related_anime = characters['animes']
        related_games = characters['games']

        return VoiceActorResults(
            voice_actor = voice_actor,
            related_anime = related_anime,
            related_games = related_games
        )