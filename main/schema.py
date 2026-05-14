import strawberry
from asobu.graphql.query import AsobuQuery
from asobu.graphql.mutation import AsobuMutation

@strawberry.type
class ArcadiaMutation(AsobuMutation):
    pass

@strawberry.type
class ArcadiaQuery:

    @strawberry.field
    def asobu(self) -> AsobuQuery:
        return AsobuQuery()
    

schema = strawberry.Schema(query=ArcadiaQuery, mutation=ArcadiaMutation)