from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import ArcadiaProfile
from accounts.repository import AccountsRepository
from accounts.exceptions import AccountsValidationError

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
        refresh_token = str(refresh)

        return access_token, refresh_token

class AccountsService:

    profile = ArcadiaProfileService()
    authentication = AuthenticationService()