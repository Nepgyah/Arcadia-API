from rest_framework.exceptions import APIException, ValidationError, NotFound

class ArcadiaAppError(APIException):
    default_detail = 'An internal error occured'
    default_code = 'arcadia_error'

class ArcadiaValidationError(APIException):
    default_code = "arcadia_invalid_input"
    status_code = 400

class ArcadiaNotFoundError(NotFound):
    default_code = "arcadia_not_found"