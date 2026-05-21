from rest_framework.serializers import ModelSerializer
from accounts.models import ArcadiaProfile

class ProfileSerializer(ModelSerializer):

    class Meta:
        model = ArcadiaProfile
        exclude=['admin_account']

    