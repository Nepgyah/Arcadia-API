import graphene

from miru.service import MiruService
from users.models import ArcadiaUser
from miru.exceptions import AnimeNotFoundError
from util.schema import (
    MediaSortInput,
    PaginationInput,
    PaginationResults
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

class AnimeSearchResults(graphene.ObjectType):
    animes = graphene.List(AnimeType)
    pagination_results = graphene.Field(PaginationResults)

class AnimeEntryListResults(graphene.ObjectType):
    username = graphene.String()
    watching = graphene.List(AnimeListEntryType)
    completed = graphene.List(AnimeListEntryType)
    plan_to = graphene.List(AnimeListEntryType)
    on_hold = graphene.List(AnimeListEntryType)

class Query(graphene.ObjectType):

    anime_by_id = graphene.Field(AnimeType, anime_id=graphene.ID(required=True))
    characters_by_anime = graphene.List(AnimeCharacterType, anime_id=graphene.ID(required=True))
    anime_by_category = graphene.List(AnimeType, category=graphene.String(required=True), count=graphene.Int(required=False))
    search_anime = graphene.Field(AnimeSearchResults, filter_input=AnimeFilterInput(), sort_input=MediaSortInput(), pagination_input=PaginationInput())
    get_anime_list = graphene.Field(AnimeEntryListResults, user_id=graphene.ID(required=True))
    get_anime_list_entry = graphene.Field(AnimeListEntryType, anime_id=graphene.ID(required=True))
    get_anime_episodes = graphene.List(AnimeEpisodeType, anime_id=graphene.ID(required=True))

    def resolve_anime_by_id(root, _info, anime_id):
        try:
            return MiruService.get_anime_by_id(anime_id)
        except AnimeNotFoundError as e:
            raise e
    
    def resolve_characters_by_anime(root, _info, anime_id):
        return MiruService.get_characters_by_anime(anime_id)
        
    def resolve_anime_by_category(root, _info, category, count):
        return MiruService.get_anime_by_category(f'-{category}', count)
    
    def resolve_search_anime(root, _info, filter_input, sort_input, pagination_input):
        animes, pagination_results = MiruService.search_anime(filter_input, sort_input, pagination_input)
        return AnimeSearchResults(
            animes = animes,
            pagination_results = pagination_results
        )

    def resolve_get_anime_list(root, _info, user_id):
        user = ArcadiaUser.objects.get(id=user_id)
        watching, completed, plan_to, on_hold = MiruService.get_anime_list_by_user_id(user_id)
        return AnimeEntryListResults (
            username = user.username,
            watching = watching,
            completed = completed,
            plan_to = plan_to,
            on_hold = on_hold
        )
    
    def resolve_get_anime_list_entry(root, info, anime_id):
        user = info.context.user
        return MiruService.get_anime_list_entry(user, anime_id)
    
    def resolve_get_anime_episodes(root, _info, anime_id):
        return MiruService.episodes_by_anime_id(anime_id)