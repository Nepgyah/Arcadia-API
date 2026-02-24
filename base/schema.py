import graphene
from graphene_django import DjangoObjectType
from .models import (
    Franchise,
    Genre
)
from miru.models import Anime
from base.repository.franchise_repository import FranchiseRepository
from base.service.franchise_service import FranchiseService

class FranchiseType(DjangoObjectType):

    class Meta:
        model = Franchise
        fields = '__all__'

class GenreType(DjangoObjectType):

    class Meta:
        model = Genre
        fields = "__all__"

class Query(graphene.ObjectType):

    franchise_by_id = graphene.Field(FranchiseType, id=graphene.Int(required=True))
    franchise_by_anime = graphene.Field(FranchiseType, id=graphene.Int(required=True))

    def resolve_franchise_by_id(self, info, id):
        return FranchiseRepository.get_franchise_by_id(id)
    
    def resolve_franchise_by_anime(self, info, id):
        return FranchiseService.get_franchise_by_anime(id)