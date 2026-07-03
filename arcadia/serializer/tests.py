from unittest.mock import patch
import pytest
from . import ReviewSerializer
from arcadia.exceptions import ArcadiaValidationError

@pytest.mark.django_db
class TestReviewSerializer:

    # Define the mock target path as a constant for easy maintenance
    MOCK_PROFILE_CHECK = 'arcadia.serializer.review_serializer.AccountsService.profile.does_profile_exist'

    # --- Valid Data Tests ---

    @staticmethod
    def test_valid_serializer_data(arcadia_profile_fixture):
        valid_data = {
            'profile_id': arcadia_profile_fixture.id,
            'score': 8,
            'text': 'This is a beautifully written review that easily passes the minimum length.'
        }
        
        with patch(TestReviewSerializer.MOCK_PROFILE_CHECK, return_value=True):
            serializer = ReviewSerializer(data=valid_data)
            assert serializer.is_valid() is True

    # --- Profile ID Validation Tests ---

    @staticmethod
    def test_validate_profile_id_not_found():
        invalid_data = {
            'profile_id': 999,
            'score': 5,
            'text': 'This is a beautifully written review that easily passes the minimum length.'
        }
        
        with patch(TestReviewSerializer.MOCK_PROFILE_CHECK, return_value=False):
            serializer = ReviewSerializer(data=invalid_data)
            with pytest.raises(ArcadiaValidationError):
                serializer.is_valid(raise_exception=True)

    # --- Score Validation Tests ---

    @staticmethod
    @pytest.mark.parametrize('invalid_score', [0, 11])
    def test_validate_score_out_of_bounds(arcadia_profile_fixture, invalid_score):
        invalid_data = {
            'profile_id': arcadia_profile_fixture.id,
            'score': invalid_score,
            'text': 'This is a beautifully written review that easily passes the minimum length.'
        }
        
        with patch(TestReviewSerializer.MOCK_PROFILE_CHECK, return_value=True):
            serializer = ReviewSerializer(data=invalid_data)
            with pytest.raises(ArcadiaValidationError):
                serializer.is_valid(raise_exception=True)


    # --- Text Length Validation Tests ---

    @staticmethod
    def test_validate_text_too_short(arcadia_profile_fixture):
        invalid_data = {
            'profile_id': arcadia_profile_fixture.id,
            'score': 7,
            'text': 'Too short'
        }
        
        with patch(TestReviewSerializer.MOCK_PROFILE_CHECK, return_value=True):
            serializer = ReviewSerializer(data=invalid_data)
            with pytest.raises(ArcadiaValidationError):
                serializer.is_valid(raise_exception=True)

    @staticmethod
    def test_validate_text_too_long(arcadia_profile_fixture):
        invalid_data = {
            'profile_id': arcadia_profile_fixture.id,
            'score': 7,
            'text': 'A' * 1501
        }
        
        with patch(TestReviewSerializer.MOCK_PROFILE_CHECK, return_value=True):
            serializer = ReviewSerializer(data=invalid_data)
            with pytest.raises(ArcadiaValidationError):
                serializer.is_valid(raise_exception=True)
            