import strawberry

@strawberry.input
class MediaReviewInput:
    score: int | None = 0
    text: str | None = None

@strawberry.input
class PaginationInput:
    per_page: int = 12
    target_page: int = 1

@strawberry.input
class SortInput:
    category: str
    direction: str