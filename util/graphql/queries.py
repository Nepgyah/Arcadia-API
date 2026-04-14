from django.db.models import Q
import graphene

from miru.graphql.schema import AnimeType
from miru.models.anime import Anime
from asobu.graphql.schema import GameType
from asobu.models import Game
from talent.graphql.schema import CharacterType, VoiceActorType
from talent.models import  Character, VoiceActor
from users.graphql.schema import ArcadiaUserType
from users.models import ArcadiaUser

class GlobalSearchResults(graphene.ObjectType):
    anime = graphene.List(AnimeType)
    games = graphene.List(GameType)
    voice_actors = graphene.List(VoiceActorType)
    characters = graphene.List(CharacterType)

class Query(graphene.ObjectType):

    search_arcadia = graphene.Field(GlobalSearchResults, query_string=graphene.String(required=True))

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