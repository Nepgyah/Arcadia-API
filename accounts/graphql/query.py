from typing import Optional
import strawberry
from accounts.graphql.types import ArcadiaProfileType
from accounts.service import AccountsService

@strawberry.type
class AppStats:
    anime: int
    games: int
    manga: int
    events: int

@strawberry.type
class AccountsQuery:

    @strawberry.field
    def profile(self, info: strawberry.Info, pk: Optional[int] = None) -> ArcadiaProfileType:
        if pk is None:
            profile_id = info.context.user_id
            return AccountsService.profile.get_profile(profile_id)
        return AccountsService.profile.get_profile(pk)