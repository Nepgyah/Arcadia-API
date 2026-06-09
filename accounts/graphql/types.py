import strawberry_django
from accounts.models import ArcadiaProfile
from miru.service import MiruService

@strawberry_django.type(ArcadiaProfile, exclude=['admin_account'])
class ArcadiaProfileType:

    @strawberry_django.field
    def anime_list_count(self) -> int:
        return MiruService.list.get_user_list_count(self.id)