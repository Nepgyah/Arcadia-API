import graphene
import talent.graphql.query
import base.schema
import miru.graphql.queries
import miru.graphql.mutations
import asobu.graphql.query

class Query(
    asobu.graphql.query.Query,
    miru.graphql.queries.Query,
    talent.graphql.query.Query,
    base.schema.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    miru.graphql.mutations.Mutation
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)