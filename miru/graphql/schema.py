import graphene
from graphene_django import DjangoObjectType
from miru.models.anime import Anime
from miru.models.relations import (
    AnimeCharacter,
    AnimeEpisode,
    RelatedAnime
)
from miru.models.list_entry import AnimeListEntry
from talent.graphql.schema import CharacterType
from base.schema import GenreType

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
    status = graphene.String()
    type = graphene.String()
    rating = graphene.String()
    season = graphene.String()
    genres = graphene.List(GenreType)
    characters = graphene.List(AnimeCharacterType)
    studio = graphene.String()
    prev_anime = graphene.Field(AnimePrevFlowType)
    next_anime = graphene.Field(AnimeNextFlowType)
    latest_episode = graphene.Field(lambda: AnimeEpisodeType)

    class Meta:
        model = Anime
        fields = "__all__"

    def resolve_rating(self, _info):
        return self.get_rating_display()
    
    def resolve_type(self, _info):
        return self.get_type_display()
    
    def resolve_status(self, _info):
        return self.get_status_display()
    
    def resolve_season(self, _info):
        if self.season:
            return str(self.season)
        return 'N/A'
    
    def resolve_genres(self, _info):
        return self.genres.all()
    
    def resolve_studio(self, _info):
        return self.studio
    
    def resolve_characters(self, _info):
        return AnimeCharacter.objects.filter(anime=self)
    
    def resolve_prev_anime(self, _info):
        try:
            return RelatedAnime.objects.get(to_anime_id=self.id, relation_type='series_entry')
        except RelatedAnime.DoesNotExist:
            return None
        
    def resolve_next_anime(self, _info):
        try:
            return RelatedAnime.objects.get(from_anime_id=self.id, relation_type='series_entry')
        except RelatedAnime.DoesNotExist:
            return None
    
    def resolve_latest_episode(self, _info):
        return AnimeEpisode.objects.filter(anime=self).last()
    
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
