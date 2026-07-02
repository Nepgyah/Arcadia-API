from rest_framework.exceptions import APIException, NotFound

class ArcadiaAppError(APIException):
    default_detail = 'An internal error occured'
    default_code = 'arcadia_error'

class ArcadiaValidationError(APIException):
    
    # Importing the drf validation exception converts detail into a list of error objects
    # making message display from the api on the frontend more of a hassle
    # Inheriting the default APIException removes this issue with returning a single string
    default_code = "arcadia_invalid_input"
    status_code = 400

class ArcadiaNotFoundError(NotFound):
    default_code = "arcadia_not_found"