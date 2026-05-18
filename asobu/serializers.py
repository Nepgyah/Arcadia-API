from rest_framework import serializers
from .exceptions import AsobuError
from .models import GameListEntry, Review

class AsobuSerializer(serializers.ModelSerializer):

    def is_valid(self, *, raise_exception=False):
        valid = super().is_valid()

        if not valid and raise_exception is True:
            field_name = next(iter(self.errors))
            error_details = self.errors[field_name]
            error_message = error_details[0] if isinstance(error_details, list) else error_details

            raise AsobuError(f'{str(field_name).capitalize()}: {error_message}')
        
class GameReviewSerializer(AsobuSerializer):

    class Meta:
        model = Review
        fields = "__all__"
        
class GameListEntrySerializer(AsobuSerializer):

    class Meta:
        model = GameListEntry
        fields = "__all__"
        
    def validate(self, attrs):

        start_date = attrs['start_play_date']
        end_date = attrs['end_play_date']
        if start_date and end_date:
            if start_date > end_date:
                raise AsobuError('Start date cannot be after end date')

        return attrs