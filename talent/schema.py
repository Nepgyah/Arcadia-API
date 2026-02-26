import graphene
from graphene_django import DjangoObjectType
from .models import (
    Character
)

class CharacterType(DjangoObjectType):

    class Meta:
        model = Character
        fields = "__all__"

class Query(graphene.ObjectType):

    character_by_id = graphene.Field(CharacterType, id=graphene.Int(required=True))

    def resolve_character_by_id(self, info, id):
        return Character.objects.get(id=1)