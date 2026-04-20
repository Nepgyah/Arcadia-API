import graphene

from asobu.graphql.schema import GameListEntryType
from asobu.service import AsobuService
from asobu.exceptions import AsobuNotFound

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
    def mutate(cls, _root, info, game_id, status, details):
        user = info.context.user
        game_entry = AsobuService.create_game_list_entry(user, game_id, status, details)

        return cls(
            game_entry = game_entry,
            message = 'Game successfully added',
            detail = f'Entry list created with Game ID: f{game_id}'
        )
    
class UpdateGameListEntry(graphene.Mutation):

    class Arguments:
        game_id = graphene.ID()
        status = graphene.Int()
        details = GameListEntryMetadata(required=False)

    game_entry = graphene.Field(GameListEntryType)
    message = graphene.String()
    detail = graphene.String()

    @classmethod
    def mutate(cls, _root, info, game_id, status, details):
        user = info.context.user
        game_entry = AsobuService.update_game_list_entry(user, game_id, status, details)
        
        return cls(
            game_entry = game_entry,
            message = 'Entry successfully updated.',
            detail = f'Entry with ID: {game_entry.id} updated.'
        )

class Mutation(graphene.ObjectType):
    create_game_list_entry = CreateGameListMutation.Field()
    update_game_list_entry = UpdateGameListEntry.Field()