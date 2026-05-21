import strawberry
from accounts.graphql.types import ArcadiaProfileType
from accounts.service import AccountsService

@strawberry.type
class AccountsQuery:

    @strawberry.field
    def profile(self, pk: int) -> ArcadiaProfileType:
        return AccountsService.profile.get_profile(pk)