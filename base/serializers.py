from rest_framework.serializers import ModelSerializer
from accounts.service import AccountsService
from main.exceptions import ArcadiaValidationError

class MediaReviewSerializer(ModelSerializer):

    def validate_profile_id(self, value):

        if AccountsService.profile.does_profile_exist(value) is False:
            raise ArcadiaValidationError('Arcadia profile does not exist')
        return value
    
    def validate_score(self, value):
        if value < 1:
            raise ArcadiaValidationError('Score cannot be less than 1')
        if value > 10:
            raise ArcadiaValidationError('Score cannot be greater than 10')
        return value
    
    def validate_text(self, value):
        if len(value) < 24:
            raise ArcadiaValidationError('Review is too short (min: 24)')
        if len(value) > 1500:
            raise ArcadiaValidationError('Review is too long (max: 1500)')
        return value