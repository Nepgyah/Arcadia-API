import graphene
from .schema import GameCharacterType, GameType, DLCType
from asobu.models import GameCharacter, Game, DLC
import graphene_django_optimizer as gql_optimizer

class Query(graphene.ObjectType):

    game_by_id = graphene.Field(GameType, id=graphene.ID(required=True))
    games_by_category = graphene.List(GameType, category=graphene.String(required=False), count=graphene.Int(required=False))
    characters_by_game = graphene.List(GameCharacterType, id=graphene.ID(required=True))
    dlc_by_game = graphene.List(DLCType, game_id=graphene.ID(required=True))

    def resolve_game_by_id(self, info, id):
        return gql_optimizer.query(Game.objects.get(id=id), info)
    
    def resolve_games_by_category(self, info, category, count):
        if category == None:
            category = '-score'
        if count == None:
            count == 5

        return gql_optimizer.query(Game.objects.all().order_by(category)[:count], info)
    
    def resolve_characters_by_game(self, info, id):
        characters = GameCharacter.objects.filter(game_id=id)
        return characters
    
    def resolve_dlc_by_game(self, info, game_id):
        return DLC.objects.filter(game_id=game_id)