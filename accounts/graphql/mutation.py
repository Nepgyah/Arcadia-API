import strawberry
from main.graphql.permissions import IsAuthenticated
from accounts.service import AccountsService

@strawberry.type
class TokenType:
    value: str
    expiry: str

@strawberry.type
class TokenSetResponse:
    access: TokenType
    refresh: TokenType

@strawberry.type
class AccountMutation:

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def login_as_admin(self, email: str, password: str) -> TokenSetResponse:
        tokens = AccountsService.authentication.login_as_admin(email, password)
        access = TokenType(
            value=tokens['access']['value'],
            expiry=tokens['access']['expiry']
        )
        refresh = TokenType(
            value=tokens['refresh']['value'],
            expiry=tokens['refresh']['expiry']
        )
        return TokenSetResponse(
            access=access,
            refresh=refresh
        )
    
    @strawberry.mutation
    def refresh_token(self, refresh_token: str = None) -> TokenSetResponse:
        tokens = AccountsService.authentication.refresh_token(refresh_token)

        access = TokenType(
            value=tokens['access']['value'],
            expiry=tokens['access']['expiry']
        )
        refresh = TokenType(
            value=tokens['refresh']['value'],
            expiry=tokens['refresh']['expiry']
        )

        return TokenSetResponse(
            access=access,
            refresh=refresh
        )
