import strawberry

@strawberry.interface
class MutationResponseType:
    message: str
    detail: str

@strawberry.input
class PaginationInput:
    per_page: int = 12
    target_page: int = 1

@strawberry.input
class SortInput:
    category: str
    direction: str

@strawberry.type
class PaginationResultsType:
    per_page: int
    total_pages: int
    total_items: int