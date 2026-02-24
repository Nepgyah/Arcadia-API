import graphene
from graphene_django import DjangoObjectType
from miru.models import (
    Anime,
    AnimeCharacter
)
from characters.schema import CharacterType
from base.schema import GenreType

class AnimeCharacterType(DjangoObjectType):
    character = graphene.Field(CharacterType)
    role = graphene.String()

    class Meta:
        model = AnimeCharacter
        fields = "__all__"

    def resolve_role(self, info):
        return self.get_role_display()
    
class AnimeType(DjangoObjectType):
    status = graphene.String()
    type = graphene.String()
    rating = graphene.String()
    season = graphene.String()
    genres = graphene.List(GenreType)
    characters = graphene.List(AnimeCharacterType)

    class Meta:
        model = Anime
        fields = "__all__"

    def resolve_rating(self, info):
        return self.get_rating_display()
    
    def resolve_type(self, info):
        return self.get_type_display()
    
    def resolve_status(self, info):
        return self.get_status_display()
    
    def resolve_season(self, info):
        if self.season:
            return str(self.season)
        else:
            return 'N/A'
    
    def resolve_genres(self, info):
        return self.genres.all()
    
    def resolve_characters(self, info):
        return AnimeCharacter.objects.filter(anime=self)
    