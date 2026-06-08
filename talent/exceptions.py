from main.exceptions import ArcadiaAppError, ArcadiaNotFoundError, ArcadiaValidationError

class TalentError(ArcadiaAppError):
    default_detail = 'An internal error occured within the Talent service.'
    default_code = 'talent_internal_error'

class TalentNotFound(ArcadiaNotFoundError):
    default_detail = 'Unable to find requested Talent resource'
    default_code = 'talent_not_found'

class TalentValidationError(ArcadiaValidationError):
    default_detail = "An error occured processing input within the Talent app"
    default_code="talent_validation_error"
