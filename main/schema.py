import graphene
import talent.schema
import base.schema
import miru.graphql.queries
import miru.graphql.mutations

class Query(
    talent.schema.Query,
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