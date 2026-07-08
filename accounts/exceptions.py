from rest_framework.exceptions import APIException, NotFound, ValidationError

class AccountsAppError(APIException):
    default_detail = "An internal error occurred within the Accounts app"
    default_code = "accounts_internal_error"

class AccountsValidationError(APIException):
    status_code = 400
    default_detail = "An error occured processing input within the Accounts app"
    default_code = "accounts_input_error"

class AccountsAppNotFound(NotFound):
    default_detail = "Unable to find the requested Accounts resouce"
    default_code = "accounts_not_found"