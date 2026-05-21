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

class AccountsRepository:

    profile = ArcadiaProfileRepository()