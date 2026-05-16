import strawberry_django
from users.models import ArcadiaUser

@strawberry_django.type(ArcadiaUser, fields="__all__")
class ArcadiaUserType:
    pass