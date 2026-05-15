from rest_framework import serializers
from .exceptions import AsobuError
from .models import GameListEntry

class AsobuSerializer(serializers.ModelSerializer):

    def is_valid(self, *, raise_exception=False):
        valid = super().is_valid(raise_exception=raise_exception)

        if not valid and raise_exception is True:
            field_name = next(iter(self.errors))
            error_details = self.errors[field_name]

            error_message = error_details[0] if isinstance(error_details, list) else error_details

            raise AsobuError(f'{field_name}: {error_message}')
        
class GameListEntrySerializer(AsobuSerializer):

    class Meta:
        model = GameListEntry
        fields = "__all__"

    # def validate(self, attrs):
    #     if attrs['start_play_date'] is not None and attrs['end_play_date'] is not None:
    #         if attrs['start_play_date'] > attrs['end_play_date']:
    #             raise serializers.ValidationError('End date must occur after start')
        
    #     return attrs