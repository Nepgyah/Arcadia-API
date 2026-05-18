from rest_framework.serializers import ModelSerializer
from miru.models import AnimeListEntry

class AnimeListEntrySerializer(ModelSerializer):

    class Meta:
        model = AnimeListEntry
        fields = "__all__"