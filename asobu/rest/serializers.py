from rest_framework.serializers import ModelSerializer
from asobu.models import GameListEntry

class GameListEntrySerializer(ModelSerializer):

    class Meta:
        model = GameListEntry
        fields = "__all__"