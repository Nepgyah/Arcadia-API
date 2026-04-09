from main.exceptions import ArcadiaException

class UsersError(ArcadiaException):
    status_code = 400
    default_detail = 'An internal error occured within the Users service.'
    default_code = 'users_error'

class UserNotFoundError(UsersError):
    status_code = 404
    default_code = 'user_not_found'

    def __init__(self, user_id=None):
        if user_id:
            self.detail = f'User with ID: {user_id} not found.'
        else:
            self.detail = 'User not found'
            
        super().__init__(detail=self.detail)