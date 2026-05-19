import strawberry
from asobu.graphql.query import AsobuQuery
from asobu.graphql.mutation import AsobuMutation
from base.graphql.query import BaseQuery
from miru.graphql.query import MiruQuery

@strawberry.type
class ArcadiaMutation(AsobuMutation):
    pass

@strawberry.type
class ArcadiaQuery:

    @strawberry.field
    def asobu(self) -> AsobuQuery:
        return AsobuQuery()
    
    @strawberry.field
    def base(self) -> BaseQuery:
        return BaseQuery()
    
    @strawberry.field
    def miru(self) -> MiruQuery:
        return MiruQuery()
    
schema = strawberry.Schema(query=ArcadiaQuery, mutation=ArcadiaMutation)