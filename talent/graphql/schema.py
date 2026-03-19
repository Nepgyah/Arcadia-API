import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from talent.models import (
    Character,
    VoiceActor
)
from talent.service.voice_actor import VoiceActorService

class VoiceActorType(DjangoObjectType):
    characters = graphene.List(lambda: CharacterType)
    socials = GenericScalar()

    class Meta:
        model = VoiceActor
        fields = "__all__"

    def resolve_characters(self, _info):
        return self.characters.all()

class CharacterType(DjangoObjectType):
    voice_actor = graphene.Field(VoiceActorType)
    full_name = graphene.String()

    class Meta:
        model = Character
        fields = "__all__"

    def resolve_voice_actor(self, _info):
        return VoiceActorService.get_voice_actor_by_id(self.voice_actor.id)
    
    def resolve_full_name(self, _info):
        return self.full_name