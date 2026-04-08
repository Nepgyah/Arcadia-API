import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from users.models import ArcadiaUser
from users.repositories import UserRepository

class ArcadiaUserType(DjangoObjectType):
    list_data = GenericScalar()

    class Meta:
        model = ArcadiaUser
        fields = '__all__'

    def resolve_list_data(self, info):
        return UserRepository.get_user_list_stat(self.id)