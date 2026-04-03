from rest_framework.exceptions import APIException

class ArcadiaException(APIException):
    status_code = 400
    default_detail = 'An internal error occured'
    default_code = 'arcadia_error'