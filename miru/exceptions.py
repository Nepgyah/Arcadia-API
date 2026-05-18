from main.exceptions import ArcadiaException

class MiruError(ArcadiaException):
    status_code = 500
    default_detail = 'An internal error occured within the Miru app'
    default_code = 'miru_internal_error'

class MiruNotFound(MiruError):
    status_code = 404
    default_detail = "Cannot find requested miru resource"
    default_code = "miru_not_found"