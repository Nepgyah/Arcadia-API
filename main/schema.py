import strawberry
from asobu.graphql.query import AsobuQuery

@strawberry.type
class Query:

    @strawberry.field
    def asobu(self) -> AsobuQuery:
        return AsobuQuery()
    

schema = strawberry.Schema(query=Query)