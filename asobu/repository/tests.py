import pytest
from rest_framework.exceptions import ValidationError

from asobu.models import Review
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
    pass