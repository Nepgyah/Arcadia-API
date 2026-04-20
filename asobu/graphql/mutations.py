import graphene

from asobu.graphql.schema import GameListEntryType
from asobu.service import AsobuService

class GameListEntryMetadata(graphene.InputObjectType):
    score = graphene.Int()
    note = graphene.String()
    review = graphene.String()
    start_play_date = graphene.String()
    end_play_date = graphene.String()

class CreateGameListMutation(graphene.Mutation):
    class Arguments:
        game_id = graphene.ID()
        status = graphene.Int()
        details = GameListEntryMetadata(required=False)

    game_entry = graphene.Field(GameListEntryType)
    message = graphene.String()
    detail = graphene.String()

    @classmethod
    def mutate(_cls, _root, info, game_id, status, details):
        user = info.context.user
        game_entry = AsobuService.create_game_list_entry(user, game_id, status, details)

        return CreateGameListMutation(
            game_entry = game_entry,
            message = 'Game successfully added',
            detail = f'Entry list created with Game ID: f{game_id}'
        )
    
class Mutation(graphene.ObjectType):
    create_game_list_entry = CreateGameListMutation.Field()