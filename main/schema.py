import strawberry
from asobu.graphql.query import AsobuQuery
from asobu.graphql.mutation import AsobuMutation
from base.graphql.query import BaseQuery
from miru.graphql.query import MiruQuery
from miru.graphql.mutation import MiruMutation

@strawberry.type
class ArcadiaMutation(
    AsobuMutation,
    MiruMutation
):
    pass

@strawberry.type(description="Overall namespace for the Arcadia graphql queries")
class ArcadiaQuery:

    @strawberry.field(description="Namespace for queries related to the Asobu app")
    def asobu(self) -> AsobuQuery:
        return AsobuQuery()
    
    @strawberry.field(description="Namespace for queries related to general media (Franchise, Genres)")
    def base(self) -> BaseQuery:
        return BaseQuery()
    
    @strawberry.field(description="Namespace for queries related to the Miru app")
    def miru(self) -> MiruQuery:
        return MiruQuery()
    
schema = strawberry.Schema(query=ArcadiaQuery, mutation=ArcadiaMutation)