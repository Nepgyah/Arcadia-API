import graphene
from graphene_django import DjangoObjectType
from .models import (
    Character,
    VoiceActor
)
from talent.service.voice_actor_service import VoiceActorService

class VoiceActorType(DjangoObjectType):

    class Meta:
        model = VoiceActor
        fields = "__all__"

class CharacterType(DjangoObjectType):
    voice_actor = graphene.Field(VoiceActorType)

    class Meta:
        model = Character
        fields = "__all__"

    def resolve_voice_actor(self, info):
        if (self.voice_actor):
            return VoiceActorService.get_voice_actor_by_id(self.voice_actor.id)
        return None

class Query(graphene.ObjectType):

    character_by_id = graphene.Field(CharacterType, id=graphene.Int(required=True))

    def resolve_character_by_id(self, info, id):
        return Character.objects.get(id=1)