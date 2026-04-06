from rest_framework.serializers import ModelSerializer
from users.models import ArcadiaUser

class UserSerializer(ModelSerializer):
    
    class Meta:
        model = ArcadiaUser
        fields = '__all__'