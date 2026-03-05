import graphene
from graphene_django import DjangoObjectType
from talent.models import (
    Character,
    VoiceActor
)
from talent.service.voice_actor import VoiceActorService

class VoiceActorType(DjangoObjectType):
    characters = graphene.List(lambda: CharacterType)

    class Meta:
        model = VoiceActor
        fields = "__all__"

    def resolve_characters(self, info):
        return self.characters.all()

class CharacterType(DjangoObjectType):
    voice_actor = graphene.Field(VoiceActorType)

    class Meta:
        model = Character
        fields = "__all__"

    def resolve_voice_actor(self, info):
        if (self.voice_actor):
            return VoiceActorService.get_voice_actor_by_id(self.voice_actor.id)
        return None