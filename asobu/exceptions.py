from main.exceptions import ArcadiaAppError, ArcadiaValidationError, ArcadiaNotFoundError

class AsobuError(ArcadiaAppError):
    default_detail = 'An internal error occured within the Asobu service.'
    default_code = 'asobu_internal_error'

class AsobuValidationError(ArcadiaValidationError):
    default_detail = 'An error occured processing input within the Asobu app'
    default_code = 'asobu_input_error'

class AsobuNotFound(ArcadiaNotFoundError):
    default_detail = 'Unable to find requested Asobu resource'
    default_code = 'asobu_not_found'

