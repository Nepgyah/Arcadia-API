import graphene
import characters.schema
import base.schema
import miru.graphql.queries
import miru.graphql.mutations

class Query(
    characters.schema.Query,
    base.schema.Query,
    miru.graphql.queries.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    miru.graphql.mutations.Mutation
):
    pass
schema = graphene.Schema(query=Query, mutation=Mutation)