from main import settings
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import ArcadiaProfile
from accounts.repository import AccountsRepository
from accounts.exceptions import AccountsValidationError, AccountsAppError

class ArcadiaProfileService:

    @staticmethod
    def get_profile(profile_id: int) -> ArcadiaProfile:
        return AccountsRepository.profile.get_profile(profile_id)
    
    @staticmethod
    def does_profile_exist(profile_id: int) -> bool:
        return AccountsRepository.profile.does_profile_exist(profile_id)

class AuthenticationService:
    
    @staticmethod
    def login_as_admin(email: str, password: str) -> dict:
        """
            Verifies the admin and returns jwt tokens
        """
        if email is None:
            raise AccountsValidationError('You must provide a email')
        
        if password is None:
            raise AccountsValidationError("You must provide a password")

        arcadia_profile = AccountsRepository.authentication.admin_login(email, password)

        refresh = RefreshToken.for_user(arcadia_profile)
        access_token = str(refresh.access_token)
        access_token_expiry = timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        
        refresh_token = str(refresh)
        refresh_token_expiry = timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

        return {
            "access": {
                "value": str(access_token),
                "expiry": access_token_expiry
            },
            "refresh": {
                "value": str(refresh_token),
                "expiry": refresh_token_expiry
            },
        }

    @staticmethod
    def refresh_token(refresh_token: str | None) -> dict:
        if refresh_token is None:
            raise AccountsValidationError("You must provide a refresh token")
        
        try:
            new_refresh = RefreshToken(refresh_token)
            new_refresh_expiry = timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

            new_access = str(new_refresh.access_token)
            new_access_expiry = timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

            return {
                "access": {
                    "value": str(new_access),
                    "expiry": new_access_expiry
                },
                "refresh": {
                    "value": str(new_refresh),
                    "expiry": new_refresh_expiry
                },
            }
        except Exception as e:
            raise AccountsAppError("Unexpected error occured while refreshing the token") from e


class AccountsService:

    profile = ArcadiaProfileService()
    authentication = AuthenticationService()