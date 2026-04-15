from django.db.models import Q
import graphene

from miru.graphql.schema import AnimeType
from miru.models.anime import Anime
from miru.service import MiruService
from asobu.graphql.schema import GameType
from asobu.models import Game
from asobu.service import AsobuService
from talent.graphql.schema import CharacterType, VoiceActorType
from talent.models import  Character, VoiceActor
from users.graphql.schema import ArcadiaUserType
from users.models import ArcadiaUser

class GlobalSearchResults(graphene.ObjectType):
    anime = graphene.List(AnimeType)
    games = graphene.List(GameType)
    voice_actors = graphene.List(VoiceActorType)
    characters = graphene.List(CharacterType)

class ArcadiaStatisticsResults(graphene.ObjectType):
    anime_count = graphene.Int()
    game_count = graphene.Int()

class Query(graphene.ObjectType):

    search_arcadia = graphene.Field(GlobalSearchResults, query_string=graphene.String(required=True))
    arcadia_stats = graphene.Field(ArcadiaStatisticsResults)

    def resolve_search_arcadia(_root, _info, query_string):
        anime = Anime.objects.filter(Q(title__icontains=query_string))
        games = Game.objects.filter(Q(title__icontains=query_string))
        voice_actors = VoiceActor.objects.filter(Q(first_name__icontains=query_string) | Q(last_name__icontains=query_string))
        characters = Character.objects.filter(Q(first_name__icontains=query_string) | Q(last_name__icontains=query_string))

        return GlobalSearchResults(
            anime = anime,
            games = games,
            voice_actors = voice_actors,
            characters = characters
        )
    
    def resolve_arcadia_stats(_root, _info):
        anime_count = MiruService.total_anime_count()
        game_count = AsobuService.total_game_count()
        return ArcadiaStatisticsResults(
            anime_count=anime_count,
            game_count=game_count
        )