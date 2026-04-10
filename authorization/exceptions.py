from rest_framework.exceptions import APIException

class AuthorizationError(APIException):
    status_code = 400
    default_detail = 'An authorization related error occured'
    default_code = 'auth_error'

class NotLoggedInError(AuthorizationError):
    status_code = 401
    default_detail = 'You must be logged in'
    default_code = 'auth_error_not_logged_in'

class UserPermissionError(AuthorizationError):
    status_code = 403
    default_detail = 'You are not allowed to access this data'
    default_code = 'auth_error_no_access'