from main.exceptions import ArcadiaAppError, ArcadiaNotFoundError, ArcadiaValidationError

class MiruError(ArcadiaAppError):
    default_detail = 'An internal error occured within the Miru app'
    default_code = 'miru_internal_error'

class MiruValidationError(ArcadiaValidationError):
    default_detail = 'An error occured processing input within the Miru app'
    default_code = 'miru_input_error'

class MiruNotFoundError(ArcadiaNotFoundError):
    default_detail = "Unable to find requested Miru resource"
    default_code = "miru_not_found"