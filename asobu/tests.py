import pytest
from asobu.exceptions import AsobuValidationError
from asobu.serializers import GameListEntrySerializer

@pytest.mark.django_db
class TestGameListEntrySerializer:

    @staticmethod
    def test_invalidDates_raisesValidationError(game_fixture, arcadia_profile_fixture):
        data = {
            "profile_id": arcadia_profile_fixture.id,
            "game": game_fixture,
            "score": 5,
            "status": 0,
            "note": "",
            "start_play_date": "2024-10-10",
            "end_play_date": "2023-10-10"
        }
        
        serializer = GameListEntrySerializer(data=data)
        with pytest.raises(AsobuValidationError):
            serializer.is_valid(raise_exception=True)

    @staticmethod
    def test_invalidUser_raisesValidationError(game_fixture):
        data = {
            "profile_id": 9999,
            "game": game_fixture,
            "score": 5,
            "status": 0,
            "note": "",
            "start_play_date": "2024-10-10",
            "end_play_date": "2025-10-10"
        }
        
        serializer = GameListEntrySerializer(data=data)
        with pytest.raises(AsobuValidationError):
            serializer.is_valid(raise_exception=True)
