import graphene
from graphene_django import DjangoObjectType
from users.models import ArcadiaUser

class ArcadiaUserType(DjangoObjectType):

    class Meta:
        model = ArcadiaUser
        fields = '__all__'