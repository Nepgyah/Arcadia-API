import graphene
from graphene_django import DjangoObjectType
from miru.models import (
    Anime,
    AnimeCharacter,
    AnimeListEntry,
    AnimeRelation,
    AnimeEpisode
)
from talent.schema import CharacterType
from base.schema import GenreType

class AnimeCharacterType(DjangoObjectType):
    character = graphene.Field(CharacterType)
    role = graphene.String()

    class Meta:
        model = AnimeCharacter
        fields = "__all__"

    def resolve_role(self, info):
        return self.get_role_display()

class AnimePrevFlowType(DjangoObjectType):
    relation_type = graphene.String()
    anime = graphene.Field(lambda: AnimeType)

    class Meta:
        model = AnimeRelation
        fields = "__all__"

    def resolve_relation_type(self, info):
        return self.get_relation_type_display()
    
    def resolve_anime(self, info):
        return self.from_anime

class AnimeNextFlowType(DjangoObjectType):
    relation_type = graphene.String()
    anime = graphene.Field(lambda: AnimeType)

    class Meta:
        model = AnimeRelation
        fields = "__all__"

    def resolve_relation_type(self, info):
        return self.get_relation_type_display()
    
    def resolve_anime(self, info):
        return self.to_anime
    
class AnimeType(DjangoObjectType):
    status = graphene.String()
    type = graphene.String()
    rating = graphene.String()
    season = graphene.String()
    genres = graphene.List(GenreType)
    characters = graphene.List(AnimeCharacterType)
    studio = graphene.String()
    prev_anime = graphene.Field(AnimePrevFlowType)
    next_anime = graphene.Field(AnimeNextFlowType)

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
    
    def resolve_studio(self, info):
        return self.studio
    
    def resolve_characters(self, info):
        return AnimeCharacter.objects.filter(anime=self)
    
    def resolve_prev_anime(self, info):
        try:
            return AnimeRelation.objects.get(to_anime_id=self.id, relation_type='series_entry')
        except AnimeRelation.DoesNotExist:
            return None
        
    def resolve_next_anime(self, info):
        try:
            return AnimeRelation.objects.get(from_anime_id=self.id, relation_type='series_entry')
        except AnimeRelation.DoesNotExist:
            return None
        
class AnimeListEntryType(DjangoObjectType):
    status = graphene.Int()

    class Meta:
        model = AnimeListEntry
        field = "__all__"
    
    def resolve_status(self, info):
        return self.status
    
class AnimeEpisodeType(DjangoObjectType):

    class Meta:
        model = AnimeEpisode
        field = "__all__"
