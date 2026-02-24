import graphene

class AddAnimeListEntryMetaData(graphene.InputObjectType):
    current_episode = graphene.Int(required=False, default_value=0)
    score = graphene.Float(required = False, default_value = 0.0)
    start_watch_date = graphene.Date()
    end_watch_date = graphene.Date(required=False)

class AddAnimeListEntryMutation(graphene.Mutation):
    # Define the return data
    ok = graphene.Boolean()

    # Define the arguements for the mutation
    class Arguments:
        anime_id = graphene.ID()
        user_id = graphene.ID()
        data = AddAnimeListEntryMetaData(required=False)

    # Define the for the mutation go here, use services, repo, etc
    @classmethod
    def mutate(cls, root, info, anime_id, user_id, data):
        ok = True

        # Return an instance, make sure to set the values of your returns
        return AddAnimeListEntryMutation(ok=ok)
    
class Mutation(graphene.ObjectType):
    add_anime_list_entry = AddAnimeListEntryMutation.Field()