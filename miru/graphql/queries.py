import graphene

from miru.service.miru_service import MiruService
from users.models import User

from util.schema import (
    MediaSortInput,
    PaginationInput
)

from .schema import (
    AnimeType,
    AnimeCharacterType,
    AnimeListEntryType,
    AnimeEpisodeType
)


class AnimeFilterInput(graphene.InputObjectType):
    title = graphene.String()
    type = graphene.Int()
    status = graphene.Int()

class AnimeFilterResults(graphene.ObjectType):
    animes = graphene.List(AnimeType)
    page_count = graphene.Int()
    current_page = graphene.Int()
    total = graphene.Int()

class AnimeEntryListResults(graphene.ObjectType):
    username = graphene.String()
    watching = graphene.List(AnimeListEntryType)
    completed = graphene.List(AnimeListEntryType)
    plan_to = graphene.List(AnimeListEntryType)
    on_hold = graphene.List(AnimeListEntryType)

class Query(graphene.ObjectType):

    anime_by_id = graphene.Field(AnimeType, id=graphene.ID(required=True))
    characters_by_anime = graphene.List(AnimeCharacterType, id=graphene.ID(required=True))
    anime_by_category = graphene.List(AnimeType, category=graphene.String(required=True), count=graphene.Int(required=False))
    search_anime = graphene.Field(AnimeFilterResults, filters=AnimeFilterInput(), sort=MediaSortInput(), pagination=PaginationInput())
    get_anime_list = graphene.Field(AnimeEntryListResults, user_id=graphene.ID(required=True))
    get_anime_list_entry = graphene.Field(AnimeListEntryType, user_id=graphene.ID(required=True), anime_id=graphene.ID(required=True))
    get_anime_episodes = graphene.List(AnimeEpisodeType, anime_id=graphene.ID(required=True))

    def resolve_anime_by_id(self, _info, id):
        return MiruService.get_anime_by_id(id)
    
    def resolve_characters_by_anime(self, _info, id):
        return MiruService.get_characters_by_anime(id)
    
    def resolve_anime_by_category(self, _info, category, count):
        return MiruService.get_anime_by_category(f'-{category}', count)
    
    def resolve_search_anime(self, _info, filters, sort, pagination):
        animes, page_count, current_page, total = MiruService.search_anime(filters, sort, pagination)
        return AnimeFilterResults(
            animes = animes,
            page_count = page_count,
            current_page = current_page,
            total = total
        )

    def resolve_get_anime_list(self, _info, user_id):
        user = User.objects.get(id=user_id)
        watching, completed, plan_to, on_hold = MiruService.get_anime_list_by_user_id(user_id)
        return AnimeEntryListResults (
            username = user.username,
            watching = watching,
            completed = completed,
            plan_to = plan_to,
            on_hold = on_hold
        )
    
    def resolve_get_anime_list_entry(self, _info, user_id, anime_id):
        return MiruService.get_anime_list_entry(user_id, anime_id)
    
    def resolve_get_anime_episodes(self, _info, anime_id):
        return MiruService.episodes_by_anime_id(anime_id)