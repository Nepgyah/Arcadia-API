import pytest
from rest_framework.exceptions import ValidationError

from asobu.models import Review, GameListEntry
from asobu.repository import AsobuRepository
from asobu.exceptions import AsobuError, AsobuNotFound, AsobuValidationError
from asobu.conftest import create_video_game_characters

@pytest.mark.django_db
class TestAsobuRepoGame:

    @staticmethod
    def test_getGameCount_returnsCount(game_fixture):
        assert AsobuRepository.game.get_game_count() == 1

    @staticmethod
    def test_getGame_validID_returnsGameObject(game_fixture):
        result = AsobuRepository.game.get_game(game_fixture.id)
        assert result == game_fixture

    @staticmethod
    def test_getGame_invalidID_raisesNotFound():
        with pytest.raises(AsobuNotFound):
            AsobuRepository.game.get_game(99999)

    @staticmethod
    def test_checkGameExists_valid_returnsTrue(game_fixture):
        assert AsobuRepository.game.does_game_exist(game_fixture.id) is True

    @staticmethod
    def test_checkGameExists_invalidID_returnsFalse():
        assert AsobuRepository.game.does_game_exist(9999) is False

    @staticmethod
    def test_getDLC_valid_returnsDLC(game_dlc_fixture):
        dlc = AsobuRepository.game.get_dlc(game_dlc_fixture.game.id)
        assert dlc.first() == game_dlc_fixture

    @staticmethod
    def test_getDLC_invalidGame_returnsEmpty():
        assert len(AsobuRepository.game.get_dlc(9999)) == 0

    @staticmethod
    def test_getReviews_valid_returnsReviews(game_review_fixture):
        reviews = AsobuRepository.game.get_reviews(game_review_fixture.game.id)
        assert reviews.first() == game_review_fixture

    @staticmethod
    def test_getReviews_invalidGame_returnsEmpty():
        assert len(AsobuRepository.game.get_reviews(9999)) == 0

@pytest.mark.django_db
class TestAsobuRepoList:
    
    @staticmethod
    def test_createEntry_valid_createsEntry(game_fixture):
        details = {
            "score": 10,
            "status": 0,
            "note": "Umazing",
            "start_play_date": None,
            "end_play_date": None
        }

        entry = AsobuRepository.list.create_entry(
            1,
            game_fixture.id,
            **details
        )

        assert entry.game == game_fixture
        assert entry.profile_id == 1

    @staticmethod
    def test_getEntry_valid_returnsEntry(game_list_entry_fixture):
        entry = AsobuRepository.list.get_entry(
            game_list_entry_fixture.profile_id,
            game_list_entry_fixture.game.id
        )

        assert entry == game_list_entry_fixture

    @staticmethod
    def test_getEntry_invalidID_raisesAsobuNotFound(arcadia_profile_fixture):
        with pytest.raises(AsobuNotFound):
            AsobuRepository.list.get_entry(
                arcadia_profile_fixture.id,
                99999
            )

    @staticmethod
    def test_updateEntry_validInfo_updatesEntry(game_list_entry_fixture):
        details = {
            "score": 5,
            "status": 2,
            "note": "Umazing",
            "start_play_date": None,
            "end_play_date": None
        }

        entry = AsobuRepository.list.update_entry(
            game_list_entry_fixture,
            **details
        )

        assert entry.score == 5
        assert entry.status == 2

    @staticmethod
    def test_deleteEntry_valid_deletesEntry(game_list_entry_fixture):
        AsobuRepository.list.delete_entry(game_list_entry_fixture)

        assert GameListEntry.objects.filter(
            profile_id=game_list_entry_fixture.profile_id,
            game=game_list_entry_fixture.game
        ).exists() is False