from functools import wraps
from accounts.repository import AccountsRepository
from accounts.exceptions import AccountsAppNotFound

def require_profile(func):
    """Checks if the profile id is valid, must be first in arguements"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        profile_id = args[0]

        if not AccountsRepository.profile.does_profile_exist(profile_id):
            raise AccountsAppNotFound("Arcadia profile not found")
        
        return func(*args, **kwargs)
    return wrapper