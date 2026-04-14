import graphene
import asobu.graphql.query
import authorization.graphql.mutations
import base.schema
import miru.graphql.queries
import miru.graphql.mutations
import talent.graphql.query
import users.graphql.queries
import util.graphql.queries

class Query(
    asobu.graphql.query.Query,
    base.schema.Query,
    miru.graphql.queries.Query,
    talent.graphql.query.Query,
    users.graphql.queries.Query,
    util.graphql.queries.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    miru.graphql.mutations.Mutation,
    authorization.graphql.mutations.Mutation
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)