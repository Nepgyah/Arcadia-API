from rest_framework.exceptions import APIException, ValidationError, NotFound

class ArcadiaAppError(APIException):
    default_detail = 'An internal error occured'
    default_code = 'arcadia_error'

class ArcadiaValidationError(ValidationError):
    default_code = "arcadia_invalid_input"

class ArcadiaNotFoundError(NotFound):
    default_code = "arcadia_not_found"