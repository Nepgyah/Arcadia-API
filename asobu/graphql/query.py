import graphene
import graphene_django_optimizer as gql_optimizer
from users.repositories import UserRepository
from asobu.models import Game
from asobu.graphql.schema import GameCharacterType, GameType, DLCType, GameListEntryType, GameReviewType
from asobu.repository import AsobuRepository
from asobu.service import AsobuService

class GameList(graphene.ObjectType):
    username = graphene.String()
    playing = graphene.List(GameListEntryType)
    completed = graphene.List(GameListEntryType)  
    plan_to = graphene.List(GameListEntryType)
    on_hold = graphene.List(GameListEntryType)
    replaying = graphene.List(GameListEntryType)

class Query(graphene.ObjectType):

    game_by_id = graphene.Field(GameType, game_id=graphene.ID(required=True))
    games_by_category = graphene.List(GameType, category=graphene.String(required=False), count=graphene.Int(required=False))
    characters_by_game = graphene.List(GameCharacterType, game_id=graphene.ID(required=True))
    asobu_game_reviews = graphene.List(GameReviewType, game_id=graphene.ID())
    dlc_by_game = graphene.List(DLCType, game_id=graphene.ID(required=True))
    game_list_entry = graphene.Field(GameListEntryType, game_id=graphene.ID())
    user_game_list = graphene.Field(GameList, user_id=graphene.ID())

    def resolve_game_by_id(self, info, game_id):
        return gql_optimizer.query(Game.objects.get(id=game_id), info)
    
    def resolve_games_by_category(self, info, category, count):
        if category is None:
            category = '-score'
        if count is None:
            count = 5

        return gql_optimizer.query(Game.objects.all().order_by(category)[:count], info)
    
    def resolve_characters_by_game(self, _info, game_id):
        return AsobuRepository.get_characters_by_game(game_id)
    
    def resolve_asobu_game_reviews(self, _info, game_id):
        return AsobuRepository.get_reviews_by_game(game_id)

    def resolve_dlc_by_game(self, _info, game_id):
        return AsobuRepository.get_dlc_by_game(game_id)
    
    def resolve_game_list_entry(self, info, game_id):
        user = info.context.user
        return AsobuRepository.get_game_list_entry(user, game_id, info)
    
    def resolve_user_game_list(self, info, user_id=None):
        if user_id:
            user = UserRepository.get_user_by_id(user_id=user_id)
        else:
            user = info.context.user
        list_data = AsobuService.get_game_list_by_user(user)
        
        return GameList(
            username = user.username,
            playing = list_data['playing'],
            completed = list_data['completed'],
            plan_to = list_data['plan_to'],
            on_hold = list_data['on_hold'],
            replaying = list_data['replaying']
        )