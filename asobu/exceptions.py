from main.exceptions import ArcadiaException

class AsobuError(ArcadiaException):
    status_code = 400
    default_detail = 'An internal error occured within the Asobu service.'
    default_code = 'asobu_error'

class AsobuNotFound(AsobuError):
    status_code = 404

class AsobuServerError(AsobuError):
    status_code = 500
    default_detail = 'An unexpected error occured with the Asobu API'

