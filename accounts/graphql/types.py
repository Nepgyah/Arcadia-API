import strawberry_django
from accounts.models import ArcadiaProfile

@strawberry_django.type(ArcadiaProfile, exclude=['admin_account'])
class ArcadiaProfileType:
    pass