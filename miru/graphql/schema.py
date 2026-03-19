import graphene
from graphene_django import DjangoObjectType
from miru.models.anime import Anime
from miru.models.misc import AnimeCompany
from miru.models.relations import (
    AnimeCharacter,
    AnimeEpisode,
    RelatedAnime
)
from miru.models.list_entry import AnimeListEntry
from talent.graphql.schema import CharacterType
from base.schema import GenreType

class AnimeCompanyType(DjangoObjectType):

    class Meta:
        model = AnimeCompany
        fields = "__all__"

class AnimeCharacterType(DjangoObjectType):
    character = graphene.Field(CharacterType)
    role = graphene.String()

    class Meta:
        model = AnimeCharacter
        fields = "__all__"

    def resolve_role(self, _info):
        return self.get_role_display()

class AnimePrevFlowType(DjangoObjectType):
    relation_type = graphene.String()
    anime = graphene.Field(lambda: AnimeType)

    class Meta:
        model = RelatedAnime
        fields = "__all__"

    def resolve_relation_type(self, _info):
        return self.get_relation_type_display()
    
    def resolve_anime(self, _info):
        return self.from_anime

class AnimeNextFlowType(DjangoObjectType):
    relation_type = graphene.String()
    anime = graphene.Field(lambda: AnimeType)

    class Meta:
        model = RelatedAnime
        fields = "__all__"

    def resolve_relation_type(self, _info):
        return self.get_relation_type_display()
    
    def resolve_anime(self, _info):
        return self.to_anime
    
class AnimeType(DjangoObjectType):
    season = graphene.String()
    type = graphene.String()
    status = graphene.String()
    rating = graphene.String()
    genres = graphene.List(GenreType)

    characters = graphene.List(AnimeCharacterType)

    producers = graphene.List(AnimeCompanyType)
    studios = graphene.List(AnimeCharacterType)

    prev_anime = graphene.List(lambda: AnimeType)
    next_anime = graphene.List(lambda: AnimeType)

    class Meta:
        model = Anime
        fields = "__all__"

    def resolve_season(self, _info):
        return self.season_string

    def resolve_type(self, _info):
        return self.get_type_display()
    
    def resolve_status(self, _info):
        return self.get_status_display()
    
    def resolve_rating(self, _info):
        return self.get_rating_display()
    
    def resolve_genres(self, _info):
        return self.genres.all()
    
    def resolve_characters(self, _info):
        return AnimeCharacter.objects.filter(anime=self)
    
    def resolve_producers(self, _info):
        return []
    
    def resolve_studios(self, _info):
        return []
    
    def resolve_prev_anime(self, _info):
        return self.prev_anime
    
    def resolve_next_anime(self, _info):
        return self.next_anime
    
class AnimeListEntryType(DjangoObjectType):
    status = graphene.Int()

    class Meta:
        model = AnimeListEntry
        fields = "__all__"
    
    def resolve_status(self, _info):
        return self.status
    
class AnimeEpisodeType(DjangoObjectType):

    class Meta:
        model = AnimeEpisode
        fields = "__all__"
