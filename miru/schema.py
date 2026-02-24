import graphene
from graphene_django import DjangoObjectType
from .models import (
    Anime,
    AnimeCharacter
)
from characters.schema import CharacterType
from .service.miru_service import MiruService
from base.schema import GenreType
from util.schema import (
    MediaSortInput,
    PaginationInput
)
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
    
class AnimeFilterInput(graphene.InputObjectType):
    title = graphene.String()
    type = graphene.Int()
    status = graphene.Int()

class AnimeFilterResults(graphene.ObjectType):
    animes = graphene.List(AnimeType)
    page_count = graphene.Int()
    current_page = graphene.Int()
    total = graphene.Int()
    
class Query(graphene.ObjectType):

    anime_by_id = graphene.Field(AnimeType, id=graphene.Int(required=True))
    characters_by_anime = graphene.List(AnimeCharacterType, id=graphene.Int(required=True))
    anime_by_category = graphene.List(AnimeType, category=graphene.String(required=True), count=graphene.Int(required=False))
    search_anime = graphene.Field(AnimeFilterResults, filters=AnimeFilterInput(), sort=MediaSortInput(), pagination=PaginationInput())

    def resolve_anime_by_id(self, info, id):
        return MiruService.get_anime_by_id(id)
    
    def resolve_characters_by_anime(self, info, id):
        return MiruService.get_characters_by_anime(id)
    
    def resolve_anime_by_category(self, info, category, count):
        return MiruService.get_anime_by_category(f'-{category}', count)
    
    def resolve_search_anime(self, info, filters, sort, pagination):
        animes, page_count, current_page, total = MiruService.search_anime(filters, sort, pagination)
        return AnimeFilterResults(
            animes = animes,
            page_count = page_count,
            current_page = current_page,
            total = total
        )