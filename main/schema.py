import graphene
import characters.schema
import base.schema
import miru.schema

class Query(
    characters.schema.Query,
    base.schema.Query,
    miru.schema.Query,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query)