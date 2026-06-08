from django.contrib.auth.models import User 
from accounts.models import ArcadiaProfile
from accounts.exceptions import AccountsAppNotFound

class ArcadiaProfileRepository:
    
    @staticmethod
    def get_profile(profile_id: int) -> ArcadiaProfile:
        try:
            return ArcadiaProfile.objects.get(id=profile_id)
        except ArcadiaProfile.DoesNotExist:
            raise AccountsAppNotFound(
                'Unable to find Arcadia Profile',
                'accounts_profile_not_found'
            ) from None
        
    @staticmethod
    def does_profile_exist(profile_id: int) -> bool:
        return ArcadiaProfile.objects.filter(id=profile_id).exists()

class AuthenticationRepository:

    @staticmethod
    def admin_login(email: str, password: str) -> ArcadiaProfile:
        """
            Normal django login utilizes username, this allows for login via email
        """

        try:
            admin_user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AccountsAppNotFound("Admin not found") from None
        
        if not admin_user.check_password(password):
            raise AccountsAppNotFound("Incorrect password") from None
        
        try:
            return ArcadiaProfile.objects.get(admin_account=admin_user)
        except ArcadiaProfile.DoesNotExist:
            raise AccountsAppNotFound("Unable to find arcadia profile") from None

class AccountsRepository:

    profile = ArcadiaProfileRepository()
    authentication = AuthenticationRepository()