import graphene
from miru.service.miru_service import MiruService

class AddAnimeListEntryMetaData(graphene.InputObjectType):
    current_episode = graphene.Int(required=False, default_value=0)
    score = graphene.Float(required = False, default_value = 0.0)
    start_watch_date = graphene.Date(required=False, default_value=None)
    end_watch_date = graphene.Date(required=False, default_value=None)

class AnimeListEntryStatusEnum(graphene.Enum):
    WATCHING = 0
    COMPLETED = 1
    PLAN_TO = 2
    ON_HOLD = 3

class AddAnimeListMutation(graphene.Mutation):
    # Define the return data
    ok = graphene.Boolean()

    # Define the arguements for the mutation
    class Arguments:
        anime_id = graphene.ID()
        user_id = graphene.ID()
        status = AnimeListEntryStatusEnum()
        details = AddAnimeListEntryMetaData(required=False)

    # Define the for the mutation go here, use services, repo, etc
    @classmethod
    def mutate(cls, root, info, anime_id, user_id, status, details):
        ok = MiruService.add_anime_list_entry(anime_id, user_id, status.value, details)

        # Return an instance, make sure to set the values of your returns
        return AddAnimeListMutation(ok=ok)

class UpdateAnimeListMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        anime_id = graphene.ID()
        user_id = graphene.ID()
        status = AnimeListEntryStatusEnum(required=False)
        details = AddAnimeListEntryMetaData(required=False)

    @staticmethod
    def mutate(root, info, anime_id, user_id, status, details):
        ok = MiruService.update_anime_list_entry(anime_id, user_id, status.value, details)

        return UpdateAnimeListMutation(ok=ok)

class DeleteAnimeListMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        user_id = graphene.ID()
        anime_id = graphene.ID()

    @staticmethod
    def mutate(root, info, user_id, anime_id):
        ok = MiruService.delete_anime_list_entry(user_id, anime_id)

        return DeleteAnimeListMutation(ok=ok)
        
class Mutation(graphene.ObjectType):
    add_anime_list_entry = AddAnimeListMutation.Field()
    update_anime_list_entry = UpdateAnimeListMutation.Field()
    delete_anime_list_entry = DeleteAnimeListMutation.Field()