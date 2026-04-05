import graphene
from users.services import UserService

from .schema import (
    ArcadiaUserType
)

class Query(graphene.ObjectType):

    User = graphene.Field(ArcadiaUserType, user_id=graphene.ID(required=True))

    def resolve_User(_self, _info, user_id: int):
        return UserService.get_user_by_id(user_id)