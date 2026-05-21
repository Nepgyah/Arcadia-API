from rest_framework.serializers import ModelSerializer
from miru.models import AnimeListEntry
from miru.exceptions import MiruValidationError

class AnimeListEntrySerializer(ModelSerializer):

    class Meta:
        model = AnimeListEntry
        fields = "__all__"

    def validate(self, attrs):
       
        start_date = attrs['start_watch_date']
        end_date = attrs['end_watch_date']
        if start_date and end_date:
            if start_date > end_date:
                raise MiruValidationError("Start date cannot be past end date")
            
        return attrs