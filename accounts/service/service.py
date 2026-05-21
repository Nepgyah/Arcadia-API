from accounts.models import ArcadiaProfile
from accounts.repository import AccountsRepository

class ArcadiaProfileService:

    @staticmethod
    def get_profile(profile_id: int) -> ArcadiaProfile:
        return AccountsRepository.profile.get_profile(profile_id)
    
    @staticmethod
    def does_profile_exist(profile_id: int) -> bool:
        return AccountsRepository.profile.does_profile_exist(profile_id)

class AccountsService:

    profile = ArcadiaProfileService()