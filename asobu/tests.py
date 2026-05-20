import pytest
from rest_framework.exceptions import ValidationError
from asobu.exceptions import AsobuValidationError
from asobu.serializers import GameListEntrySerializer

@pytest.mark.django_db
class TestGameListEntrySerializer:

    @staticmethod
    def test_invalidDates_raisesValidationError(game_fixture, arcadia_user_fixture):
        data = {
            "user": arcadia_user_fixture,
            "game": game_fixture,
            "score": 5,
            "status": 0,
            "note": "",
            "start_play_date": "2024-10-10",
            "end_play_date": "2023-10-10"
        }
        
        serializer = GameListEntrySerializer(data=data)
        with pytest.raises(AsobuValidationError) as e:
            serializer.is_valid(raise_exception=True)
