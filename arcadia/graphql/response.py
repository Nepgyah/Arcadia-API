import strawberry

@strawberry.interface
class MutationResponseType:
    message: str
    detail: str

@strawberry.type
class BaseMutationResponse(MutationResponseType):
    """Basic response type if no further objects are needed"""
    pass

@strawberry.type
class PaginationResultsType:
    per_page: int
    total_pages: int
    total_items: int