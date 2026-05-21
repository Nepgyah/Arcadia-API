import strawberry
from main.graphql.permissions import IsAuthenticated
from accounts.service import AccountsService

@strawberry.type
class TokenType:
    value: str
    expiry: str

@strawberry.type
class AdminLoginResponse:
    access: str
    refresh: str

@strawberry.type
class AccountMutation:

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def login_as_admin(self, email: str, password: str) -> AdminLoginResponse:
        access_token, refresh_token = AccountsService.authentication.login_as_admin(email, password)

        return AdminLoginResponse(
            access=access_token,
            refresh=refresh_token
        )
    
    @strawberry.mutation
    def refresh_token(self, refresh_token: str = None):
        tokens = AccountsService.authentication.refresh_token(refresh_token)
