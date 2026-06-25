import strawberry

@strawberry.input
class MediaReviewInput:
    score: int | None = 0
    text: str | None = None