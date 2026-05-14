import strawberry

@strawberry.interface
class MutationResponseType:
    message: str
    detail: str