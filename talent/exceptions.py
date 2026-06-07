from main.exceptions import ArcadiaAppError, ArcadiaNotFoundError

class TalentError(ArcadiaAppError):
    default_detail = 'An internal error occured within the Talent service.'
    default_code = 'talent_internal_error'

class TalentNotFound(ArcadiaNotFoundError):
    default_detail = 'Unable to find requested Talent resource'
    default_code = 'talent_not_found'

