from rest_framework.serializers import ModelSerializer
from base.serializers import MediaReviewSerializer
from accounts.service import AccountsService
from miru.models import AnimeListEntry, AnimeReview, CustomAnimeList
from miru.exceptions import MiruValidationError

class AnimeListEntrySerializer(ModelSerializer):

    class Meta:
        model = AnimeListEntry
        fields = "__all__"

    def validate_profile_id(self, value):

        if AccountsService.profile.does_profile_exist(value) is False:
            raise MiruValidationError('Arcadia profile does not exist')
        return value
    
    def validate(self, attrs):
       
        start_date = attrs['start_watch_date']
        end_date = attrs['end_watch_date']
        if start_date and end_date:
            if start_date > end_date:
                raise MiruValidationError("Start date cannot be past end date")
            
        return attrs
    
class AnimeReviewSerializer(MediaReviewSerializer):

    class Meta:
        model = AnimeReview
        fields = "__all__"

class CustomAnimeListSerializer(ModelSerializer):

    class Meta:
        model = CustomAnimeList
        fields = ['title', 'profile_id', 'is_public']

    def validate_title(self, value):
        if len(value) > 125:
            raise MiruValidationError("Title too long (Max: 125)")
        return value
