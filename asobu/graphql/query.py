import graphene
import graphene_django_optimizer as gql_optimizer
from asobu.models import GameCharacter, Game, DLC
from asobu.graphql.schema import GameCharacterType, GameType, DLCType

class Query(graphene.ObjectType):

    game_by_id = graphene.Field(GameType, game_id=graphene.ID(required=True))
    games_by_category = graphene.List(GameType, category=graphene.String(required=False), count=graphene.Int(required=False))
    characters_by_game = graphene.List(GameCharacterType, game_id=graphene.ID(required=True))
    dlc_by_game = graphene.List(DLCType, game_id=graphene.ID(required=True))

    def resolve_game_by_id(self, info, game_id):
        return gql_optimizer.query(Game.objects.get(id=game_id), info)
    
    def resolve_games_by_category(self, info, category, count):
        if category is None:
            category = '-score'
        if count is None:
            count = 5

        return gql_optimizer.query(Game.objects.all().order_by(category)[:count], info)
    
    def resolve_characters_by_game(self, _info, game_id):
        characters = GameCharacter.objects.filter(game_id=game_id)
        return characters
    
    def resolve_dlc_by_game(self, _info, game_id):
        return DLC.objects.filter(game_id=game_id)