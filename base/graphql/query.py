import strawberry
from base.graphql.types import FranchiseType, GenreType
from base.service import FranchiseService, GenreService

@strawberry.type
class BaseQuery:

    @strawberry.field
    def franchise(self, pk: int) -> FranchiseType:
        return FranchiseService.get_franchise(pk)
    
    @strawberry.field
    def genre(self, pk: int) -> GenreType:
        return GenreService.get_genre(pk)
    
    @strawberry.field
    def genres(self, id_list: list[int]) -> list[GenreType]:
        return GenreService.get_genres(id_list)