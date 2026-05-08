import graphene

from asobu.graphql.schema import GameListEntryType, ReviewType
from asobu.service import AsobuService
from asobu.repository import AsobuRepository

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
            detail = f'Entry list created with Game ID: {game_id}'
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
            message = 'Entry successfully updated',
            detail = f'Entry with ID: {game_entry.id} updated.'
        )

class DeleteGameListEntry(graphene.Mutation):

    class Arguments:
        entry_id = graphene.ID()

    message = graphene.String()
    detail = graphene.String()
    
    @classmethod
    def mutate(cls, _root, info, entry_id):
        user = info.context.user
        AsobuRepository.delete_game_list_entry(user, entry_id)
        return DeleteGameListEntry(
            message = 'Entry deleted',
            detail = f'Game entry deleted for user f{user.id}'
        )

class CreateGameReview(graphene.Mutation):
    class Arguments:
        game_id = graphene.ID()
        review_text = graphene.String()

    message = graphene.String()
    detail = graphene.String()
    review = graphene.Field(ReviewType)

    @classmethod
    def mutate(cls, _root, info, game_id, review_text):
        user = info.context.user
        created_review = AsobuRepository.review.create_review(user.id, game_id, review_text)
        return CreateGameReview(
            review=created_review,
            message='Review created',
            detail=f'Created review with id: {created_review.id}'
        )

class UpdateGameReview(graphene.Mutation):
    class Arguments:
        game_id = graphene.ID()
        review_text = graphene.String()

    message = graphene.String()
    detail = graphene.String()
    review = graphene.Field(ReviewType)

    @classmethod
    def mutate(cls, _root, info, game_id, review_text):
        user = info.context.user
        created_review = AsobuRepository.review.update_review(user.id, game_id, review_text)
        return UpdateGameReview(
            review=created_review,
            message='Review created',
            detail=f'Created review with id: {created_review.id}'
        )

class DeleteGameReview(graphene.Mutation):
    class Arguments:
        game_id = graphene.ID()

    message = graphene.String()
    detail = graphene.String()

    @classmethod
    def mutate(cls, _root, info, game_id):
        user = info.context.user
        AsobuRepository.review.delete_review(user.id, game_id)
        return DeleteGameReview(
            message='Review deleted',
            detail='Review deleted'
        )
    
class Mutation(graphene.ObjectType):
    create_game_list_entry = CreateGameListMutation.Field()
    update_game_list_entry = UpdateGameListEntry.Field()
    delete_game_list_entry = DeleteGameListEntry.Field()
    create_game_review = CreateGameReview.Field()
    update_game_review = UpdateGameReview.Field()
    delete_game_review = DeleteGameReview.Field()